"""Record failed simplifications and a precise structural counterexample."""
from scripts.residue_formula import build_model,formula
from scripts.primitive_local_audit import load
from scripts.audit_residue_formula import save
from scripts.audit_fiber_structure import row,compress,paf


def main():
    cat=load('results/p5_branch_portfolio/canonical_branches.json')
    c=cat[278];cs=[c['first'],c['second']];m=build_model(cs)
    records=load('results/primitive_local/audit.json')['cases'][1]['records']
    candidate=next(h for h in records if h['masks']==[31210651353580,20580563788346])
    f=formula(m,candidate['phases'],candidate['norm_defect'])
    assert f['in_domain'] and f['J']==[0,0,1,1] and f['Q'][0]==0
    alt=[compress(row(x,45),9) for x in candidate['masks']]
    sums=[a+b for a,b in zip(*map(paf,alt))]
    assert sums!=[-10]*8
    old=load('results/primitive_local/audit.json')['saved_false_positive']
    outside=formula(m,old['phases'],old['norm_defect'])
    assert not outside['in_domain']
    save('challenges.json',{
        'candidate':'For branch 279, the moments and S in 9O force the constant coordinate J_0 to be nonzero.',
        'outcome':'refuted by an existing allowed third-gauged phase assignment',
        'counterexample':{'masks':candidate['masks'],'phases':candidate['phases'],
            'Q':f['Q'],'J':f['J'],'alternate_paf_sums':sums,
            'qualification':'Does not satisfy the exact length-nine compression PAFs; the strengthened claim remains open structurally.'},
        'failed_early_reduction':{'explanation':'All six Q vectors reduce to zero modulo three, although their quotient residues differ.',
            'examples':[{k:r[k] for k in ('rank','masks','Q','J')} for r in load('results/residue_formula/audit.json')['mod_nine_records']]},
        'out_of_domain_saved_witness':{'masks':old['masks'],'Q':outside['Q'],
            'polynomial_extension':outside['polynomial_extension'],'J':None,
            'explanation':'The polynomial extension is defined here but is not the residue of S/9 in O.'},
        'next_target':'Use the two degree-six coordinates jointly with exact length-nine signed balances to derive a support-dependent identity excluding their common zero. No such identity proved.'})
    print({'candidate_refuted':candidate['masks'],'J':f['J'],'K9':sums,
           'old_outside_extension':outside['polynomial_extension']})


if __name__=='__main__':main()
