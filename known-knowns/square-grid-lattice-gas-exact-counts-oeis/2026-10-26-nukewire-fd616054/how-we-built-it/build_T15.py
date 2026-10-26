"""build_T15.py — class-DP construction of the A054759 row-transfer matrix at n = 15.

T[s, s'] = Tr(prod_c M(s_c, s'_c)) with M(0,0)=M(1,1)=I, M(1,0)=S+=|1><0|, M(0,1)=S-=|0><1|.
Semigroup classes: 0:I, 1:S+, 2:S-, 3:P0=S-S+=|0><0|, 4:P1=S+S-=|1><1|, 5:DEAD.
Final value: I->2 (trace of I), P0->1, P1->1, S+/S-/DEAD->0.
Diagonal s=s' gives I -> 2 (matches the verified characterization).

Also validates small n against brute force (n=3,4) before the n=15 build.
Output: sparse triplets saved to output/T15_sparse.npz (int32 rows/cols, int8 vals).
"""
import numpy as np
import os

RUN = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# class transition table: TABLE[cur, step] -> new class
# step classes: 0 = I (bits equal), 1 = S+, 2 = S-
I, SP, SM, P0, P1, DEAD = range(6)
TABLE = np.array([
    #  I   S+  S-
    [ I,  SP, SM],   # from I
    [SP, DEAD, P1],  # from S+
    [SM, P0, DEAD],  # from S-
    [P0, DEAD, SM],  # from P0  (P0*S+ = |0><0|1><0| = 0; P0*S- = S-)
    [P1, SP, DEAD],  # from P1  (P1*S+ = S+; P1*S- = 0)
    [DEAD, DEAD, DEAD],
], dtype=np.int8)
VALUE = np.array([2, 0, 0, 1, 1, 0], dtype=np.int8)  # trace by final class


def build_T(n):
    dim = 1 << n
    states = np.arange(dim, dtype=np.int32)
    cls = np.zeros(dim, dtype=np.int8)  # classes for (s=0 fixed row? NO: full grid)
    # For the full matrix we need classes for every (s, s') pair: iterate over s rows.
    rows = []
    cols = []
    vals = []
    for s in range(dim):
        c = np.zeros(dim, dtype=np.int8)  # class of prod for (s, s') as s' varies
        sb = (s >> np.arange(n)) & 1      # bits of s, per column
        for col in range(n):
            sbit = sb[col]
            # step class per s' bit: equal -> I(0); (1,0) -> S+(1); (0,1) -> S-(2)
            step = np.where(sbit == 1, np.where(((states >> col) & 1) == 1, 0, 1),
                            np.where(((states >> col) & 1) == 1, 2, 0)).astype(np.int8)
            c = TABLE[c, step]
        v = VALUE[c]
        nz = np.nonzero(v)[0]
        rows.append(np.full(len(nz), s, dtype=np.int32))
        cols.append(nz.astype(np.int32))
        vals.append(v[nz])
        if s % 4096 == 0:
            print(f"  row {s}/{dim}", flush=True)
    return (np.concatenate(rows), np.concatenate(cols), np.concatenate(vals))


def trace_mod(rt, ct, vt, n, mod, chunk=512):
    """Tr(T^n) mod p: propagate basis chunk C as dense matrix; use CSC multiply.
    Tr = sum over s of (e_s T^n)[s]. We compute W = C @ T repeatedly (n times) where
    C rows are unit vectors; then pick diagonal entries. Dense-chunk times sparse
    via scipy.sparse."""
    import scipy.sparse as sp
    dim = 1 << n
    T = sp.csr_matrix((vt.astype(np.int64) % mod, (rt, ct)), shape=(dim, dim))
    total = 0
    for start in range(0, dim, chunk):
        end = min(start + chunk, dim)
        V = np.zeros((end - start, dim), dtype=np.int64)
        V[np.arange(end - start), np.arange(start, end)] = 1
        for _ in range(n):
            V = (V @ T) % mod          # dense @ csr -> dense np.matrix? ensure ndarray
            V = np.asarray(V) % mod
        total = (total + int(V[np.arange(end - start), np.arange(start, end)].sum())) % mod
        if (start // chunk) % 8 == 0:
            print(f"  trace chunk {start}-{end} mod {mod}", flush=True)
    return total % mod


if __name__ == "__main__":
    # validation: n = 3, 4 traces must be 148, 2970
    for n, expect in ((3, 148), (4, 2970)):
        r, c, v = build_T(n)
        # exact small trace by dense power
        dim = 1 << n
        T = np.zeros((dim, dim), dtype=object)
        T[r, c] = v.astype(object)
        P = np.eye(dim, dtype=object)
        for _ in range(n):
            P = P @ T
        tr = int(np.trace(P))
        print(f"n={n}: Tr(T^{n}) = {tr} (expect {expect}) {'OK' if tr == expect else 'FAIL'}")
    # n = 15 build
    print("building T at n = 15 ...", flush=True)
    r15, c15, v15 = build_T(15)
    print(f"nnz(T15) = {len(r15)}  ({len(r15)/32768:.1f} per row)", flush=True)
    np.savez_compressed(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "output",
                                     "T15_sparse.npz"), rows=r15, cols=c15, vals=v15)
    print("saved T15_sparse.npz")
