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

> Review only the `[section]` section of `will_cygan_resume.typ`. Ignore unrelated sections. Produce your standard output: VERDICT, CONFIDENCE, TOP ISSUES (with line refs), WHAT'S WORKING. Cap at 5 issues.

Substitute `[section]` with the normalized section name (e.g., `work-experience`, not the alias the user typed).

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
