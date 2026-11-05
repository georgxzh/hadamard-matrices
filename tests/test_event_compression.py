from fractions import Fraction
from itertools import product
from random import Random

from scripts.event_compression_products import (indicator, contract, form_value,
    event_probability, local_dipole, carry_feedback)
from scripts.primitive_local_audit import load, red, mul, POW
from scripts.residue_formula import binomial


def test_contraction_including_wrap_and_negative_orientation():
    # A generic four-variable identity, not a branch assignment search.
    form = {'constant':-3,'terms':[[2,0,2,3,0],[-1,3,2,1,0],
        [1,2,0,2,0],[-2,2,2,1,0],[1,1,3,4,0]]}
    for d in range(3):
        selector = {'event':[0,2,d]}
        contracted = contract(form,selector)
        for phases in product(range(3),repeat=4):
            y = indicator(selector['event'],phases)
            assert y*form_value(form,phases) == y*form_value(contracted,phases)


def test_event_probability_against_small_generic_sample_space():
    rng = Random(16102026); mapping = [-1,0,1,2,0]
    for _ in range(30):
        es = [(rng.randrange(5),rng.randrange(5),rng.randrange(4)) for _ in range(2)]
        count = 0
        for values in product(range(3),repeat=3):
            x = [0 if i == -1 else values[i] for i in mapping]
            count += all(indicator(e,x) for e in es)
        assert event_probability(es,mapping,3) == Fraction(count,27)


def test_dipole_factorization_and_distinct_compression_kernel():
    z_minus_one = [a-b for a,b in zip(POW[1],POW[0])]
    for n in range(45):
        first = mul(z_minus_one,POW[-n % 45])
        second = [a-b for a,b in zip(POW[(2*n-1)%45],POW[0])]
        b = local_dipole(n)
        s = red(b)
        assert s == mul(first,second)
        assert (not any(s)) == (n == 23)
        assert (not any(sum(b[t::9]) for t in range(9))) == (n % 9 == 5)


def test_integer_carry_feedback_positive_and_negative():
    for q in range(-15,16):
        for g in range(-12,13):
            for y in (0,1):
                diff = carry_feedback(q,g,y)
                assert diff == ((q+y*g)//3-q//3) % 3
                if g % 3 == 0:
                    assert diff == y*(g//3) % 3
    assert binomial(6,3) % 3 == 2


def test_saved_challenges_remain_distinct_domains():
    a = load('results/event_compression/audit.json')
    rows = {r['masks'][0]:r for r in a['saved_points'] if not r['saved_design_member']}
    assert rows[22487656929184]['nonzero_products'] == 0
    strong = rows[442312790436]
    assert strong['J'] == [1,0,2,2] and strong['in_domain']
    assert strong['equal_cancelling_phases'] and strong['nonzero_products'] == 0
    counter = rows[31210651353580]
    assert counter['J'] == [0,0,1,1] and counter['nonzero_products'] == 36
    outside = rows[22964264347100]
    assert outside['J'] is None and outside['nonzero_products'] == 0
    assert [r['core_nonzero_product_means'] for r in a['saved_design_means']] == [16,14]
    m = a['modular_product_counterexample']
    assert m['Y_G_mod3'] == 0 and m['carry_difference_mod3'] == 2
    # Existing certificate obstructs a global affine combination of degree-4
    # products, not a conditional identity restricted to the full 9O domain.
    cert = load('results/residue_formula/audit.json')['degree_challenge']
    diff = sum((-1)**(6-sum(bits))*v for bits,v in zip(product((0,1),repeat=6),cert['values_lexicographic']))
    assert diff % 3 == 2
