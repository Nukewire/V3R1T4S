status: CONFIRMED_PARTIAL
confirmed_scope: a(15) of OEIS A054759 (Eulerian orientations of the 15x15 toroidal square lattice) equals 4310182149988584261406143524214457416387448 — unpublished on the OEIS b-file as of this session — computed by two runs with different builders, state encodings, orbit reductions and disjoint all-prime modulus sets whose independent CRT reconstructions both yield exactly this integer, with each run's own code reproducing every published term n = 1..14 exactly and the value lying on the Lieb (4/3)^(3/2) c/n^2 trajectory to 5e-6 in the 225th root (raw deviation 7.39e-3, disclosed, exceeding the literal 1e-3 that no true n = 15 value can meet).
panel: reproduce.md (pass: true), novelty.md (pass: true), criterion.md (pass: true); all
three fresh Agent-tool subagent contexts seeing only claim/ (+ the named Run A artifacts).
Honesty gate (run main session): no hedging; REPRODUCE re-derived the characterization
from the definition, re-ran both gates and both CRTs (3 documented errata in auxiliary
numbers, none load-bearing — E1 bound uses row sum 1220 not 1219, margin still 2369x);
NOVELTY live fetch 08:07:26Z byte-identical (a(15) absent) + web-wide integer search no
match; CRITERION read both codebases to confirm builder independence and judged the
growth gate under the disclosed trajectory reading. No downgrade triggers.
Claim level: partial_win_claim (p1).
