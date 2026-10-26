# A054759 a(15): the next term of the square-ice torus sequence (partial win p1)

Submission id: 2026-10-26-nukewire-fd616054 · target:
square-grid-lattice-gas-exact-counts-oeis · claim level: partial_win_claim (p1), one
sequence term.

## What

confirmed_scope: a(15) of OEIS A054759 (Eulerian orientations of the 15x15 toroidal square lattice) equals 4310182149988584261406143524214457416387448 — unpublished on the OEIS b-file as of this session — computed by two runs with different builders, state encodings, orbit reductions and disjoint all-prime modulus sets whose independent CRT reconstructions both yield exactly this integer, with each run's own code reproducing every published term n = 1..14 exactly and the value lying on the Lieb (4/3)^(3/2) c/n^2 trajectory to 5e-6 in the 225th root (raw deviation 7.39e-3, disclosed, exceeding the literal 1e-3 that no true n = 15 value can meet).

## Check it yourself

One command, standard library only (Python 3.8+), about 4 minutes:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS` (the standalone exact-integer trace reproduces the published
a(2)..a(11); its real output is in verify-it-yourself/RECEIPTS.md).

## Compared to

OEIS A054759, b-file https://oeis.org/A054759/b054759.txt fetched 2026-10-26T07:32:39Z
(HTTP 200, sha256 26a837111876762bf9d1c5892c21ec1a15c36e00b0ee9e45bd2c389741cbfada):
terms n = 1..14, largest 15844635835975276495290739119895808472; a(15) absent. The
sequence counts Eulerian orientations of the n x n toroidal square lattice (square ice);
terms to n = 14 are due to Brendan McKay (2024). Snapshot in the-record-we-beat/.

## Not claimed

- Not a(16) or any other term; not the other sequences in the bank entry (A028420,
  A006506, A063443, A027683).
- Not a proof of anything about the limit; the Lieb-constant trajectory reading is
  disclosed as a judgment (raw finite-size deviation 7.39e-3, same order as the published
  n = 13/14 terms' deviations).
- No submission to OEIS is made by us; the human decides any outward action.

## Credits

- Brendan McKay — the published terms a(1)..a(14) this extends (OEIS A054759, 2024).
- Elliott Lieb (1967) — the square-ice residual entropy constant (4/3)^(3/2) used as the
  growth check.
- The V3R1T4S open notebook (https://github.com/elder-plinius/V3R1T4S) — the bank entry
  defining the criterion, the run protocol, and the three-skeptic panel.
- Method: transfer matrix over 2^15 vertical-arrow states; Run A builds it by a 2x2
  matrix-class DP, Run B by DFS alternating flip-mask enumeration; both trace with orbit
  reduction (Run B: dihedral x complement symmetry, 612 representatives) and modular
  arithmetic over disjoint verified-prime sets with CRT; a pure-stdlib exact big-integer
  path verifies the smallest terms.

## Packaging note

All package files are LF; hashes (SHA256SUMS, INDEX.csv, verify-it-yourself/check.py)
refer to those LF bytes; the checker accepts the CRLF-materialised form of the object
too. The object is a 43-digit integer (object/a15_value.txt).
