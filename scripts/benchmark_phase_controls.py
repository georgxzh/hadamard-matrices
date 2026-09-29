"""Bounded factorial controls: translation, PAF updates, and aligned PB gauges.

One worker, three repeats, ten-second solver probes. No p=37 model/search.
The Gray traversal, mask update, projected shifts and bucket join are held
fixed when comparing incremental versus recomputed PAFs.
"""
from __future__ import annotations

import hashlib
import json
import platform
import random
import statistics
import time
from collections import Counter
from datetime import datetime, timezone
from itertools import combinations
from pathlib import Path

from scripts.benchmark_staged_uncompression import _known_pair, _artifact
from scripts.benchmark_ternary_phase import solve
from scripts.classify_p5_lifts import ROOT, CATALOG, save, digest, packed_key, peak_memory
from src.legendre import compress, structured_compressed_pair
from src.pb_model import PBConstraint, OPBArtifact
from src.staged_uncompression import FactorThreeBranch
from src.ternary_phase import PhaseRow, TernaryPhasePBModel

OUTPUT = ROOT / 'results/phase_controls'


class AlignedPhaseModel(TernaryPhasePBModel):
    """Use the exact same binary anchor gauge as the canonical XOR model."""
    def __init__(self, *pair):
        super().__init__(*pair)
        self.anchors = tuple(2 if row.compressed[row.active[0]] == 1 else 0 for row in self.rows)

    def iter_constraints(self):
        replacements = {self.phase_variable(r, 0, 0): self.phase_variable(r, 0, a)
                        for r, a in enumerate(self.anchors)}
        for c in super().iter_constraints():
            if len(c.terms) == 1 and c.terms[0][0] == 1 and c.terms[0][1] in replacements:
                c = PBConstraint(((1, replacements[c.terms[0][1]]),), c.relation, c.rhs)
            yield c

    def canonicalize_pair(self, first, second):
        return tuple(row.decode(tuple((a - phases[0] + target) % 3 for a in phases))
                     for row, target, phases in
                     zip(self.rows, self.anchors, (r.encode(x) for r, x in zip(self.rows, (first, second))), strict=True))

    def write_opb(self, path):
        super().write_opb(path)
        text = path.read_text().replace('anchor phase zero', 'anchor phases aligned to binary lexicographic gauge')
        path.write_text(text, encoding='ascii', newline='\n')
        return OPBArtifact(path, path.stat().st_size, digest(path))


def iter_gray_keys(compressed, *, canonical, incremental):
    """Identical candidate order/mask maintenance in both evaluation modes."""
    row = PhaseRow(compressed)
    n, k, length = row.length, len(row.active), 3*row.length
    phases, directions = [0]*k, [1]*k
    mask = sum(1 << i for i, v in enumerate(row.decode(phases)) if v == -1)
    signature = [row.paf_terms(s)[0] for s in range(1, n)]
    adjacent = [[] for _ in range(k)]
    if incremental:
        for u, v in combinations(range(k), 2):
            r = row.active[v]-row.active[u]
            w = row.delta[row.active[u]]*row.delta[row.active[v]]
            signature[r-1] += w
            edge = (u, v, r-1, n-r-1, w)
            adjacent[u].append(edge); adjacent[v].append(edge)
    while True:
        yield (bytes(v+length for v in signature) if incremental
               else packed_key(mask, length, n-1))
        index = k-1
        while index >= int(canonical) and not 0 <= phases[index]+directions[index] <= 2:
            directions[index] *= -1
            index -= 1
        if index < int(canonical): return
        if incremental:
            for u, v, forward, reverse, weight in adjacent[index]:
                difference = (phases[v]-phases[u]) % 3
                if difference != 1: signature[forward if difference == 0 else reverse] -= weight
        old = phases[index]
        phases[index] += directions[index]
        mask ^= (1 << (row.active[index]+old*n)) | (1 << (row.active[index]+phases[index]*n))
        if incremental:
            for u, v, forward, reverse, weight in adjacent[index]:
                difference = (phases[v]-phases[u]) % 3
                if difference != 1: signature[forward if difference == 0 else reverse] += weight


def join_control(pair, canonical, incremental):
    started = time.perf_counter()
    active = [sum(abs(c)==1 for c in row) for row in pair]
    expected = [3**(k-int(canonical)) for k in active]
    stored = min(range(2), key=lambda r: expected[r])
    counts = [0, 0]; table = Counter(); matches = 0
    hashers = [hashlib.sha256(), hashlib.sha256()]
    target = 6*len(pair[0])-2
    for side in (stored, 1-stored):
        for key in iter_gray_keys(pair[side], canonical=canonical, incremental=incremental):
            counts[side] += 1
            hashers[side].update(key)
            if counts[side] % 1024 == 0 and time.perf_counter()-started > 60:
                raise TimeoutError('one-minute control limit')
            if side == stored: table[key] += 1
            elif all(v <= target for v in key):
                matches += table.get(bytes(target-v for v in key), 0)
    assert counts == expected
    return {'seconds':time.perf_counter()-started, 'canonical':canonical,
            'incremental':incremental, 'counts':counts, 'matched_pairs':matches,
            'ordered_pairs':matches*(9 if canonical else 1),
            'ordered_stream_sha256':[h.hexdigest() for h in hashers], 'signatures':len(table)}


def main():
    started = time.perf_counter()
    solver = ROOT/'tmp/tools/roundingsat/roundingsat.exe'
    verifier = ROOT/'tmp/tools/veripb-3.0.2/bin/veripb.exe'
    scratch = ROOT/'tmp/phase_controls'
    OUTPUT.mkdir(parents=True, exist_ok=True); scratch.mkdir(parents=True, exist_ok=True)
    catalog = json.loads(CATALOG.read_text())
    branch5 = tuple(tuple(catalog[0][key]) for key in ('first','second'))
    empty5 = tuple(tuple(catalog[2][key]) for key in ('first','second'))
    known3 = _known_pair(3)
    branch3 = tuple(compress(row,9) for row in known3)
    old = json.loads((ROOT/'results/ternary_phase/metadata.json').read_text())
    branch7 = tuple(tuple(row) for row in old['branch_acquisition'][0]['pair'])
    metadata = {'started_utc':datetime.now(timezone.utc).isoformat(), 'workers':1,
                'python':platform.python_version(),'platform':platform.platform(),
                'repeats':3,'search_seconds':10,'restart_multiplier':100,
                'solver':_artifact(solver,tracked=False),'verifier':_artifact(verifier,tracked=False),
                'source_sha256':digest(Path(__file__)),'catalog_sha256':digest(CATALOG),
                'join_controls':[], 'solver_controls':{},
                'method':'same Gray order and masks; exact projected keys; aligned binary PB gauges',
                'limitations':'deterministic solver repeats are timing replicates, not independent search seeds; no p=37'}
    rng = random.Random(20260929)
    for repetition in range(3):
        tasks = [(name, pair, c, i) for name,pair in [('p5_rank1',branch5),('p5_rank3',empty5)]
                 for c in (False,True) for i in (False,True)]
        rng.shuffle(tasks)
        for name,pair,canonical,incremental in tasks:
            result = join_control(pair,canonical,incremental)
            assert result['ordered_pairs'] == (27 if name=='p5_rank1' else 0)
            metadata['join_controls'].append({'branch':name,'repeat':repetition,**result})
            print(f"join {name} gauge={canonical} incremental={incremental}: {result['seconds']:.3f}s",flush=True)
        save(OUTPUT/'metadata.json',metadata)
    for name in ('p5_rank1','p5_rank3'):
        for canonical in (False,True):
            records = [r for r in metadata['join_controls'] if r['branch']==name and r['canonical']==canonical]
            assert len({tuple(r['ordered_stream_sha256']) for r in records}) == 1
    metadata['join_medians'] = {
        f'{name}_canonical{int(c)}_incremental{int(i)}': statistics.median(r['seconds'] for r in metadata['join_controls']
             if r['branch']==name and r['canonical']==c and r['incremental']==i)
        for name in ('p5_rank1','p5_rank3') for c in (False,True) for i in (False,True)}
    for repetition in range(3):
        tasks = [(name,pair,encoding) for name,pair in [('p3',branch3),('p5_rank1',branch5),('p7',branch7)]
                 for encoding in ('binary','phase')]
        rng.shuffle(tasks)
        for name,pair,encoding in tasks:
            p = len(pair[0])//3
            model = (FactorThreeBranch(*structured_compressed_pair(p,3),*pair).model(
                     canonical_translations=True,projected_correlations=True)
                     if encoding=='binary' else AlignedPhaseModel(*pair))
            label=f'{name}_{encoding}_repeat{repetition}'
            metadata['solver_controls'][label] = solve(model,label,solver,verifier,OUTPUT,scratch,10,100)
            save(OUTPUT/'metadata.json',metadata)
    metadata.update(completed_utc=datetime.now(timezone.utc).isoformat(),
                    elapsed_seconds=time.perf_counter()-started,peak_process_working_set_bytes=peak_memory(),
                    scratch_bytes=sum(p.stat().st_size for p in scratch.rglob('*') if p.is_file()))
    save(OUTPUT/'metadata.json',metadata)
    print(json.dumps({'elapsed_seconds':metadata['elapsed_seconds'],'join_medians':metadata['join_medians']},indent=2),flush=True)


if __name__=='__main__': main()
