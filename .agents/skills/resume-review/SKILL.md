---
name: resume-review
description: "Review and improve resume content against the candidate's documented evidence and target role. Use for broad or focused resume critique, job-description tailoring, bullet refinement, before-and-after content comparison, seniority or narrative assessment, and claim-grounded interview preparation. Use resume-parsability instead for PDF extraction, ATS mechanics, Greenhouse parsing, reading order, fonts, tags, links, or layout experiments. Never invent facts, simulate independent reviewer consensus, or predict callbacks."
---

# Resume Review

Evaluate and improve resume content without turning judgment into fake
measurement. Trace claims to the repository's factual sources, separate fact
from inference, and keep the final recommendation proportionate to the
evidence.

## Companion skills

- Use `resume-parsability` when the request includes extraction, external ATS
  behavior, PDF structure, field association, reading order, links, fonts, or
  layout safety.
- Before changing Typst source, locate and follow the current `typst-author`
  skill.
- When visual layout matters, locate and follow the current `pdf` skill and
  inspect the rendered artifact.

## Source precedence

Use evidence in this order:

1. The user's requested outcome and supplied job description.
2. `will_cygan_resume-data.json` and the current rendered
   `will_cygan_resume.pdf`.
3. `work-experience/*.md` and `work-experience/ACRONYMS.md`.
4. `work-experience/RELEVANCE.md` as the author's prioritization prior, not as
   an objective score.
5. Current primary or vendor documentation for claims about a named product or
   process.
6. Identified professional guidance or practitioner experience.

Do not use a job description, advice file, model completion, or relevance
score as evidence that the candidate performed work.

## Reference router

Read the evidence model and project workflow for every task, then only the
mode-specific references needed.

| Task cue | Required references |
| --- | --- |
| Any review or rewrite | [Evidence model](references/01-evidence-model.md) and [Project workflow](references/06-project-workflow.md) |
| Broad review, focused section review, seniority, narrative, density | [Content review](references/02-content-review.md) |
| Tailor to a job description or assess fit | [Job tailoring](references/03-job-tailoring.md) |
| Compare versions or refine one bullet | [Diff and bullet workshop](references/04-diff-and-bullet-workshop.md) |
| Prepare questions or rehearse a claim | [Interview preparation](references/05-interview-preparation.md) |
| Rely on external or repository advice | [Evidence register](references/07-evidence-register.md) |

## Entry contract

Before analysis, establish:

```text
Mode: review | tailor | compare | bullet | interview
Authoritative content and rendered artifact:
Target role or audience, if supplied:
Allowed edits: none | content | layout
Relevant supporting evidence:
Requested output and completion bar:
```

Infer these from the request and checkout when safe. Reviewing, explaining,
or diagnosing is read-only; edit only when the user asks for changes.

## Core workflow

1. Read the authoritative content and the relevant supporting entries.
2. If visual hierarchy or density matters, inspect the current PDF rather than
   inferring layout from JSON or Typst.
3. Build a small evidence ledger before reaching conclusions.
4. Apply only the review lenses relevant to the requested outcome. Do not
   impersonate multiple reviewers or vote across personas.
5. Prioritize findings by consequence, confidence, and actionability. Prefer
   five strong findings to an exhaustive list of minor opinions.
6. If editing, change the content authority rather than generated artifacts,
   compile, inspect the final PDF, and run the checks required by the project
   workflow.
7. Report facts, inferences, heuristics, preferences, and unknowns distinctly.

## Non-negotiable rules

- Never create or strengthen a claim beyond its documented evidence.
- Preserve actual employer titles. Describe target-role alignment through
  truthful accomplishments and profile language, not title substitution.
- Quantify only when a reviewed source supports the number and its meaning.
- Do not manufacture keyword density, ATS scores, hiring probabilities,
  recruiter scan times, or causal claims about callbacks.
- Do not report same-model personas as independent evidence or consensus.
- Treat missing support as unknown, partial, or gap; do not fill it by
  inference.
- Preserve useful disagreement as a tradeoff when evidence does not settle a
  judgment call.

## Completion report

Lead with the recommended outcome. For each material finding include the
artifact location, evidence or counterevidence, confidence, and action. State
which checks were performed, whether the PDF was actually inspected, and what
remains untested.
