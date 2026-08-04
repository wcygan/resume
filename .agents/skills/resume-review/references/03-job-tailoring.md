# Job tailoring

Tailor by mapping requirements to truthful evidence, not by copying keywords
into the resume.

## Requirement map

Normalize the supplied job description into a compact table:

| Requirement | Importance | Existing evidence | Status | Truthful action |
| --- | --- | --- | --- | --- |
| Exact or normalized requirement | required or preferred | JSON/work-experience location | supported, partial, unknown, or gap | keep, surface, clarify, verify, or omit |

Use `required` only when the posting actually distinguishes it from preferred
criteria. Preserve uncertainty when the posting is ambiguous.

## Status meanings

- **Supported:** Direct evidence demonstrates the requirement.
- **Partial:** Adjacent or narrower evidence exists; explain the gap.
- **Unknown:** The repository does not settle whether the experience exists.
- **Gap:** Available evidence indicates the requirement is not represented.

Unknown and gap are not permission to fabricate.

## Tailoring rules

- Prefer reordering, selection, and clearer supported terminology before adding
  new content.
- Use the posting's exact terminology only when it truthfully describes the
  documented work.
- Do not rename an employment title to the target title.
- Do not turn familiarity into production ownership or an adjacent technology
  into direct experience.
- Do not force every posting keyword into the resume. Prioritize requirements
  that are important, differentiating, and supported.
- Separate shipped outcomes from targets and in-flight work.

## Proposed changes

For each proposed change provide:

```text
Current content:
Proposed content or ordering:
Requirement served:
Candidate evidence:
Risk or caveat:
```

If the user requests implementation, edit `will_cygan_resume-data.json`, then
compile and inspect the actual PDF. A content mapping alone does not establish
one-page fit or mechanical parsability.
