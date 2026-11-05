"""Independent exact enumeration, coverage, and spectral safety checks."""
import json
from fractions import Fraction
from pathlib import Path

import pytest

from src.spectral_join import build_native,coefficients,pi_bounds,SCALE,search
from src.legendre import compress
from scripts.benchmark_staged_uncompression import _known_pair
from tests.test_phase_propagation import exact_masks


@pytest.fixture(scope='module',autouse=True)
def native():
    build_native()


def test_pi_interval_contains_independent_machin_bounds():
    # Independently sum with a longer series, retaining an explicit remainder.
    def atan(x):
        total=sum(((-1)**j*x**(2*j+1)/Fraction(2*j+1) for j in range(50)),Fraction())
        return total,total+x**101/Fraction(101)
    a,b=atan(Fraction(1,5)); c,d=atan(Fraction(1,239))
    lo,hi=pi_bounds()
    assert lo<=16*a-4*d<16*b-4*c<=hi
    assert hi-lo<Fraction(1,10**39)


@pytest.mark.parametrize('mode',[0,1,2])
def test_native_search_matches_independent_p3_masks(mode,tmp_path):
    pair=tuple(compress(row,9) for row in _known_pair(3))
    r=search(*pair,tmp_path/f'p3_{mode}.json',mode=mode)
    assert r['complete'] and r['ordered_pairs']==135
    assert [tuple(m) for m in r['solutions']]==exact_masks(pair)
    for row in r['rows']:
        assert row['leaves']+row['excluded_completions']==row['expected']
        assert row['accepted']+row['full_rejections']==row['leaves']


def test_every_p5_census_witness_passes_integer_spectral_test():
    data=coefficients(45)
    census=json.loads(Path('results/p5_classification/classification.json').read_text())
    checked=0
    for branch in census:
        for pair in branch['solutions']:
            for mask in pair:
                row=[1-2*((mask>>i)&1) for i in range(45)]
                for c,s in zip(data['cosine'],data['sine']):
                    a=max(0,abs(sum(x*y for x,y in zip(row,c)))-45)
                    b=max(0,abs(sum(x*y for x,y in zip(row,s)))-45)
                    assert a*a+b*b<=SCALE*SCALE*92
            checked+=1
    assert checked==2976


def test_limits_have_null_exact_counts(tmp_path):
    pair=tuple(compress(row,9) for row in _known_pair(3))
    for kw in ({'node_limit':1},{'mode':0,'stored_candidate_limit':1},
               {'mode':0,'solution_limit':1},{'seconds':0.0000001}):
        r=search(*pair,tmp_path/(str(len(kw))+'limited.json'),**kw)
        assert not r['complete'] and r['canonical_pairs'] is None and r['ordered_pairs'] is None
    with pytest.raises(ValueError): coefficients(333)
