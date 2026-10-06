"""Supplement prefix probes with bounded real-key joins before portfolio trials."""
import json
import time
from scripts.p7_study import OUT,branches,provenance,search,digest,save,ROOT


def main():
    start=time.perf_counter(); records=[]
    for branch in branches():
        for mode in (0,1,2):
            result=search(*branch['pair'],OUT/'pilot'/f"join_{branch['id']}_m{mode}.json",mode=mode,
                           seconds=5,node_limit=1_000_000,stored_candidate_limit=250_000,solution_limit=1000)
            # Actual key generation, spectral tests and (where reached) partner lookups.
            # Use worst observed node cost for both full unpruned trees, with 10x margin.
            costs=[r['elapsed_seconds']/max(1,r['nodes']) for r in result['rows'] if r['nodes']]
            estimate=10*max(costs)*sum((3*v-1)//2 for v in branch['row_domains'])
            records.append({'id':branch['id'],'mode':mode,'expected_seconds_10x':estimate,
                            'stop_reason':result['stop_reason'],'result_file':f"pilot/join_{branch['id']}_m{mode}.json"})
    pilot=json.loads((OUT/'pilot.json').read_text())
    save(OUT/'join_pilot.json',{'records':records,'elapsed_seconds':time.perf_counter()-start,
         'memory_envelope_bytes':pilot['memory_envelope_bytes'],'expected_storage_bytes':30_000_000,
         'conservative_storage_envelope_bytes':1_000_000_000,'trial_seconds_cap':80,
         'worst_trial_batch_engine_seconds':80*3*len(branches()),'workers':1,
         'source_sha256':digest(ROOT/'scripts/p7_join_pilot.py'),**provenance(),
         'limitation':'Prefix-only probes omit joins and underestimate the native-off cost. Real-key pilot also samples early prefixes and may omit streaming; estimates are empirical. Hard trials remain scheduled under equal caps regardless of estimate.'})
    print(json.loads((OUT/'join_pilot.json').read_text()),flush=True)


if __name__=='__main__': main()
