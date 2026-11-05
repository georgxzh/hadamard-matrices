"""Pin the new research round without touching any inherited artifact."""
import hashlib

from scripts.primitive_local_audit import ROOT, OUT, load, save
from scripts.verify_primitive_local import frozen_digest
from src.legendre import _reduce_mod_monic


def main():
    verification=load('results/primitive_local/verification.json')
    assert frozen_digest()==verification['baseline']
    residues=[]
    for r in verification['mod_9_survivors']:
        assert all(x%9==0 for x in r['norm_defect'])
        j=list(_reduce_mod_monic([x//9 for x in r['norm_defect']],[1]*5))
        j += [0]*(4-len(j));j=[x%3 for x in j]
        assert (not any(j))==(r['pi_valuation']=='infinity' or r['pi_valuation']>=13)
        residues.append({'rank':r['rank'],'masks':r['masks'],'J':j,
                         'passes_K9':r['passes_K9'],'pi_valuation':r['pi_valuation']})
    save('next_residue.json',{'modulus':[1]*5,'characteristic':3,'records':residues,
         'interpretation':'Next residue on saved modulo-nine survivors; not a structural nonvanishing proof.'})
    paths=[p for p in OUT.iterdir() if p.is_file() and p.name!='manifest.json']
    paths += [ROOT/p for p in ('research/primitive_local_obstruction.md',
         'scripts/primitive_local_audit.py','scripts/verify_primitive_local.py',
         'scripts/package_primitive_local.py','tests/test_primitive_local.py')]
    entries=[{'path':p.relative_to(ROOT).as_posix(),'bytes':p.stat().st_size,
              'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(paths)]
    save('manifest.json',{'algorithm':'sha256','base_commit':verification['base_commit'],'files':entries})
    print({'files_pinned':len(entries),'new_bytes_excluding_manifest':sum(e['bytes'] for e in entries),
           'frozen_files_preserved':verification['baseline']['files'],'paper_unchanged':True})


if __name__=='__main__':main()
