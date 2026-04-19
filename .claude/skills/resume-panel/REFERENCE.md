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

Send this prompt to every persona. All 12 calls must go in a **single parallel Agent tool message** (one tool call per persona, all in one response). Do not paraphrase — the source-of-truth framing is load-bearing:

> Review `will_cygan_resume.typ` as the artifact under review.
>
> **Source-of-truth evidence base.** Also read `work-experience/01-linkedin-swe.md` (Software Engineer, LinkedIn, Feb 2022 – Mar 2024) and `work-experience/02-linkedin-sr-swe.md` (Senior Software Engineer, LinkedIn, Mar 2024 – Present). These contain the full Context / Role / Actions / Impact / Tech / Status logs. They are the authoritative source for every LinkedIn claim on the resume. `work-experience/99-personal-projects.md` covers the Projects section. `work-experience/ACRONYMS.md` glosses LinkedIn-internal terms (LBP, OMS, VYMBII, LiX, WSL, SWI, etc.) — use it instead of guessing.
>
> **Relevance Score prior.** Each project in `work-experience/*.md` carries a `**Relevance:** N/5 — <rationale>` field (rubric: `work-experience/RELEVANCE.md`). Treat it as a **calibration prior, not gospel** — the author's judgment of how heavily a deliverable should weigh on a resume.
>
> **What to do with it.** As you evaluate the resume, explicitly cross-reference:
> 1. **Inflation / under-support.** Flag any claim on the resume whose number, scope, scale, or ownership is not corroborated by `work-experience/`. Cite the conflicting / missing line. If a number on the resume differs from the work-experience log, report the delta.
> 2. **Buried lead.** Flag material in `work-experience/` — especially high-RS projects — that is missing from, weakly represented on, or out-ranked by weaker material on `will_cygan_resume.typ`. Name the specific bullet being under-sold. **Weight by RS**: a missing RS 5/4 project is a high-priority buried lead; a missing RS 3 is medium; RS 2/1 do not belong on the resume by design.
> 3. **Real-estate check.** If an RS 2/1 project has made it onto the resume while RS 5/4 material is absent or weak, flag the swap.
> 4. **Score disagreement.** If you believe a score is wrong (an RS 5 that seems inflated to you, or an RS 3 that seems under-rated), say so explicitly and explain why — this is cheap calibration for the author.
>
> Produce your standard output: VERDICT, CONFIDENCE, TOP ISSUES (with `will_cygan_resume.typ` line refs; add `work-experience/*.md` citations whenever an issue is inflation, a buried lead, or a score disagreement), and WHAT'S WORKING. Cap at 5 issues.
>
> **RS citation requirement.** Any issue framed as inflation, buried lead, real-estate waste, or score disagreement MUST cite the Relevance Score of the affected project inline (e.g., "JVM tuning (RS 2/5)" or "VYMBII Slideshows (RS 4/5, `01-linkedin-swe.md`)"). If none of your top issues touch RS-weighted material, state that explicitly — silence is not a valid default. If you believe an RS is wrong, raise it as its own issue with "SCORE DISAGREEMENT:" prefix.

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
