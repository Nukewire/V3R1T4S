#!/usr/bin/env python
"""Standalone stdlib verification of the a(15) claim's reproduction gate.

From the definition (Eulerian orientations of the n x n torus: every edge directed, 2
arrows in and 2 out at each vertex), builds the transfer matrix T over 2^n vertical-arrow
states via the alternating-flip characterization (derived and brute-force-verified in run
2026-10-25-0731: T[s,s'] = 2 if s == s'; 1 iff the set bits of s^s' form an even cyclic
sequence on which s's bits alternate; else 0), and checks a(2)..a(12) against the
published b-file copied beside this file. Pure standard library.

Usage: python verify_standalone.py    (last line PASS or FAIL; ~2 minutes)
"""
import sys

PUB = {2: 18, 3: 148, 4: 2970, 5: 143224, 6: 16448400, 7: 4484823396,
       8: 2901094068042, 9: 4448410550095612, 10: 16178049740086515288,
       11: 139402641051212392498528, 12: 2849295959501939989625992464}


def build_partners(s, n):
    pos1 = [i for i in range(n) if (s >> i) & 1]
    pos0 = [i for i in range(n) if not ((s >> i) & 1)]
    succ = {p: [q for q in pos0 if q > p] for p in pos1}
    for p in pos0:
        succ[p] = [q for q in pos1 if q > p]
    partners = [s]
    stack = [(p, (s >> p) & 1, 1, 1 << p) for p in range(n)]
    while stack:
        pos, fbit, cnt, x = stack.pop()
        if cnt >= 2 and cnt % 2 == 0 and ((s >> pos) & 1) != fbit:
            partners.append(s ^ x)
        for q in succ[pos]:
            stack.append((q, fbit, cnt + 1, x | (1 << q)))
    return partners


def a_of(n):
    size = 1 << n
    rows = [(build_partners(s, n), s) for s in range(size)]
    # trace of T^n by exact integer vector iteration from each state
    # (T[s,s] = 2 for the x=0 partner; 1 otherwise)
    total = 0
    for s0 in range(size):
        v = {s0: 1}
        for _ in range(n):
            nv = {}
            for s, c in v.items():
                partners, self_s = rows[s]
                for sp in partners:
                    w = 2 if sp == self_s else 1
                    nv[sp] = nv.get(sp, 0) + c * w
            v = nv
        total += v.get(s0, 0)
    return total


def main():
    ok = True
    for n in sorted(PUB):
        val = a_of(n)
        good = val == PUB[n]
        print(f"n={n}: {val} vs published {PUB[n]} {'OK' if good else 'FAIL'}", flush=True)
        ok = ok and good
    try:
        crt_check()
    except AssertionError as e:
        print(f"OBJECT CHECK FAILED: {e}")
        print("FAIL")
        return 1
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


def is_prime_int(m):
    if m < 2:
        return False
    d = 2
    while d * d <= m:
        if m % d == 0:
            return False
        d += 1
    return True


def crt_check():
    """The object itself: a15_value.txt must equal the CRT reconstruction of BOTH run
    records (disjoint, all-prime moduli). Fails if the object file is corrupted."""
    import json
    import os
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "..", "object", "a15_value.txt")) as f:
        a15 = int(f.read().strip())
    seen = set()
    for name in ("runA_crt.json", "runB_crt.json"):
        with open(os.path.join(here, "..", "object", name)) as f:
            rec = json.load(f)
        primes, residues = rec["primes"], rec["residues"]
        assert len(primes) == len(residues)
        for p in primes:
            assert is_prime_int(p), f"{name}: modulus {p} is not prime"
            assert p not in seen, f"modulus {p} shared between runs"
            seen.add(p)
        x, M = 0, 1
        for p, r in zip(primes, residues):
            t = ((r - x) * pow(M, -1, p)) % p
            x += M * t
            M *= p
        assert 0 <= x < M
        print(f"{name}: CRT over {len(primes)} primes ({M.bit_length()} bits) = {x}")
        assert x == rec["crt_result"], f"{name}: CRT mismatch vs record"
        assert x == a15, f"{name}: reconstruction != object a15_value.txt"
    print(f"object check: a(15) = {a15} confirmed by both independent CRT records OK")
    return True


if __name__ == "__main__":
    sys.exit(main())
