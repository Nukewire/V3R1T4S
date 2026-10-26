# Novelty verdict — p1 claim: a(15) of OEIS A054759

## Live primary source (fetched once, honestly; no retries)

- URL: https://oeis.org/A054759/b054759.txt
- fetch time: 2026-10-26T08:07:26Z (UTC)
- HTTP status: 200 (plain curl, one attempt)
- size: 304 bytes; sha256 26a837111876762bf9d1c5892c21ec1a15c36e00b0ee9e45bd2c389741cbfada
  (byte-identical to the fetch recorded in the claim's table_record.md)
- largest index present: n = 14 (value 15844635835975276495290739119895808472, matches the
  claim's stated baseline)
- a(15): ABSENT — no line "15 ..." in the live b-file.

## Is the claimed term new?

Yes by the stated rule: a next term is new iff absent from the live b-file/DATA at
verification time. The largest published index is 14, the claim is exactly the n = 15
term, and it is absent from the live b-file at 2026-10-26T08:07:26Z. The claim package's
own fetch (2026-10-26T07:32:39Z) is byte-identical (same sha256), so nothing changed
between the claim's baseline and this verification.

## Prior or equal results (the tie check — a tie would NOT count for p1)

- Trophy case (repo TROPHY_CASE.md, grepped): no match for "A054759", "square ice",
  "lattice gas", "Eulerian orientation", or "six-vertex". No prior or equal result there.
- Open pull requests of the V3R1T4S repo: fetched the open-PR list twice (page 1 and
  page 2, ~200 open PRs, titles and bodies grepped for A054759 / square ice /
  lattice gas / Eulerian orientation): zero matches. No competing a(15) claim PR.
  (Coverage note: two API pages fetched, the budget allowed; deeper pages were not
  paged through.)
- Literature (two web searches, the stated maximum):
  1. Search for recent A054759 extensions 2025-2026: no result reports any new term of
     A054759; the OEIS entry itself remains the only authority and its b-file stops at
     n = 14 (checked live above).
  2. Search for the exact claimed integer 4310182149988584261406143524214457416387448:
     no exact match anywhere on the indexed web — no tie, no prior publication of this
     value.

## What this verdict covers

This is a partial-win (p1) claim whose bar is "the next unknown term", not a record over
other hunters. Checked: the live b-file (absent at verification time), the repo trophy
case (no prior/equal entry), open PRs (no competing claim), and the indexed literature
(no 2025-2026 extension, no occurrence of the value itself). Nothing known beats or ties
the claimed term. Novelty of a(15) at verification time is established.

context: zcode Agent-tool subagent, fresh context
pass: true
