#!/usr/bin/env python
"""Standalone checker for the packaged a(15) claim. Python 3.8+, standard library only.

Verifies: (1) the object file holds exactly the claimed integer; (2) the pure-stdlib
exact big-integer trace of the transfer matrix (built from the definition via the
alternating-flip characterization) reproduces the published a(2)..a(11) — the "one exact
big-integer run" arm of the two-run rule; (3) the object matches the integer carried in
INDEX.csv.

Run from the package folder:  python verify-it-yourself/check.py
Last line: PASS or FAIL.
"""
import hashlib
import sys

CLAIMED = 4310182149988584261406143524214457416387448
OBJECT = "object/a15_value.txt"
OBJECT_SHA = "fd616054f7567327589dd9720fd91599613b6a0285484f1c49587a63651f484c"

PUB = {2: 18, 3: 148, 4: 2970, 5: 143224, 6: 16448400, 7: 4484823396,
       8: 2901094068042, 9: 4448410550095612, 10: 16178049740086515288,
       11: 139402641051212392498528}
GATE_MAX_N = 11  # time-capped: n=12 exceeds the claim-folder budget


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
    raw = open(OBJECT, "rb").read().replace(b"\r\n", b"\n")
    h = hashlib.sha256(raw).hexdigest()
    if h != OBJECT_SHA:
        print(f"FAIL: {OBJECT} sha256 mismatch")
        return 1
    val = int(raw.decode().strip())
    print(f"object sha256 ok; integer = {val}")
    if val != CLAIMED:
        print("FAIL: integer differs from the claim")
        return 1
    ok = True
    for n in sorted(PUB):
        if n > GATE_MAX_N:
            continue
        v = a_of(n)
        good = v == PUB[n]
        print(f"published gate n={n}: {v} vs {PUB[n]} {'OK' if good else 'FAIL'}")
        ok = ok and good
    # INDEX.csv consistency
    idx = open("INDEX.csv").read()
    if str(CLAIMED) not in idx:
        print("FAIL: INDEX.csv does not carry the claimed integer")
        ok = False
    else:
        print("INDEX.csv carries the claimed integer: OK")
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
