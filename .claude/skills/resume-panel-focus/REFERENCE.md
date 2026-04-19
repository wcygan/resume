# Section-Focused Panel Reference

## Section Routing

Match `$ARGUMENTS` case-insensitively against the aliases in the first column.

| Section (aliases) | Personas to spawn |
|---|---|
| `work-experience`, `work`, `experience`, `bullets` | `hiring-manager`, `bar-raiser`, `staff-ic-peer`, `domain-sme-systems`, `technical-screener`, `future-self-skeptic` |
| `skills` | `ats-parser`, `recruiter-triage`, `domain-sme-systems` |
| `projects` | `staff-ic-peer`, `domain-sme-systems`, `career-coach`, `hiring-manager` |
| `formatting`, `typography`, `layout`, `visual` | `typography-reviewer`, `recruiter-triage`, `ats-parser` |
| `narrative`, `positioning`, `overall`, `story` | `career-coach`, `skip-level-exec`, `leveling-committee` |
| `header`, `top`, `contact` | `recruiter-triage`, `skip-level-exec`, `ats-parser` |

## Missing or Unknown Argument

If `$ARGUMENTS` is empty, `null`, or matches no alias, call AskUserQuestion with the six section groups as options. Do NOT proceed with a default — the whole point of this skill is a targeted review, which requires an explicit section.

## Spawn Prompt

Send to each matched persona in a single parallel Agent tool message:

> Review only the `[section]` section of `will_cygan_resume.typ`. Ignore unrelated sections.
>
> **Source-of-truth evidence base.** `work-experience/01-linkedin-swe.md` and `work-experience/02-linkedin-sr-swe.md` contain the full project logs backing LinkedIn claims; `work-experience/99-personal-projects.md` backs the Projects section; `work-experience/ACRONYMS.md` glosses internal terms. Each project also carries a `**Relevance:** N/5 — <rationale>` field (rubric: `work-experience/RELEVANCE.md`) — use it as a calibration prior.
>
> **Cross-reference responsibilities** when the section touches substantive content (`work-experience`, `bullets`, `projects`, `narrative`):
> - Flag inflation: resume claims not corroborated by `work-experience/*.md`.
> - Flag buried leads: RS 5/4 material missing from or weakly represented on the resume.
> - Flag real-estate waste: RS 2/1 material that made it onto the resume.
> - Flag score disagreements: if a project's RS looks inflated or under-rated, say so.
>
> Produce your standard output: VERDICT, CONFIDENCE, TOP ISSUES (with line refs to both `will_cygan_resume.typ` and `work-experience/*.md` when relevant), WHAT'S WORKING. Cap at 5 issues.

Substitute `[section]` with the normalized section name (e.g., `work-experience`, not the alias the user typed).

For sections where `work-experience/` is not the evidence base (`formatting`, `header`, `skills`), the cross-reference responsibilities are non-binding — personas may ignore them if the section doesn't benefit from that context.

## Output Format

### Section-Focused Panel Review: `[section]`

**Personas Consulted:** [comma-separated list]

**Consensus on This Section:** [advance | borderline | reject]

**Per-Persona Summary Table**

| Persona | Verdict | Top Issue (one line) |
|---|---|---|
| ... | ... | ... |

**Top Issues in This Section** (max 7, ranked by cross-persona support and severity)

1. **[severity]** [issue] — raised by: [persona names] — [line refs]
   Fix: [concrete suggestion]
2. ...

**Spillover (if any)**

Issues that touch other sections — one sentence each, not expanded into full findings.

**What's Working in This Section**

1-3 bullets on strengths the personas flagged.

**Recommended Next Step**

The single most impactful fix and which skill or workflow to run next. Examples: "run `/resume-debate <line>` on the disputed bullet at line N", or "re-run `/resume-panel-focus skills` after adjusting the skills section", or "use the `resume-optimizer` skill's bullet-rewrite workflow".
