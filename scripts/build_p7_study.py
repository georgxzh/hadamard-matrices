"""Rebuild both unchanged audited small-domain binaries with the pinned flags."""
import json
import os
import subprocess
import time
from scripts.p7_study import ROOT,OUT,NATIVE,EXE,COMPILER,FLAGS,digest,save,provenance
from src.spectral_join import build_native


def main():
    start=time.perf_counter(); command=build_native()
    independent=[str(COMPILER),str(ROOT/'src/full_paf_audit.cpp'),'-o',str(EXE),*FLAGS]
    environment=os.environ.copy(); environment['PATH']=str(COMPILER.parent)+os.pathsep+environment.get('PATH','')
    run=subprocess.run(independent,capture_output=True,text=True,env=environment,timeout=120)
    if run.returncode: raise RuntimeError(run.stderr)
    prior=json.loads((ROOT/'results/spectral_join/independent_audit.json').read_text())
    assert digest(EXE)==prior['binary_sha256'],'independent rebuild differs from audited executable'
    OUT.mkdir(exist_ok=True)
    save(OUT/'build.json',{'commands':[command,independent],'elapsed_seconds':time.perf_counter()-start,
          'native_sha256':digest(NATIVE),'independent_sha256':digest(EXE),**provenance(),
          'limitation':'Byte-identical rebuild with the installed pinned compiler; other toolchains/OS are untested.'})
    print('Both executables match the audited hashes.')


if __name__=='__main__': main()
