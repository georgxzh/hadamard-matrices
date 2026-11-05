"""Exact integer factorization of the saved counterexample's correlation defect."""
from pathlib import Path
import hashlib
from scripts.phase_moment_obstruction import load,save


def monic_divide(a,b):
    a=a.copy();q=[0]*max(0,len(a)-len(b)+1)
    for i in range(len(a)-len(b),-1,-1):
        q[i]=a[i+len(b)-1]
        for j,c in enumerate(b):a[i+j]-=q[i]*c
    return q,a[:len(b)-1]


def main():
    witness=load('results/phase_moments/refinement_challenge.json')['witness']
    defect=[0]+[(v+2)//12 for v in witness['full_paf_sums']]
    h=[0]*22
    for i in (0,3,6):h[i]-=1;h[i+15]+=1
    q,r=monic_divide(defect,h);assert not any(r) and any(q) and len(q)==24
    for n in (9,15):assert all(sum(defect[i::n])==0 for i in range(n))
    save('defect_factorization.json',{'normalized_defect_coefficients':defect,
         'divisor_coefficients':h,'quotient_coefficients':q,'remainder_coefficients':r,
         'identity':'Delta(z)=12*(z^15-1)*(1+z^3+z^6)*Q(z)',
         'interpretation':'Every nonprimitive 45th-root frequency is correct, whereas every primitive frequency is incorrect; Q is nonzero of degree less than phi(45)=24.',
         'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()})
    print({'quotient_nonzero_terms':[(i,c) for i,c in enumerate(q) if c]})


if __name__=='__main__':main()
