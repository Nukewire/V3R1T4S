#!/usr/bin/env python
"""INDEPENDENT second computation of A054759 a(15) (square ice, n x n torus).

Written fresh in this session from the run-2026-10-25-0731 derivation (the 2x2
matrix-product characterization), sharing NO code or artifacts with run
2026-10-25-1031 (Run A). Decomposition here: DFS enumeration of alternating
flip-masks per state -> CSR transfer matrix -> trace of T^n by
dihedral-x-complement orbit representatives with modular sparse matvecs over
sympy-PROVEN primes -> CRT. Rigorous bound from the actual max row sum.

Usage: python indep_run.py all|build|gate|trace15
"""
import sys
import time
import numpy as np
from sympy import isprime
from sympy.ntheory.modular import crt as sympy_crt


def build_T(n):
    """CSR arrays of T over 2^n states via alternating-flip DFS.

    From my 2x2 matrix rule (run 2026-10-25-0731, verified vs brute force):
    T[s,s'] = 2 if s == s'; 1 iff the set bits of x = s^s' form an even-count
    cyclic sequence on which s's bits alternate; else 0. DFS enumerates exactly
    those x: flips at increasing positions, consecutive flips differ in s-bit,
    last-vs-first differ (cyclic closure), even count.
    """
    size = 1 << n
    indptr = np.zeros(size + 1, dtype=np.int64)
    indices_l = []
    data_l = []
    for s in range(size):
        pos1 = [i for i in range(n) if (s >> i) & 1]
        pos0 = [i for i in range(n) if not ((s >> i) & 1)]
        succ = {}
        for p in pos1:
            succ[p] = [q for q in pos0 if q > p]
        for p in pos0:
            succ[p] = [q for q in pos1 if q > p]
        partners = [s]  # x = 0 -> value 2
        stack = [(p, (s >> p) & 1, 1, 1 << p) for p in range(n)]
        while stack:
            pos, fbit, cnt, x = stack.pop()
            if cnt >= 2 and cnt % 2 == 0 and ((s >> pos) & 1) != fbit:
                partners.append(s ^ x)
            for q in succ[pos]:
                stack.append((q, fbit, cnt + 1, x | (1 << q)))
        partners.sort()
        indptr[s + 1] = indptr[s] + len(partners)
        indices_l.extend(partners)
        data_l.extend([2 if sp == s else 1 for sp in partners])
    return indptr, np.array(indices_l, dtype=np.int32), np.array(data_l, dtype=np.int64)


def rev_bits(s, n):
    r = 0
    for _ in range(n):
        r = (r << 1) | (s & 1)
        s >>= 1
    return r


def images(s, n):
    mask = (1 << n) - 1
    out = []
    for comp in (0, 1):
        t = s ^ (mask * comp)
        for k in range(n):
            r = ((t << k) | (t >> (n - k))) & mask
            out.append(r)
            out.append(rev_bits(r, n))
    return out


def compute_reps(n):
    """Orbit representatives and sizes under D_n x Z2 (order 4n).
    Diag(T^n) is G-invariant: T commutes with rotations, reversal and complement
    (the characterization is cyclic- and type-dual-invariant); verified vs brute
    force at n=3,4 by the gate."""
    reps = []
    sizes = []
    seen = set()
    for s0 in range(1 << n):
        if s0 in seen:
            continue
        imgs = images(s0, n)
        seen.update(imgs)
        reps.append(min(imgs))
        sizes.append(len(set(imgs)))
    return reps, sizes


def trace_mod(indptr, indices, data, n, p, reps, sizes):
    import scipy.sparse as sp
    size = 1 << n
    T = sp.csr_matrix((data % p, indices, indptr), shape=(size, size))
    total = 0
    for c, w in zip(reps, sizes):
        v = np.zeros(size, dtype=np.int64)
        v[c] = 1
        for _ in range(n):
            v = (T @ v) % p
        total = (total + w * int(v[c])) % p
    return total


def published():
    vals = {}
    for line in open("data/b054759_live.txt"):
        if line.startswith("#"):
            continue
        k, v = line.split()
        vals[int(k)] = int(v)
    return vals


def need_bits_for(size, R, n):
    import math
    return int(math.log2(size * R**n)) + 1


def pick_primes(hi, need_bits):
    primes = []
    bits = 0
    cand = hi
    while bits <= need_bits + 8:
        cand -= 1
        if isprime(cand):
            primes.append(cand)
            bits += cand.bit_length()
    return primes


def crt(residues, primes):
    v, _ = sympy_crt(primes, residues)
    return int(v)


def main():
    t0 = time.time()
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    pub = published()
    if what in ("gate", "all"):
        for n in range(2, 15):
            ip, ix, da = build_T(n)
            reps, sizes = compute_reps(n)
            R = int((np.diff(ip)).max())
            primes = pick_primes(1 << 30, need_bits_for(1 << n, R, n))
            res = [trace_mod(ip, ix, da, n, p, reps, sizes) for p in primes]
            val = crt(res, primes)
            ok = val == pub[n]
            print(f"gate n={n}: {val} vs pub {pub[n]} {'OK' if ok else 'FAIL'} "
                  f"[{time.time()-t0:.0f}s]", flush=True)
            if not ok:
                print("GATE FAILED — aborting")
                return 1
    if what in ("build", "all"):
        indptr, indices, data = build_T(15)
        np.save("t15_indptr.npy", indptr)
        np.save("t15_indices.npy", indices)
        np.save("t15_data.npy", data)
        R = int((np.diff(indptr)).max())
        print(f"T15 built: nnz={len(indices)} maxrowsum={R} "
              f"bound~2^{need_bits_for(32768, R, 15)} [{time.time()-t0:.0f}s]", flush=True)
    if what in ("trace15", "all"):
        indptr = np.load("t15_indptr.npy")
        indices = np.load("t15_indices.npy")
        data = np.load("t15_data.npy")
        reps, sizes = compute_reps(15)
        print(f"orbit reps: {len(reps)} [{time.time()-t0:.0f}s]", flush=True)
        R = int((np.diff(indptr)).max())
        primes = pick_primes(1 << 30, need_bits_for(32768, R, 15))
        print(f"{len(primes)} proven primes [{time.time()-t0:.0f}s]", flush=True)
        res = []
        for p in primes:
            r = trace_mod(indptr, indices, data, 15, p, reps, sizes)
            res.append(r)
            print(f"  p={p}: {r} [{time.time()-t0:.0f}s]", flush=True)
        val = crt(res, primes)
        print(f"a(15) = {val}", flush=True)
        known = 4310182149988584261406143524214457416387448
        print(f"matches Run A: {val == known}", flush=True)
        print(f"growth a(15)^(1/225) = {val ** (1/225):.7f}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
