# Panel verdict — role REPRODUCE — claim: a(15) of OEIS A054759 = 4310182149988584261406143524214457416387448

context: zcode Agent-tool subagent, fresh context

## Definition worked from (quoted)

"a(15) of OEIS A054759 — the number of Eulerian orientations of the 15 x 15 toroidal
square lattice (square ice, six-vertex model at the ice point)" where an Eulerian
orientation of the n x n torus means "every edge directed, exactly 2 arrows in and 2 out
at each vertex" (CLAIM.md / claim/verify_standalone.py). Transfer-matrix characterization
under test (quoted): "T[s,s'] = 2 if s == s'; 1 iff the set bits of s XOR s' form an even
cyclic sequence on which s's bits alternate; else 0", with a(n) = trace(T^n).

All my code: runs/2026-10-26-0731/panel/skeptic_check.py, skeptic_rows.py,
skeptic_crt.py, skeptic_orbit.py (outputs tee'd beside them). Written from the
definition before I read any of the author's pipeline code (claim/verify_standalone.py
was read as part of the claim package; attempts/constructor/code/indep_run.py only
after my checker ran).

## What I implemented and ran, and the results

1. **Own brute-force counter from the definition** (all 2^(2n^2) orientations of the
   n x n torus, in-degree == 2 checked at every vertex; parallel edges of the 2-torus
   counted as distinct): a(1) = 4, a(2) = **18**, a(3) = **148** — both quoted b-file
   values confirmed by exhaustive enumeration. Published terms taken from the live
   b-file fetched by me this session (runs/2026-10-26-0731/panel/b054759_fetch.txt,
   sha256 26a837111876762bf9d1c5892c21ec1a15c36e00b0ee9e45bd2c389741cbfada, 304 bytes,
   byte-identical to the fetch recorded in claim/table_record.md; content n = 1..14
   only, a(15) ABSENT — the live-table rule holds at verdict time).
2. **Transfer-matrix characterization vs my own brute force, ALL pairs**: for every
   (s, s') pair I enumerated all 2^n orientations of the row's horizontal ring and
   counted Eulerian completions W(s,s'); compared with the claimed rule. n=2: 16/16
   pairs, n=3: 64/64, n=4: 256/256 — **zero mismatches**. Trace with the brute-forced
   W gives a(2) = 18, a(3) = 148 (equals the direct enumeration); trace with the rule
   reproduces the published a(1)..a(8) exactly (4, 18, 148, 2970, 143224, 16448400,
   4484823396, 2901094068042).
3. **Orbit-trace assumption**: Run B's trace sums orbit sizes times diag(T^n) over
   D15 x Z2 representatives. With my own rule-built T, diag(T^n) is invariant under
   rotation, reversal and complement at n = 3, 4, 5, and my orbit-sum reconstruction
   gives 148, 2970, 143224. No int64 overflow in their matvec (data values are {1, 2}
   mod p, so row sums stay ~2.6e12 << 2^63).
4. **Author's standalone verifier re-run** (venv python, from panel/):
   `python ../claim/verify_standalone.py` — completed n = 2..12 all OK plus final
   `PASS`, exit 0 (panel/verify_standalone_rerun.txt). The saved
   claim/verify_standalone_output.txt (cut at n = 11 under the author's time cap)
   matches my run line-for-line through n = 11.
5. **Run B gate re-run** (from the run-folder root, as REPRODUCE.md instructs):
   `python attempts/constructor/code/indep_run.py gate` — **every published term
   n = 2..14 reproduces exactly**, all OK, exit 0 (panel/gate_rerun.txt); every "pub"
   value equals my independent live b-file fetch, including a(13) =
   137950545200232788276834783781648 and a(14) =
   15844635835975276495290739119895808472. Deterministic pipeline (deterministic
   prime descent from 2^30, DFS builder, fixed orbits); re-run output is identical to
   the saved attempts/constructor/code/gate_output.txt.
6. **Run A (runs/2026-10-25-1031/)**: preserved with its own claim/statement.md
   recording the SAME integer 4310182149988584261406143524214457416387448; its builder
   claim/code/build_T15.py is a genuinely different implementation (class-DP over a
   2x2 matrix-product semigroup with a 6-class transition table, vectorized numpy)
   versus Run B's per-state DFS flip-mask enumeration — different algorithm, different
   state handling, no shared code. Its own panel files exist: panel/reproduce.md
   (pass: true — that skeptic re-derived a(13), a(14), a(15) with yet another prime set
   and found the author's T15 npz bit-identical to an independently built one),
   panel/novelty.md (pass: true), panel/gate.md (PROMISING — value confirmed but p1
   failed on shared builder + composite moduli + literal growth clause; its prescribed
   re-claim path — different builder, proven primes, corrected errata — is exactly what
   Run B's claim supplies).
7. **CRT arithmetic, all my own code** (residues/primes parsed from
   attempts/constructor/code/trace_output.txt, not hand-copied): all six primes
   (1073741789, 1073741783, 1073741741, 1073741723, 1073741719, 1073741717) pass my
   deterministic Miller-Rabin and are pairwise distinct; my own CRT (no sympy) over
   M = 1532494867205097740342720759854047793306665548942750543 (180 bits) reconstructs
   **exactly** 4310182149988584261406143524214457416387448 = claim/a15_value.txt
   (whose sha256 fd616054f7567327589dd9720fd91599613b6a0285484f1c49587a63651f484c
   matches CLAIM.md); direct checks a15 mod p == r true for all six. Referenced matrix
   artifacts hash-match CLAIM.md (t15_indptr 5c2266f1..., t15_indices 5a0ece43...,
   t15_data a7b06bed...).
8. **Bound check**: trace(T^15) <= 2^15 * R^15 with R = max WEIGHTED row sum. I computed
   R by two independent methods (cyclic DP over ring orientations, validated against
   brute row sums at n = 2..10; and direct rule summation over all 32768 partners for
   the top rows): R = **1220**, not 1219 — see errata. Corrected bound
   2^15 * 1220^15 = 6.47e50 (169 bits, < 2^169). M exceeds it 2368.9x, and
   a(15) < 2^15 * 1220^15 < M, so the CRT identification is rigorous even with the
   corrected constant.
9. **Growth gate (own arithmetic)**: (4/3)^(3/2) = 1.5396007; a(15)^(1/225) =
   1.5469869, raw deviation 7.386e-3 (claim: 7.39e-3); two-point fit W + c/n^2 on
   a(13), a(14): W = 1.539592 (|W - Lieb| = 8.6e-6), predicted r15 = 1.5469920,
   measured 1.5469869, difference 5.0e-6 (claim: 4.9e-6 — last-digit rounding). All
   headline numbers confirmed.

## Mismatches: none in any load-bearing object. Errata in auxiliary numbers:

- **E1 (build_output.txt "maxrowsum=1219" / CLAIM.md "rigorous bound a(15) <= 2^15 x
  1219^15 = 2^169, modulus product exceeds it 2398x")**: 1219 is
  `np.diff(indptr).max()` in indep_run.py — the max number of stored ENTRIES per row
  (1 diagonal + 1218 partners). The max weighted row sum (2 + 1218) is 1220, so the
  rigorous row-sum bound is 2^15 x 1220^15, not 1219^15. Harmless to the result: the
  modulus product still exceeds the corrected bound 2368.9x, both bounds are < 2^169,
  and the prime picker carries +8 bits of headroom. "2398x" is exact only for the
  1219 version (2398.24); with 1220 it is 2368.9.
- **E2 (CLAIM.md growth section "(it was 1.06e-3 at n = 14, 1.9e-3 at n = 13)")**:
  actual raw deviations from Lieb are 8.49e-3 at n = 14 and 9.84e-3 at n = 13. The
  surrounding conclusion (deviation is c/n^2 with c ~= 1.66; no n = 15 torus value can
  meet the literal 1e-3 raw clause) is nevertheless correct.
- **E3 (minor)**: verify_standalone.py's docstring says "the published b-file copied
  beside this file" but PUB is hardcoded (values match the live b-file, so harmless);
  the standalone check takes ~7 minutes to reach PASS incl. n = 12 on this machine,
  not the "~2"/"~4 minutes" of the docstring/REPRODUCE.md (the author's saved output
  was honestly cut at n = 11 inside their cap).

## Bottom line

Independently of the author's code paths: the definition's small values check out by
exhaustive enumeration, the claimed transfer-matrix characterization is exactly right
at every pair for n = 2, 3, 4, the orbit-trace assumption holds, the author's
standalone verifier and Run B gate reproduce every published term n = 2..14 (and the
standalone reaches n = 12 + PASS), Run A is a genuinely different implementation
recording the same integer with its own passing panel, all six moduli are prime by my
own Miller-Rabin, my own CRT reconstruction equals claim/a15_value.txt exactly, and
the corrected rigorous bound still leaves the modulus product 2368.9x above it. The
found errata (E1-E3) are in auxiliary statistics and narrative numbers, none touch the
value or the proof chain.

pass: true
