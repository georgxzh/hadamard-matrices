"""Exact finite-domain search on ternary differences and weighted PAF sums.

The anchor phase of each row is zero; edge (0,j) is therefore phase j.
All active-active edges are present. Triangle relations retain cross terms
and ensure globally realizable differences. Bounds are only necessary tests;
complete assignments are independently checked by full binary PAF and SDS.
"""
from collections import deque
from bisect import bisect_left, bisect_right
from itertools import combinations
from time import perf_counter

from src.legendre import check_legendre_pair, check_negative_support_sds
from src.ternary_phase import TernaryPhasePBModel


VALUES = tuple(tuple(v for v in range(3) if mask & (1 << v)) for mask in range(8))


def triangle_support(x, y, z):
    """Supported values for x+y=z (mod 3), independently tabulated."""
    a=b=c=0
    for u in VALUES[x]:
        for v in VALUES[y]:
            w=(u+v)%3
            if z & (1 << w):
                a |= 1 << u; b |= 1 << v; c |= 1 << w
    return a,b,c


TRIANGLE = tuple(triangle_support(x,y,z) for x in range(8) for y in range(8) for z in range(8))


class PhasePropagationModel:
    def __init__(self, first, second, *, cycle_mode='all', paf_bounds=True):
        if cycle_mode not in ('all','anchor'):
            raise ValueError('cycle_mode must be all or anchor')
        checked=TernaryPhasePBModel(first,second)
        self.rows=checked.rows
        self.n=checked.compressed_length
        self.edges=[]; lookup={}; self.anchors=[]; self.anchor_rows=[]
        for row,source in enumerate(self.rows):
            anchors=[]
            for u,v in combinations(range(len(source.active)),2):
                edge=len(self.edges); self.edges.append((row,u,v)); lookup[row,u,v]=edge
                if u==0: anchors.append(edge)
            self.anchors.extend(anchors); self.anchor_rows.append(anchors)
        self.triangles=[]
        for row,source in enumerate(self.rows):
            for u,v,w in combinations(range(len(source.active)),3):
                if cycle_mode=='anchor' and u!=0: continue
                self.triangles.append((lookup[row,u,v],lookup[row,v,w],lookup[row,u,w]))
        self.sums=[]
        for shift in range(1,self.n):
            constant=0; tables={}
            for row,source in enumerate(self.rows):
                offset,terms=source.paf_terms(shift); constant+=offset
                for u,v,h,weight in terms:
                    assert weight%4==0
                    tables.setdefault(lookup[row,u,v],[0,0,0])[h]+=weight//4
            assert (-2-constant)%4==0
            terms=[]
            for edge,weights in sorted(tables.items()):
                limits=[None]+[(min(weights[h] for h in VALUES[d]),max(weights[h] for h in VALUES[d])) for d in range(1,8)]
                terms.append((edge,tuple(weights),limits))
            self.sums.append(((-2-constant)//4,terms))
        self.paf_bounds=paf_bounds
        self.incidence=[[] for _ in self.edges]
        for index,triangle in enumerate(self.triangles):
            for edge in triangle: self.incidence[edge].append(index)
        for index,(_,terms) in enumerate(self.sums,len(self.triangles)):
            for edge,_,_ in terms: self.incidence[edge].append(index)
        self.cycle_mode=cycle_mode

    def propagate(self, domains, *, stats=None, deadline=float('inf'), initial=None):
        """Monotone sound contraction; False means a proved local conflict."""
        count=len(self.triangles)+len(self.sums)
        queue=deque(range(count) if initial is None else initial)
        queued=set(queue)
        steps=0
        while queue:
            steps+=1
            if steps%128==0 and perf_counter()>=deadline: raise TimeoutError
            constraint=queue.popleft(); queued.remove(constraint)
            if stats is not None: stats['propagator_calls']+=1
            if constraint<len(self.triangles):
                edges=self.triangles[constraint]
                a,b,c=(domains[e] for e in edges)
                supports=TRIANGLE[(a*8+b)*8+c]
                if not all(supports): return False
                changes=zip(edges,supports)
                kind='cycle_deletions'
            else:
                if not self.paf_bounds: continue
                target,terms=self.sums[constraint-len(self.triangles)]
                bounds=[limits[domains[edge]] for edge,_,limits in terms]
                lo=sum(b[0] for b in bounds); hi=sum(b[1] for b in bounds)
                if target<lo or target>hi: return False
                updates=[]
                for (edge,weights,_),(low,high) in zip(terms,bounds):
                    supported=sum(1 << h for h in VALUES[domains[edge]]
                                  if lo-low <= target-weights[h] <= hi-high)
                    if not supported: return False
                    updates.append((edge,supported))
                changes=updates; kind='paf_deletions'
            for edge,new in changes:
                old=domains[edge]
                if new==old: continue
                assert new & old == new
                domains[edge]=new
                if stats is not None: stats[kind]+=old.bit_count()-new.bit_count()
                for affected in self.incidence[edge]:
                    if affected not in queued: queued.add(affected); queue.append(affected)
        return True

    def solution(self, domains):
        phases=[]
        for anchors,source in zip(self.anchor_rows,self.rows):
            a=(0,)+tuple(VALUES[domains[edge]][0] for edge in anchors) if source.active else ()
            phases.append(a)
        pair=tuple(row.decode(a) for row,a in zip(self.rows,phases))
        if not check_legendre_pair(*pair).ok or not check_negative_support_sds(*pair).ok:
            raise AssertionError('propagation leaf failed independent full PAF/SDS')
        return tuple(sum(1 << i for i,v in enumerate(row) if v==-1) for row in pair)

    def search(self, *, seconds=10, max_nodes=1_000_000):
        if not 0 < seconds <= 120 or max_nodes<1:
            raise ValueError('search requires 0 < seconds <= 120 and a positive node cap')
        start=perf_counter(); deadline=start+seconds
        stats={'nodes':0,'conflicts':0,'propagator_calls':0,'cycle_deletions':0,'paf_deletions':0}
        solutions=[]; complete=True; stop='exhausted'
        root=[7]*len(self.edges)
        def visit(domains,initial=None):
            if perf_counter()>=deadline: raise TimeoutError
            if stats['nodes']>=max_nodes: raise OverflowError
            stats['nodes']+=1
            if not self.propagate(domains,stats=stats,deadline=deadline,initial=initial):
                stats['conflicts']+=1; return
            choices=[e for e in self.anchors if domains[e].bit_count()>1]
            if not choices:
                # With bounds disabled this is a reference exhaustive traversal.
                if not self.paf_bounds:
                    for target,terms in self.sums:
                        if sum(weights[VALUES[domains[e]][0]] for e,weights,_ in terms)!=target: return
                solutions.append(self.solution(domains)); return
            edge=min(choices,key=lambda e:(domains[e].bit_count(),-len(self.incidence[e]),e))
            for value in VALUES[domains[edge]]:
                child=domains.copy(); child[edge]=1 << value
                visit(child,self.incidence[edge])
        try: visit(root)
        except TimeoutError: complete=False; stop='time_limit'
        except OverflowError: complete=False; stop='node_limit'
        assert len(solutions)==len(set(solutions))
        count=len(solutions)
        return {'complete':complete,'stop_reason':stop,'elapsed_seconds':perf_counter()-start,
                'canonical_pairs':count if complete else None,'ordered_pairs':9*count if complete else None,
                'canonical_lower_bound':count,'solutions':sorted(solutions),'stats':stats,
                'cycle_mode':self.cycle_mode,'paf_bounds':self.paf_bounds,
                'variables':len(self.edges),'triangles':len(self.triangles),'paf_equations':len(self.sums),
                'seconds_limit':seconds,'node_limit':max_nodes}


def search_conditioned(first, second, *, seconds=60, max_stored_candidates=250_000,
                       max_nodes=5_000_000, partner_filter=True, folded_bounds=True):
    """Propagate exact partner-signature support through partial phase rows.

Enumerate the smaller row once; retain every phase multiplicity. In the
other row every phase assignment enforces cycle consistency by construction.
All unresolved incident edges remain in rigorous interval bounds. Integer
bitsets retain precisely those partner signatures compatible with all bounds.
This is an exact row decomposition, not a separation within a complete graph.
"""
    if not 0 < seconds <= 120 or max_stored_candidates<1 or max_nodes<1:
        raise ValueError('positive caps and at most 120 seconds required')
    start=perf_counter(); deadline=start+seconds
    rows=TernaryPhasePBModel(first,second).rows
    stored=min(range(2),key=lambda r:rows[r].canonical_count); other=1-stored
    n=rows[0].length
    table={}; stored_count=0; solutions=[]
    stats={'nodes':0,'pruned':0,'leaves':0,'stored_candidates':0,'distinct_signatures':0}
    complete=True; stop='exhausted'
    def finish():
        count=len(solutions)
        return {'complete':complete,'stop_reason':stop,'elapsed_seconds':perf_counter()-start,
                'canonical_pairs':count if complete else None,'ordered_pairs':9*count if complete else None,
                'canonical_lower_bound':count,'solutions':sorted(solutions),'stats':stats,
                'stored_side':stored,'partner_filter':partner_filter,'folded_bounds':folded_bounds,
                'seconds_limit':seconds,'stored_candidate_limit':max_stored_candidates,'node_limit':max_nodes}
    for phases,key in rows[stored].iter_projected_signatures():
        if stored_count>=max_stored_candidates or perf_counter()>=deadline:
            complete=False; stop='stored_candidate_limit' if stored_count>=max_stored_candidates else 'time_limit'
            return finish()
        table.setdefault(key,[]).append(phases)
        stored_count+=1; stats['stored_candidates']=stored_count
    stats['distinct_signatures']=len(table)
    keys=list(table)
    feature_count=n-1+(n//2 if folded_bounds else 0)
    def features(signature):
        return tuple(signature)+(tuple(signature[s-1]+signature[n-s-1] for s in range(1,n//2+1)) if folded_bounds else ())
    targets=[tuple((-2 if j<n-1 else -4)-v for j,v in enumerate(features(key))) for key in keys]
    minimum=[min(t[j] for t in targets) for j in range(feature_count)]
    maximum=[max(t[j] for t in targets) for j in range(feature_count)]
    # Prefix bitsets indexed by the exact possible value of each feature.
    indexes=[]
    if partner_filter:
        size=(len(keys)+7)//8
        for j in range(feature_count):
            buckets={}
            for index,target in enumerate(targets):
                value=target[j]
                if value not in buckets: buckets[value]=bytearray(size)
                buckets[value][index//8] |= 1 << (index%8)
            values=sorted(buckets); prefixes=[0]; mask=0
            for value in values:
                mask |= int.from_bytes(buckets[value],'little'); prefixes.append(mask)
            indexes.append((values,prefixes))
            if perf_counter()>=deadline:
                complete=False; stop='time_limit'; return finish()
    del targets
    row=rows[other]; k=len(row.active)
    base=[row.paf_terms(s)[0] for s in range(1,n)]
    low=list(features(base)); high=low.copy()
    edges={}
    for u,v in combinations(range(k),2):
        r=row.active[v]-row.active[u]; w=row.delta[row.active[u]]*row.delta[row.active[v]]
        positions=(r-1,n-r-1)
        if folded_bounds: positions+=(n-1+min(r,n-r)-1,)
        edges[u,v]=(positions,w,min(0,w),max(0,w))
        for j in positions: low[j]+=min(0,w); high[j]+=max(0,w)
    # Assign anchor first; deterministic farthest-residue order spreads bounds.
    order=[0]; remaining=set(range(1,k))
    while remaining:
        selected=max(remaining,key=lambda v:(len({j for u in order for j in edges[min(u,v),max(u,v)][0]}),-v))
        order.append(selected); remaining.remove(selected)
    phases=[0]*k
    # Precompute changes for each newly assigned vertex and predecessor phase.
    transitions=[]
    for depth,v in enumerate(order[1:],1):
        prior=[]
        for u in order[:depth]:
            left,right=sorted((u,v)); positions,w,lo,hi=edges[left,right]
            deltas=[]
            for difference in range(3):
                contribution=(w if difference==0 else 0,w if difference==2 else 0)
                if folded_bounds: contribution+=(w if difference!=1 else 0,)
                deltas.append(tuple((j,actual-lo,actual-hi) for j,actual in zip(positions,contribution)))
            prior.append((u,u==left,deltas))
        transitions.append(prior)
    all_partners=(1 << len(keys))-1
    def visit(depth,lo,hi,support):
        if perf_counter()>=deadline: raise TimeoutError
        if stats['nodes']>=max_nodes: raise OverflowError
        stats['nodes']+=1
        for j in range(feature_count):
            if hi[j]<minimum[j] or lo[j]>maximum[j]: stats['pruned']+=1; return
            if partner_filter:
                values,prefix=indexes[j]
                support &= prefix[bisect_right(values,hi[j])] ^ prefix[bisect_left(values,lo[j])]
                if not support: stats['pruned']+=1; return
        if depth==len(order):
            stats['leaves']+=1
            key=tuple(-2-value for value in lo[:n-1])
            for partner in table.get(key,()):
                assignments=[None,None]; assignments[stored]=partner; assignments[other]=tuple(phases)
                pair=tuple(source.decode(a) for source,a in zip(rows,assignments))
                if not check_legendre_pair(*pair).ok or not check_negative_support_sds(*pair).ok:
                    raise AssertionError('conditioned leaf failed full PAF/SDS')
                solutions.append(tuple(sum(1 << i for i,v in enumerate(x) if v==-1) for x in pair))
            return
        v=order[depth]
        for phase in range(3):
            phases[v]=phase; lower=lo.copy(); upper=hi.copy()
            for u,forward,deltas in transitions[depth-1]:
                difference=(phase-phases[u] if forward else phases[u]-phase)%3
                for j,dl,dh in deltas[difference]: lower[j]+=dl; upper[j]+=dh
            visit(depth+1,lower,upper,support)
    try: visit(1,low,high,all_partners)
    except TimeoutError: complete=False; stop='time_limit'
    except OverflowError: complete=False; stop='node_limit'
    assert len(solutions)==len(set(solutions))
    return finish()
