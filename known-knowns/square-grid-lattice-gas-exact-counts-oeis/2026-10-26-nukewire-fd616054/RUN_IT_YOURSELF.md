# RUN_IT_YOURSELF

From this package folder, in a fresh shell:

1. Verify the claim (stdlib only, ~4 min):

   ```sh
   sh verify-it-yourself/run_checks.sh
   ```

   Expected last line `PASS`; full expected output in verify-it-yourself/RECEIPTS.md.
   The checker verifies the object's sha256, re-derives the transfer matrix from the
   definition (alternating-flip characterization of Eulerian orientations of the torus),
   reproduces the published a(2)..a(11) by exact big-integer trace, and checks INDEX.csv
   consistency.

2. Re-check the live sequence before trusting the claim (the term is new only while
   absent upstream):

   ```sh
   curl -s https://oeis.org/A054759/b054759.txt | tail -3
   ```

   Expected today: the last row is `14 15844635835975276495290739119895808472`. A row
   `15 ...` means someone published first: re-check before citing.

3. Full recomputation of a(15) (needs python with numpy, scipy, sympy; ~9 min + ~9 min):
   how-we-built-it/indep_run.py is self-contained — run
   `python how-we-built-it/indep_run.py gate` (reproduces n=2..14 via the CRT path),
   then `python how-we-built-it/indep_run.py build` and
   `python how-we-built-it/indep_run.py trace15` (rebuilds the 14,316,140-entry matrix
   and recomputes a(15) over six proven primes). Its saved outputs from the finding run:
   how-we-built-it/{gate,build,trace}_output.txt.

4. The first independent computation (Run A) is preserved in the submitting workspace at
   runs/2026-10-25-1031/ (different session, different builder; see panel/ files).
