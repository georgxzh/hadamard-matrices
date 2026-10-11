"""Derive conditional branch/class incidence from frozen solutions; no search."""
from collections import Counter, defaultdict
from scripts.publication_gap_replication import ROOT, OUT, load, save, sha

def main():
    source='results/phase_propagation/equivalence_crosswalk.json'
    classes=load(source)['classes']; census=load('results/p5_classification/classification.json')
    by_branch=defaultdict(Counter); records=[]
    for index,c in enumerate(classes,1):
        counts=Counter(m['rank'] for m in c['members'])
        for rank,count in counts.items(): by_branch[rank][index]=count
        records.append({'class_id':index,'canonical_masks':c['representative_masks'],
                        'branch_multiplicities':dict(sorted(counts.items())),
                        'phase_gauged_members':sum(counts.values()),
                        'prescribed_ordered_members':81*sum(counts.values())})
    for c in census: assert sum(by_branch[c['rank']].values())==len(c['solutions'])
    branches=[{'rank':c['rank'],'class_multiplicities':dict(sorted(by_branch[c['rank']].items()))} for c in census]
    result={'classes':records,'branches':branches,
            'classes_per_branch_histogram':dict(Counter(len(by_branch[c['rank']]) for c in census)),
            'branches_per_class_histogram':dict(Counter(len(c['branch_multiplicities']) for c in records)),
            'nonzero_incidence_entries':sum(len(c['class_multiplicities']) for c in branches),
            'branch_class_multiplicity_histogram':dict(Counter(v for c in branches for v in c['class_multiplicities'].values())),
            'source_sha256':sha(ROOT/source), 'script_sha256':sha(__file__),
            'historical_crosswalk_status':'Unavailable historical list; class IDs are local canonical-mask order only.',
            'interpretation':'Counts refine the fixed-prescription fibers. They are derivable from a complete global representative list plus orbit expansion; no logically new existence result or priority claim.'}
    save(OUT/'conditional_incidence.json',result)
    print({k:v for k,v in result.items() if k not in ('classes','branches')})

if __name__=='__main__': main()
