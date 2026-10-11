"""Independent coordinate/phase and hypothesis checks for the new proof audit."""
from itertools import combinations, product

from scripts.audit_fiber_structure import (
    affine, affine_cycles, compress, fixed_row_check, phase_gauge, row, tiny_census,
)


def test_kernel_action_against_explicit_layer_permutation():
    for q,n in ((3,3),(3,9),(5,5)):
        length=q*n
        # Coordinate-level proof check, including the p=q case.
        for a,b in product(range(q),repeat=2):
            for i,k in product(range(n),range(q)):
                assert ((1+a*n)*(i+k*n)+b*n)%length == i+n*((k+a*i+b)%q)
            cycles=affine_cycles(q,n,a,b)
            assert sorted(i for c in cycles for i in c)==list(range(length))


def test_phase_formula_for_every_normalized_length_nine_row():
    # Does not use PhaseRow or the census: decode all 126 rows directly.
    for neg in combinations(range(9),4):
        mask=sum(1<<i for i in neg);c=compress(row(mask,9),3)
        mask=phase_gauge(mask,c);x=row(mask,9)
        active=[i for i,v in enumerate(c) if abs(v)==1];anchor=active[0]
        phases={i:next(k for k in range(3) if x[i+3*k]==-c[i]) for i in active}
        for t in range(3):
            y=row(phase_gauge(affine(mask,9,1+3*t),c),9)
            for i in active:
                predicted=(phases[i]-t*(i-anchor))%3
                assert y[i+3*predicted]==-c[i]


def test_hypotheses_and_tiny_independent_lp_counts():
    assert tiny_census(3,1)['fiber_histogram']=={9:1}
    assert tiny_census(9,3)['fiber_histogram']=={54:18}
    # Dropping the LP condition permits a kernel-fixed row with sum one.
    x=(-1,1,-1,1,1,-1,1,1,-1)
    assert sum(x)==1 and compress(x,3)==(1,3,-3)
    mask=sum(1<<i for i,v in enumerate(x) if v==-1)
    assert affine(mask,9,4)==mask
    assert sum(v*v for v in compress(x,3))*2==38


def test_affine_fixed_rows_cannot_meet_pair_energy():
    for q,n in ((3,3),(5,5)):
        result=fixed_row_check(q,n)
        assert result['minimum_row_energy']+n>result['pair_energy_required']
