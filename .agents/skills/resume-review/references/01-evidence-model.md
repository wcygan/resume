# Evidence model

Use an explicit evidence model so advice does not silently become fact.

## Evidence classes

| Class | Meaning | Examples | Permitted use |
| --- | --- | --- | --- |
| Fact | Directly supported by an authoritative artifact or reviewed source | JSON field, documented project outcome, supplied job requirement | State directly with a citation to the local or external source |
| Inference | Reasonable interpretation of facts with uncertainty | A bullet may signal platform ownership | State the reasoning and confidence |
| Practitioner heuristic | Professional or community guidance, not causal proof | Tailor to the role; prefer direct language | Use as a recommendation and identify the source type |
| Preference | Aesthetic or strategic choice | Section order or desired density | Attribute it to the user or reviewer |
| Unknown | Evidence is absent, conflicting, stale, or too weak | Unverified metric or unsupported requirement | Preserve as unknown or request evidence |

## Evidence ledger

For every consequential finding, capture:

```text
Finding:
Artifact location:
Classification: fact | inference | practitioner heuristic | preference | unknown
Supporting evidence:
Counterevidence or limitation:
Confidence: high | medium | low
Recommended action:
```

Confidence describes support for the finding, not a hiring probability.

## Claim checks

Before retaining or rewriting a claim, verify:

1. **Truth:** Does a reviewed source support the work, number, status, and
   ownership implied?
2. **Attribution:** Is individual contribution distinguishable from team or
   organization outcomes?
3. **Meaning:** Is the metric's unit, baseline, timeframe, and causal link clear
   enough to defend?
4. **Status:** Is shipped impact distinguished from targets, projections, or
   in-flight work?
5. **Consistency:** Do JSON, supporting notes, dates, and the rendered artifact
   agree?

Do not upgrade a target to an outcome, team work to sole ownership, correlation
to causation, or a supporting note to a verified public fact.

## Review outcome vocabulary

- **Keep:** Supported, relevant, and already efficient.
- **Revise:** Supported, but its meaning, ownership, or relevance is obscured.
- **Verify:** Potentially valuable, but evidence is incomplete or conflicting.
- **Omit:** Low-value, redundant, unsupported, or too costly in page space.
- **Untested:** Requires a rendered, external, or user-authoritative check that
  has not occurred.
