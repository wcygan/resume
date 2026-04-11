# Resume Panel Reference

## Persona Roster (12)

All defined in `.claude/agents/`. Each persona produces structured output: `VERDICT`, `CONFIDENCE`, `TOP ISSUES` (with line refs), `WHAT'S WORKING`.

| # | Sub-agent name | Funnel stage | Primary failure mode caught |
|---|---|---|---|
| 1 | `ats-parser` | Automated pre-screen | Unparseable layout, missing exact-title keywords, column breakage |
| 2 | `recruiter-triage` | 10-sec sourcing scan | Buried lead, unscannable top-third, job-hop signals |
| 3 | `hiring-manager` | 2-5 min screening | Untailored bullets, stack gaps, inflation that won't survive grilling |
| 4 | `technical-screener` | Engineering vote | Self-inflicted wounds, flat trajectory, irrelevant stack |
| 5 | `bar-raiser` | Cross-team skeptic | Vanity metrics, unfalsifiable claims, suspicious round numbers |
| 6 | `staff-ic-peer` | Peer calibration | Insufficient scope, missing multiplier/cross-team signals |
| 7 | `leveling-committee` | Leveling rubric | Title/scope mismatch, down-level risk |
| 8 | `skip-level-exec` | 60-sec VP skim | Weak exec summary, missing business-impact framing |
| 9 | `domain-sme-systems` | Technical SME | Buzzword soup, missing mechanism-level detail |
| 10 | `typography-reviewer` | Visual craft | Hierarchy, spacing, widows, page breaks, inconsistent layout |
| 11 | `future-self-skeptic` | 2-year self-review | Claims the candidate won't want to defend in 2 years |
| 12 | `career-coach` | Meta-narrative | Positioning drift, coherence across sections, missing "so what" |

## Spawn Prompt

Send this prompt to every persona. All 12 calls must go in a **single parallel Agent tool message** (one tool call per persona, all in one response):

> Review `will_cygan_resume.typ` and produce your standard output: VERDICT, CONFIDENCE, TOP ISSUES (with line refs to specific lines in the resume), and WHAT'S WORKING. Cap at 5 issues.

## Dashboard Format

### Resume Panel Review

**Consensus Verdict:** [advance | borderline | reject] — X of 12 personas

- Advance: [count] — [persona names]
- Borderline: [count] — [persona names]
- Reject: [count] — [persona names]

**Per-Persona Summary Table**

| Persona | Verdict | Confidence | Top Issue (one line) |
|---|---|---|---|
| ats-parser | ... | ... | ... |
| recruiter-triage | ... | ... | ... |
| hiring-manager | ... | ... | ... |
| technical-screener | ... | ... | ... |
| bar-raiser | ... | ... | ... |
| staff-ic-peer | ... | ... | ... |
| leveling-committee | ... | ... | ... |
| skip-level-exec | ... | ... | ... |
| domain-sme-systems | ... | ... | ... |
| typography-reviewer | ... | ... | ... |
| future-self-skeptic | ... | ... | ... |
| career-coach | ... | ... | ... |

**Dissenting Reads**

For each persona whose verdict differs from the consensus, one paragraph quoting their strongest reason. If there's no dissent, say so explicitly — uniform verdicts across 12 reviewers is itself a signal.

**Consolidated Top Issues** (max 10, ranked by cross-persona support and severity)

1. **[severity]** [issue] — raised by: [persona names] — [line refs in will_cygan_resume.typ]
   Fix: [strongest concrete suggestion from any persona]
2. ...

**What Multiple Personas Agreed Is Working**

1-3 bullets on strengths that showed up in multiple `WHAT'S WORKING` sections.

**Recommended Next Step**

One sentence suggesting the most impactful follow-up: `/resume-panel-focus <section>` for a targeted re-review, `/resume-debate <line>` for a disputed bullet, `/resume-tailor-panel <jd>` if the user has a target role, or one of the tactical workflows in the `resume-optimizer` skill.
