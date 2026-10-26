"""repro_gate.py — reproduction gate: the same pipeline must reproduce a(2)..a(14)
exactly (published b-file values), plus the growth gate at n = 15.

n = 1 is the 1x1 torus (loops); the OEIS DATA value is checked separately by hand.
"""
import os
import numpy as np
import scipy.sparse as sp
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from build_T15 import build_T
from trace_a15 import canonical_orbits

RUN = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))


def a_of(n):
    """a(n) via the pipeline: orbit-reduced trace, modular with CRT (int64-exact for
    n <= 9; CRT over 4-6 primes for larger n — int64 alone overflows from n = 10)."""
    r, c, v = build_T(n)
    dim = 1 << n
    if n <= 9:
        T = sp.csr_matrix((v.astype(np.int64), (r, c)), shape=(dim, dim))
        reps, sizes = canonical_orbits(n)
        tot = 0
        for rep, size in zip(reps, sizes):
            vec = np.zeros(dim, dtype=np.int64)
            vec[rep] = 1
            for _ in range(n):
                vec = np.asarray(vec @ T)
            tot += size * int(vec[rep])
        return tot
    from trace_a15 import trace_orbit_mod
    primes = [2147483629, 2147483587, 2147483579, 2147483563, 2147483549, 2147483423]
    residues = []
    for p in primes:
        T = sp.csr_matrix((v.astype(np.int64) % p, (r, c)), shape=(dim, dim))
        residues.append(trace_orbit_mod(T, *canonical_orbits(n), n, p))
    x, M = 0, 1
    for p, rv in zip(primes, residues):
        t = ((rv - x) * pow(M, -1, p)) % p
        x = x + M * t
        M *= p
    assert M > (1 << 150), "CRT modulus too small for n>=10 values"
    return x


def main():
    published = {}
    for line in open(f"{RUN}/data/b054759.txt"):
        p = line.split()
        if len(p) == 2 and p[0].isdigit():
            published[int(p[0])] = int(p[1])
    print("published b-file keys:", sorted(published))
    ok = True
    for n in sorted(published):
        if n > 14:
            continue
        v = a_of(n)
        match = v == published[n]
        ok &= match
        print(f"n={n}: pipeline {v} vs published {published[n]} {'OK' if match else 'MISMATCH'}",
              flush=True)
    # growth gate
    a15 = 4310182149988584261406143524214457416387448
    g15 = float(a15 ** (1 / 225))
    a14 = published[14]
    g14 = float(a14 ** (1 / 196))
    print(f"growth: a(15)^(1/225) = {g15:.7f}; a(14)^(1/196) = {g14:.7f}; "
          f"|diff| = {abs(g15 - g14):.2e}")
    print("REPRO_GATE:", "PASS" if ok else "FAIL")


if __name__ == "__main__":
    main()
