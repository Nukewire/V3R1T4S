# Panel verdict — role: CRITERION (integer-sequence claim, p1 arm)

context: zcode Agent-tool subagent, fresh context

Claim under test: a(15) of OEIS A054759 (Eulerian orientations of the 15x15 toroidal
square lattice, square ice) = 4310182149988584261406143524214457416387448, partial win
p1, judged against the bank's p1 arm and its quoted two-run and reproduction rules.
Everything below was recomputed by my own code this session from the claim package and
the two run folders (the 2026-10-25-1031 folder and this run's attempts/constructor
artifacts); the live b-file was fetched once, fresh.

## Clause 0 — the object and the "next unknown term" premise

- sha256 of claim/a15_value.txt matches CLAIM.md's fd616054...f484c; the integer is
  142 bits.
- Fresh fetch of the OEIS b-file this session: HTTP 200, 304 bytes, sha256
  26a837111876762bf9d1c5892c21ec1a15c36e00b0ee9e45bd2c389741cbfada — byte-identical to
  table_record.md's recorded fetch; the file ends at
  a(14) = 15844635835975276495290739119895808472. a(15) is genuinely absent; the
  baseline matches. The convention ground
  truth (2 arrows in / 2 out at every vertex of the toroidal grid) is anchored by the
  shipped brute-force checker (a(2)=18, a(3)=148) which I reran, plus my own brute runs
  giving a(1)=4, a(2)=18, a(3)=148. Clause met.

## Clause 1 — two-run substance (the crux; this is what failed the 2026-10-25 panel)

The 2026-10-25 failure was real: that session's second trace imports the first's builder
("same generator; the INDEPENDENCE is the sweep") and loads the same saved matrix
artifact, so its two runs differed only in CRT moduli. Judging the NEW pair:

- Run A (session 2026-10-25-1031): builder is the class-DP construction — a six-class
  semigroup transition table (I, S+, S-, P0, P1, DEAD) over 2x2 matrix products applied
  column-wise, numpy-vectorized across all states per row; trace via pure rotation
  orbits (union-find canonical reps, 2192 reps at n=15) with chunked dense-matrix
  propagation; 6 primes near 2^31.
- Run B (this session, attempts/constructor/indep_run.py): builder is a per-state DFS
  enumerating alternating flip-mask partners (T[s,s']=2 if s=s'; 1 iff the set bits of
  s^s' form an even cyclic alternating sequence) building a CSR matrix; trace via
  D15 x Z2 orbit representatives (rotations + bit-reversal + complement, min-image reps,
  612 reps) with per-rep modular sparse matvecs; 6 primes near 2^30.
- Genuinely different in every error-prone component: state-pair encoding
  (matrix-product class vs flip-mask structure), builder code (Run B imports nothing
  from Run A), orbit group and reduction code, trace kernel, prime set (disjoint —
  confirmed), session and context. The shared matrix artifact of the failed claim is
  gone: Run B builds its own matrix (nnz 14,316,140; shipped npy arrays hash-match
  CLAIM.md and their byte sizes are exactly consistent with that nnz and 32769 indptr
  entries).
- Arithmetic: I re-proved all six Run B primes prime with my own deterministic
  Miller-Rabin and re-did BOTH CRTs from the shipped residues with my own code: Run A's
  six residues (mod 2147483629..2147483423, product 186 bits) and Run B's six residues
  (mod 1073741789..1073741717, product 180 bits) each reconstruct exactly
  4310182149988584261406143524214457416387448. Run B's CRT modulus exceeds the rigorous
  row-sum bound 2^15 x 1219^15 = 2^169 by 2398x, and the value (142 bits) is below the
  bound — reconstruction is unique in both runs.
- Residual shared risk, weighed: both runs take the trace of the same abstract matrix T,
  and Run B's flip-mask characterization was derived in an earlier session from the same
  2x2 matrix-product mathematics. That risk is precisely what the reproduction gates
  test: each run's own pipeline reproduces every published term (below), so a wrong
  abstract T would have to survive 13 exact known values (up to ~1.6e37) and still yield
  identical wrong a(15) values through two disjoint implementations and disjoint moduli.
  The criterion asks for computational independence of the runs, not independent
  mathematics, and Run A vs Run B now has real bug-detection power (a bug in either
  builder, either orbit reduction, or either trace kernel breaks the agreement). The
  exact big-integer path (verify_standalone.py, n=2..11, non-modular and non-orbit) adds
  arithmetic-path diversity though not builder diversity — it shares Run B's
  characterization, and the claim does not overstate it. Two-run rule: MET in substance.
- Minor labeling slips, not substance: CLAIM.md calls Run A "7 moduli" — the orbit trace
  (trace_a15) used 6 primes near 2^31; the 7-moduli set near 2e9 was the same session's
  same-builder sibling trace. Either counterparty yields the identical integer, and both
  sets are disjoint from Run B's.

## Clause 2 — reproduction rule ("the same code reproducing every published term for n <= N-1")

- Run B's own gate (same build_T/compute_reps/trace_mod/CRT functions as the a(15) run):
  n = 2..14 all OK against the live b-file (gate_output.txt). The only index missing
  from the shipped output is n = 1 (loop starts at 2). I ran Run B's own functions at
  n = 1 myself: build_T(1) gives T = 2I, orbit trace gives a(1) = 4 = published. The
  brute-force checker independently grounds the same convention. Nothing is missing.
- Run A's pipeline (repro_gate, same builder and trace code as its a(15) run) reproduces
  n = 1..14, including a(1) = 4, per its saved gate output. Clause met by both runs.

## Clause 3 — growth gate (judgment call, stated explicitly)

My own numbers: a(15)^(1/225) = 1.5469869; Lieb's limit L = (4/3)^(3/2) = 1.5396007178;
raw deviation 7.3862e-3 — ABOVE the literal 1e-3. The claim disclosed this rather than
hiding it, and reported both readings. The decisive facts:

- The PUBLISHED terms already violate the literal clause: deviations 1.1564e-2 (n=12),
  9.8433e-3 (n=13), 8.4861e-3 (n=14). The deviation follows c/n^2 with c = 1.6652,
  1.6635, 1.6633, 1.6619 at n = 12..15 (0.2% drift). A value literally within 1e-3 at
  n = 15 would have to be ~61% SMALLER than the trajectory continuation (root smaller by
  0.41%, i.e. value times 0.99587^225 ~ 0.394) — i.e., the letter of the clause is
  unsatisfiable by any true continuation of this sequence at N = 15, because the bank's
  parenthetical ignored the positive O(1/n^2) finite-size term.
- Trajectory reading, recomputed: fitting W + c/n^2 to the published a(13), a(14)
  predicts root(15) = 1.5469920 vs measured 1.5469869 (agreement 5.0e-6; claim said
  4.9e-6) and W = 1.5395921 vs Lieb 1.5396007 (8.6e-6; claim said 9.0e-6). This is a
  real discriminating check: a wrong value off by 0.1% in the root (1.25x in magnitude)
  would miss by ~1.5e-3, three hundred times the observed agreement.
- Judgment: the governing words are "the result consistent with the known growth
  constant"; the 1e-3 parenthetical is an operationalization that provably cannot hold
  for the true term at N = 15 (and is already violated by the last two published terms,
  which the parenthetical was presumably meant to guard consistency with). Reading the
  gate in substance, the value sits on the Lieb trajectory to ~5e-6 and is MORE
  consistent than the published a(14). I judge the clause met under the defensible
  reading; the literal miss is disclosed, not stretched silently. One more arithmetic
  slip in the claim's parenthetical, again understating its own case: it quotes the
  n = 14 and n = 13 deviations as 1.06e-3 and 1.9e-3 (true: 8.49e-3 and 9.84e-3) —
  the true numbers make the unsatisfiability argument stronger, not weaker.

## Clause 4 — hidden quantifiers and stretched definitions

- "Every published term for n <= N-1": n = 1..14; n = 1 covered (Run A's gate; my own
  run of Run B's functions; my own brute force from the definition).
- "Next unknown term(s)": verified against the live b-file this session; one term only,
  A054759 arm only; the claim declares itself partial_win_claim p1 and claims nothing
  about A027683 or the full criterion.
- CRT quantifier ("different primes"): all primes used by both counterparty traces are
  prime (my own check; the old claim's two composite moduli belong to the discarded
  same-builder sibling trace, and Run B uses sympy-PROVEN primes only).
- No stretched definition of "two independent runs" remains: the previous stretch
  ("row vs column sweep" label for identical code on the self-dual square torus) is
  gone, replaced by a genuinely different builder and encoding.
- PREREG was frozen before results and honestly quotes the literal 1e-3 clause; the
  claim then reported the raw miss rather than quietly waiving it, which is exactly
  what the disclosure discipline requires.

## Decision

The claim satisfies the p1 arm: the next unknown term of A054759, computed by two
genuinely independent runs (different builders, state encodings, orbit reductions,
trace kernels, sessions, and disjoint proven prime sets) whose CRT reconstructions agree
exactly, with each run's own code reproducing every published term n = 1..14, and the
value on the known growth trajectory to 5e-6 (the literal 1e-3 parenthetical being
unsatisfiable by any true n = 15 value, as the published n = 13, 14 terms themselves
show). This is a genuine, non-subsumed partial win — the prior 2026-10-25 failure mode
(shared builder) is specifically and verifiably cured.

confirmed_scope: a(15) of OEIS A054759 (Eulerian orientations of the 15x15 toroidal square lattice) equals 4310182149988584261406143524214457416387448 — unpublished on the OEIS b-file as of this session — computed by two runs with different builders, state encodings, orbit reductions and disjoint all-prime modulus sets whose independent CRT reconstructions both yield exactly this integer, with each run's own code reproducing every published term n = 1..14 exactly and the value lying on the Lieb (4/3)^(3/2) c/n^2 trajectory to 5e-6 in the 225th root (raw deviation 7.39e-3, disclosed, exceeding the literal 1e-3 that no true n = 15 value can meet).

pass: true
