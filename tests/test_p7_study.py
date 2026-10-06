"""Portfolio canonicalization, exact witness rejection, and frozen-harness parity."""
import json
import pytest
from scripts.p7_study import ROOT,canonical,identifier,verify_masks,timed_search
from src.spectral_join import search


def control():
    return json.loads((ROOT/'results/spectral_join/p7_metadata.json').read_text())['pair']


def test_independent_intermediate_translation_class():
    pair=control(); expected=canonical(pair)
    for first in (0,7,14):
        for second in (0,7,14):
            rotated=[row[t:]+row[:t] for row,t in zip(pair,(first,second))]
            assert canonical(rotated)==expected
    assert identifier(expected)==identifier([list(row) for row in expected])


def test_bad_witness_rejected():
    with pytest.raises(AssertionError): verify_masks(control(),[0,0])


@pytest.mark.parametrize('mode',(0,1,2))
def test_timed_harness_matches_frozen_wrapper(mode,tmp_path):
    limits={'seconds_per_trial':10,'node_cap':1000,'table_cap':15000000,'solution_cap':100000}
    a=timed_search(control(),tmp_path/'timed.json',mode,limits)
    b=search(*control(),tmp_path/'frozen.json',mode=mode,seconds=10,node_limit=1000,
             stored_candidate_limit=15000000,solution_limit=100000)
    assert (tmp_path/'timed.input.txt').read_bytes()==(tmp_path/'frozen.input.txt').read_bytes()
    for key in ('rows','complete','canonical_pairs','ordered_pairs','solutions','stop_reason'):
        if key=='rows':
            assert [{k:v for k,v in r.items() if k!='elapsed_seconds'} for r in a[key]]==[
                   {k:v for k,v in r.items() if k!='elapsed_seconds'} for r in b[key]]
        else: assert a[key]==b[key]
    assert a['canonical_pairs'] is None and a['ordered_pairs'] is None
    assert a['python_setup_seconds']>=0 and a['validation_seconds']>=0
    assert a['native_process_wall_seconds']>=a['elapsed_seconds']
