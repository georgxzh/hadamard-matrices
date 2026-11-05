"""Check the mask canonicalizer against an independent tuple orbit oracle."""
from itertools import product
from math import gcd

from scripts.crosswalk_p5_equivalence import canonical_pair


def oracle(pair,n):
    rows=[tuple((m >> i)&1 for i in range(n)) for m in pair]
    keys=[]
    for u in range(1,n):
        if gcd(u,n)!=1: continue
        choices=[]
        for row in rows:
            choices.append(min(sum(row[(sign*u*i+t)%n] << i for i in range(n))
                               for sign in (-1,1) for t in range(n)))
        keys.append(tuple(sorted(choices)))
    return min(keys)


def test_all_small_pairs_against_tuple_oracle():
    for pair in product(range(32),repeat=2):
        assert canonical_pair(pair,5)==oracle(pair,5)


def test_length45_census_examples_against_tuple_oracle():
    import json
    records=json.loads(open('results/p5_classification/classification.json').read())
    examples=[tuple(r['solutions'][0]) for r in records if r['solutions']][::25]
    for pair in examples:
        key=canonical_pair(pair,45)
        assert key==oracle(pair,45)
        assert canonical_pair(key,45)==key
