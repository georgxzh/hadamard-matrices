"""Independent checks of census bijections and benchmark controls."""
import json
from itertools import product

import pytest

from scripts.classify_p5_lifts import CATALOG, binary, independent_masks, symmetry_partition, transfer_masks
from scripts.audit_p5_classification import canonical_mask, invert_solution
from scripts.benchmark_phase_controls import AlignedPhaseModel, iter_gray_keys
from scripts.benchmark_staged_uncompression import _known_pair
from src.legendre import compress, structured_compressed_pair
from src.staged_uncompression import FactorThreeBranch
from src.ternary_phase import PhaseRow


def test_symmetry_partition_covers_catalog_and_inverts_arbitrary_preimages():
    catalog=json.loads(CATALOG.read_text())
    groups,mappings=symmetry_partition(catalog)
    assert len(groups)==79
    assert sorted(t for group in groups.values() for t in group)==list(range(1,1165))
    for target,mapping in mappings.items():
        source=catalog[mapping['representative_rank']-1]
        pair=tuple(tuple(source[k]) for k in ('first','second'))
        target_pair=tuple(tuple(catalog[target-1][k]) for k in ('first','second'))
        # Nonconstant phase patterns, including preimages that are not LPs.
        masks=[]
        for row in pair:
            phase=PhaseRow(row)
            values=phase.decode(tuple((i*i+i//2)%3 for i in range(len(phase.active))))
            masks.append(canonical_mask(values,row))
        image=transfer_masks(masks,mapping['operation'],target_pair)
        assert tuple(compress(binary(m),15) for m in image)==target_pair
        assert invert_solution(image,mapping['operation'],pair)==tuple(masks)


def test_independent_mask_gauge_has_exact_coverage_for_all_residue_signs():
    for compressed in ((1,-1,3,-3),(-1,1,-3,3)):
        row=PhaseRow(compressed)
        actual={tuple(1-2*((m>>i)&1) for i in range(12)) for m in independent_masks(compressed)}
        expected={row.decode((0,a)) for a in range(3)}
        assert actual==expected
        assert len(list(independent_masks(compressed,False)))==9


@pytest.mark.parametrize('canonical',[False,True])
def test_control_paf_streams_have_identical_gray_order(canonical):
    for binary_row in _known_pair(3):
        row=compress(binary_row,9)
        assert list(iter_gray_keys(row,canonical=canonical,incremental=False))==list(
            iter_gray_keys(row,canonical=canonical,incremental=True))


@pytest.mark.parametrize('p',[3,5])
def test_aligned_phase_and_binary_gauges_select_same_lift(p):
    known=_known_pair(p)
    pair=tuple(compress(row,3*p) for row in known)
    phase=AlignedPhaseModel(*pair)
    binary_model=FactorThreeBranch(*structured_compressed_pair(p,3),*pair).model(
        canonical_translations=True,projected_correlations=True)
    solutions=[]
    for s,t in product(range(3),repeat=2):
        candidate=tuple(tuple(row[(i+shift*3*p)%(9*p)] for i in range(9*p))
                        for row,shift in zip(known,(s,t)))
        phase_ok=phase.first_failed_constraint(*candidate) is None
        binary_ok=binary_model.first_failed_constraint(*candidate) is None
        assert phase_ok==binary_ok
        if phase_ok: solutions.append(candidate)
    assert solutions==[phase.canonicalize_pair(*known)]
