# Reproduction scripts

Each research experiment will receive a deterministic entry point here with
its configuration, seed, resource estimate, and expected output hashes.

`reproduce_h428.py` deterministically reconstructs the published order-428
matrix from source sequences, checks every intermediate exact invariant, and
runs both final matrix verifiers. Invoke it from the repository root:

```powershell
python -m scripts.reproduce_h428
```

No open-search scripts are present yet.
