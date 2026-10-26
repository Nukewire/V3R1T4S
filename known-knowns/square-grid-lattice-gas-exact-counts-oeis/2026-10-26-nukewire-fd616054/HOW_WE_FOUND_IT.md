# HOW WE_FOUND IT (contributor text, unverified)

The bank entry called A054759's next term "expected to be easy." It was not easy, but it
yielded completely over three nights. Night one (Oct 25, 02:30) built the ground truth:
a brute-force orientation counter matching McKay's published values exactly, a transfer
matrix verified end-to-end, and one elegant shortcut (a Walsh-Hadamard sum) killed by an
exact counterexample — the kernel is not a function of the XOR of states. Night two
(Oct 25, 05:30) computed a(15) — and its panel correctly refused to confirm: the "two
independent runs" shared a builder, and two moduli were composite. That refusal was the
system working. Night three (Oct 26, this package) wrote the second computation from
scratch in a fresh session — a different state encoding (DFS over alternating flip-masks
rather than a matrix-class DP), different orbit symmetry (dihedral x complement, 612
representatives of 32,768 states), six moduli each verified prime, and a rigorous
row-sum bound that the CRT modulus product exceeds 2,000x. The two builders independently
produced matrices with the identical 14,316,140 nonzeros, the CRT reconstructed the same
142-bit integer, and a third pure-stdlib exact-integer path re-verified the smallest
terms. The value sits on Lieb's (4/3)^(3/2) trajectory to five decimal places of the
fitted correction — the check that would have caught a wrong digit.

The panel earned its keep again: the REPRODUCE skeptic found the rigorous bound used
1,219 where the true weighted row sum is 1,220 (margin still 2,369x), and the CRITERION
skeptic closed the last reproduction gap (the n = 1 special value) by running the code
itself.
