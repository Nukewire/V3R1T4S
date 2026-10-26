"""trace_a15.py — Run A: Tr(T^15) for A054759 via rotation-orbit reduction, mod p, CRT.

Orbit fact: T[rot_k(s), rot_k(s')] = T[s,s'] (bit-rotation invariance), so diagonal
entries of T^15 are constant on rotation orbits; Tr = sum over orbit representatives of
orbit_size * (T^15)[rep, rep]. Validated at n = 3, 4 against 148, 2970 before n = 15.

Usage: python trace_a15.py            (runs validation then the 6-prime n=15 CRT)
"""
import os
import numpy as np
import scipy.sparse as sp
from math import gcd

HERE = os.path.dirname(os.path.abspath(__file__))
RUN = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))


def canonical_orbits(n):
    """Return (reps, sizes): canonical representative and orbit size for each rotation
    orbit of n-bit strings."""
    dim = 1 << n
    parent = list(range(dim))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    rep_of = {}
    for s in range(dim):
        best = s
        cur = s
        for _ in range(n):
            cur = ((cur << 1) | (cur >> (n - 1))) & (dim - 1)
            best = min(best, cur)
        rep_of.setdefault(best, []).append(s)
    reps = sorted(rep_of)
    sizes = [len(v) for v in (rep_of[r] for r in reps)]
    return reps, sizes


def trace_orbit_mod(T, reps, sizes, n, mod):
    """Tr(T^n) mod p via orbit representatives (chunked dense propagation)."""
    dim = 1 << n
    total = 0
    idx = {r: i for i, r in enumerate(reps)}
    CH = 256
    for start in range(0, len(reps), CH):
        chunk = reps[start:start + CH]
        V = np.zeros((len(chunk), dim), dtype=np.int64)
        V[np.arange(len(chunk)), np.array(chunk)] = 1
        for _ in range(n):
            V = np.asarray(V @ T) % mod
        diag = V[np.arange(len(chunk)), np.array(chunk)]
        w = np.array(sizes[start:start + CH], dtype=np.int64)
        total = (total + int((diag % mod * (w % mod) % mod).sum())) % mod
    return total % mod


def build_csr(n):
    data = np.load(os.path.join(HERE, "..", "output", "T15_sparse.npz")) if n == 15 else None
    if data is not None:
        r, c, v = data["rows"], data["cols"], data["vals"]
    else:
        import build_T15
        r, c, v = build_T15.build_T(n)
    return r, c, v


def main():
    from build_T15 import build_T
    # validation at n = 3, 4 (exact, small)
    for n, expect in ((3, 148), (4, 2970)):
        r, c, v = build_T(n)
        dim = 1 << n
        T = sp.csr_matrix((v.astype(np.int64), (r, c)), shape=(dim, dim))
        reps, sizes = canonical_orbits(n)
        # exact trace via orbits (int64 is exact at these sizes)
        tot = 0
        for rep, size in zip(reps, sizes):
            vec = np.zeros(dim, dtype=np.int64)
            vec[rep] = 1
            for _ in range(n):
                vec = np.asarray(vec @ T)
            tot += size * int(vec[rep])
        print(f"n={n} orbit-trace = {tot} (expect {expect}) {'OK' if tot == expect else 'FAIL'}",
              flush=True)

    # n = 15, modular
    data = np.load(os.path.join(HERE, "..", "output", "T15_sparse.npz"))
    r15, c15, v15 = data["rows"], data["cols"], data["vals"]
    reps, sizes = canonical_orbits(15)
    print(f"n=15: {len(reps)} rotation orbits (sum sizes {sum(sizes)})", flush=True)
    primes = [2147483629, 2147483587, 2147483579, 2147483563, 2147483549, 2147483423]
    residues = []
    for p in primes:
        T = sp.csr_matrix((v15.astype(np.int64) % p, (r15, c15)), shape=(32768, 32768))
        import time
        t0 = time.time()
        val = trace_orbit_mod(T, reps, sizes, 15, p)
        residues.append(val)
        print(f"  mod {p}: {val}  [{time.time()-t0:.0f}s]", flush=True)
    # CRT
    from functools import reduce
    Ms = primes
    Rs = residues
    x, M = 0, 1
    for p, rv in zip(Ms, Rs):
        # solve x' = x mod M, x' = rv mod p
        t = ((rv - x) * pow(M, -1, p)) % p
        x = x + M * t
        M *= p
    print(f"RUN A RESULT: a(15) = {x}", flush=True)
    print(f"modulus product bits: {M.bit_length()}")


if __name__ == "__main__":
    main()
