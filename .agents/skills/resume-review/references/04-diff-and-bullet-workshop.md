# Diff and bullet workshop

Use evidence and artifacts to compare versions or refine a single bullet.
Do not create theatrical debate rounds or persona votes.

## Version comparison

1. Resolve the requested baseline: current `HEAD`, another git ref, or a
   supplied file.
2. Compare `will_cygan_resume-data.json` whenever both versions use the current
   JSON-driven renderer. The thin `.typ` adapter is not a meaningful content
   diff.
3. Show the relevant raw diff before interpreting it.
4. Classify each material change as improved, regressed, neutral, or untested.
5. Cite the evidence and reasoning for the classification.
6. When layout could change, render both artifacts under the same toolchain and
   inspect both PDFs. Otherwise mark visual effects untested.

Do not count issues resolved as a net score unless the issues are comparable in
consequence. One unsupported claim can outweigh several wording improvements.

## Bullet workshop

Locate the bullet in JSON and its supporting work-experience entry. Evaluate:

- **Truth:** status, metric, causality, and ownership are defensible.
- **Signal:** the bullet shows a differentiating decision, mechanism, scope, or
  outcome for the target role.
- **Compression:** every clause earns its rendered space.
- **Coherence:** one primary action/system and one or two related outcomes are
  easier to understand than unrelated accomplishments joined together.
- **Interviewability:** the candidate can explain measurement, tradeoffs,
  failures, and individual contribution.

Preserve the current wording when it already performs well. When alternatives
would clarify a real tradeoff, offer no more than three:

- outcome-first;
- mechanism-first; and
- scope/ownership-first.

Every alternative must remain inside the same factual envelope. State what
each version emphasizes and sacrifices rather than declaring consensus.
