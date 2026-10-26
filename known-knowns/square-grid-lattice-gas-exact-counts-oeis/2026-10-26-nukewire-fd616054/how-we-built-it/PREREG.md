# PREREG — frozen 2026-10-26T07:40:30Z (before any a(15) output was scored)

target: square-grid-lattice-gas-exact-counts-oeis (partial win p1: a(15) of A054759)

## Criterion (verbatim from bank/targets.json, p1 arm)

p1: The next unknown term(s) of A054759 (square ice on the n x n torus) or A027683 (hard
squares on the n x n torus), same two-run and reproduction rules; A054759 is expected to
be easy (row transfer matrix with 2^n states plus one tracked boundary edge) and is a
partial only. [Two-run rule from the success criterion: "computed by two independent runs
that agree exactly (different primes/CRT moduli sets AND a different decomposition, e.g.
row vs column sweep or a different state encoding, or one exact big-integer run), with the
same code reproducing every published term for n <= N-1 exactly, and the result consistent
with the known growth constant (a(N)^(1/N^2) within 1e-3 of the corresponding entropy
constant)."]

## Tonight's design: the independent SECOND run (the gap that failed the 10-25 gate)

- Run A (2026-10-25-1031, different session): class-DP T-build + orbit trace; a(15) =
  4310182149988584261406143524214457416387448; PROMISING (panel: 2 runs shared a builder;
  2 moduli composite).
- Run B (THIS session, fresh context): written from the 2026-10-25-0731 derivation (2x2
  matrix-product rule, this session's own work); no code or artifacts shared with Run A.
  Decomposition: DFS enumeration of alternating flip-masks per state -> CSR T -> trace
  via D15 x Z2 orbit representatives, modular sparse matvecs, sympy-PROVEN primes only,
  CRT with a rigorous bound (max row sum: a(15) <= 2^15 * R^15).
- Run A <-> Run B: different builders, different state encodings (matrix-class DP vs
  flip-mask DFS), different prime sets (all proven), different sessions/authors.
- Reproduction gate (Run B's own code): n = 2..14 vs the live b-file (fetched
  2026-10-26T07:32Z, sha256 26a83711...fada — a(15) still absent; PENDING nothing).

## Thresholds

- Claim p1 iff: Run B a(15) == Run A a(15) exactly AND gate n=2..14 all OK AND growth
  a(15)^(1/225) within 1e-3 of the entropy constant AND CRT modulus product exceeds the
  rigorous row-sum bound with >= 256x margin.
- Any mismatch: no claim; treat Run A's value as suspect and investigate.

## Null design

null_test: not needed because the claim is an explicit integer checked by exact modular
arithmetic (CRT against a rigorous bound) plus the full n <= 14 reproduction gate and the
b-file diff; no statistical claim is made.

## Time box

Standard run (~3h); trace15 may consume up to ~90 min; panel follows if the claim lands.
