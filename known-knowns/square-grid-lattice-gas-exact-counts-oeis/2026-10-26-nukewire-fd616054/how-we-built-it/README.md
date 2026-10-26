# How we built it

- indep_run.py — the Run B pipeline (numpy + scipy + sympy): DFS alternating flip-mask
  builder for the transfer matrix (from the 2x2 matrix-product characterization derived
  and brute-force-verified on 2026-10-25), full reproduction gate n = 2..14 (CRT path,
  proven primes), the n = 15 build (14,316,140 nonzeros in 7 s) and the trace over 612
  dihedral-x-complement orbit representatives with six sympy-verified primes and CRT.
  Deterministic; no randomness. Saved outputs: gate_output.txt, build_output.txt,
  trace_output.txt (the a(15) residues and CRT).
- verify_standalone.py (in ../verify-it-yourself/) — the third path: pure-stdlib exact
  big-integer trace (the "one exact big-integer run" arm of the two-run rule).
- PREREG.md — the frozen pre-registration (criterion verbatim, thresholds, the two-run
  design fixing the 2026-10-25 panel's objections), timestamped before any a(15) output
  was scored.
- Run A (the first independent computation, a different session): preserved at
  runs/2026-10-25-1031/ in the submitting workspace — class-DP builder, 7 moduli, its
  own gate and panel files. Its recorded value equals the claimed integer.
- Pinned requirements: python 3.11; numpy 2.4.6; scipy 1.17.1; sympy (current);
  the standalone path needs the standard library only.
