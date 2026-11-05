"""Certified rational Fourier bounds; checked wrapper for the native search.

Every trigonometric coefficient has error at most 1/2**20. Coefficients
are generated using Machin's formula and exact alternating rational series.
No floating point calculation decides whether a phase assignment is pruned.
"""
import json
import os
import subprocess
from fractions import Fraction
from functools import lru_cache
from pathlib import Path
from time import perf_counter

from src.legendre import check_legendre_pair,check_negative_support_sds,compress
from src.ternary_phase import TernaryPhasePBModel

ROOT=Path(__file__).resolve().parents[1]
SCALE=1 << 20
NATIVE=ROOT/'tmp/spectral_join.exe'
COMPILER=Path('C:/msys64/ucrt64/bin/g++.exe')
FLAGS=['-std=c++17','-O3','-mpopcnt','-static','-Wl,--no-insert-timestamp','-lpsapi']


def atan_bounds(x):
    terms=[(-1)**j*x**(2*j+1)/(2*j+1) for j in range(32)]
    return sum(terms,Fraction()),sum(terms[:-1],Fraction())


@lru_cache(maxsize=1)
def pi_bounds():
    a,b=atan_bounds(Fraction(1,5)); c,d=atan_bounds(Fraction(1,239))
    # Outward rational rounding reduces coefficient-generation arithmetic cost.
    denominator=10**40
    lo,hi=16*a-4*d,16*b-4*c
    return Fraction((lo*denominator).__floor__(),denominator),Fraction((hi*denominator).__ceil__(),denominator)


def cos_series(x,last):
    value=term=Fraction(1)
    for j in range(1,last+1):
        term *= -x*x/((2*j-1)*(2*j)); value+=term
    return value


@lru_cache(maxsize=1024)
def cos_pi_bounds(q):
    q=abs((q+1)%2-1)
    if q==0: return Fraction(1),Fraction(1)
    if q==1: return Fraction(-1),Fraction(-1)
    if q==Fraction(1,2): return Fraction(),Fraction()
    lo,hi=pi_bounds()
    return cos_series(q*hi,21),cos_series(q*lo,20)


def coefficient(q):
    q=abs((q+1)%2-1)
    lo,hi=cos_pi_bounds(q)
    center=(((lo+hi)*SCALE+1)/2).__floor__()
    assert lo<=hi and Fraction(center-1,SCALE)<=lo<=hi<=Fraction(center+1,SCALE)
    return center


@lru_cache(maxsize=3)
def coefficients(length):
    if length not in (27,45,63): raise ValueError('only validated p=3,5,7 lengths; no p=37')
    frequencies=[f for f in range(1,length//2+1) if f%3]
    cosine=[[coefficient(Fraction(2*f*i,length)) for i in range(length)] for f in frequencies]
    sine=[[coefficient(Fraction(1,2)-Fraction(2*f*i,length)) for i in range(length)] for f in frequencies]
    lo,hi=pi_bounds()
    return {'scale':SCALE,'length':length,'frequencies':frequencies,'cosine':cosine,'sine':sine,
            'coefficient_error_units':1,'pi_lower':str(lo),'pi_upper':str(hi),
            'proof':'Machin 16 atan(1/5)-4 atan(1/239), 32/31-term bounds; cosine alternating partial sums through indices 21/20'}


def build_native():
    NATIVE.parent.mkdir(exist_ok=True)
    command=[str(COMPILER),str(ROOT/'src/spectral_join.cpp'),'-o',str(NATIVE),*FLAGS]
    environment=os.environ.copy()
    environment['PATH']=str(COMPILER.parent)+os.pathsep+environment.get('PATH','')
    run=subprocess.run(command,capture_output=True,text=True,timeout=120,env=environment)
    if run.returncode: raise RuntimeError(f'compiler exit {run.returncode}: {run.stderr}')
    return command


def search(first,second,output,*,mode=2,seconds=120,node_limit=100_000_000,
           stored_candidate_limit=5_000_000,solution_limit=100_000,probe=False):
    start=perf_counter()
    model=TernaryPhasePBModel(first,second); n=model.compressed_length
    if n not in (9,15,21) or mode not in (0,1,2): raise ValueError('unsupported branch or mode')
    if not 0<seconds<=1500: raise ValueError('bounded runs require 0 < seconds <= 1500')
    if not NATIVE.exists(): raise RuntimeError('build_native must be called first')
    output=Path(output); output.parent.mkdir(parents=True,exist_ok=True)
    data=coefficients(3*n); lines=[f'{n} {SCALE} {len(data["frequencies"])}']
    lines += [' '.join(map(str,row)) for row in (first,second)]
    lines += [' '.join(map(str,row)) for key in ('cosine','sine') for row in data[key]]
    lines += [f'{mode} {int(probe)} {seconds} {node_limit} {stored_candidate_limit} {solution_limit}']
    input_path=output.with_suffix('.input.txt'); input_path.write_text('\n'.join(lines)+'\n',encoding='ascii',newline='\n')
    command=[str(NATIVE),str(input_path),str(output)]
    run=subprocess.run(command,capture_output=True,text=True,timeout=seconds+15)
    if run.returncode: raise RuntimeError(run.stderr)
    result=json.loads(output.read_text()); result['command']=command
    for masks in result['solutions']:
        pair=[tuple(1-2*((m >> i)&1) for i in range(3*n)) for m in masks]
        assert tuple(compress(pair[0],n))==tuple(first) and tuple(compress(pair[1],n))==tuple(second)
        assert check_legendre_pair(*pair).ok and check_negative_support_sds(*pair).ok
    result['wrapper_elapsed_seconds']=perf_counter()-start
    output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n',encoding='utf-8',newline='\n')
    return result
