---
name: resume-panel
description: Fan out a 12-persona review panel against will_cygan_resume.typ in parallel, with work-experience/*.md supplied as the source-of-truth evidence base, and produce a consolidated dashboard with consensus verdict, dissent highlights, and deduplicated top issues. Use when the user wants a comprehensive multi-angle resume review, asks for a "panel review", "full review", "multi-angle review", or wants every reviewer to weigh in at once. Covers ATS parsing, recruiter triage, hiring manager, technical screener, bar raiser, staff IC peer, leveling committee, skip-level exec, domain SME, typography, future-self skeptic, and career coach perspectives.
allowed-tools: Read, Grep, Glob, Agent
---

# Resume Panel Review

Run a parallel fan-out of all 12 reviewer sub-agents defined in `.claude/agents/` against `will_cygan_resume.typ`, with `work-experience/*.md` supplied as the evidence base, then synthesize their outputs into a single dashboard.

## Source-of-truth hierarchy

Every reviewer must treat these three inputs with distinct roles. Brief them explicitly in the spawn prompt — do not assume the persona definition covers it.

1. **`will_cygan_resume.typ`** — the artifact under review. This is what recruiters, ATSs, and hiring managers actually see. All verdicts and line references land here.
2. **`work-experience/01-linkedin-swe.md`** and **`work-experience/02-linkedin-sr-swe.md`** — the source of truth for every LinkedIn role. Contains full Context / Role / Actions / Impact / Tech / Status logs, the "Bullet Points" section (resume-ready condensed lines), and raw evidence for every claim. `work-experience/99-personal-projects.md` covers the Projects section. `work-experience/ACRONYMS.md` glosses LinkedIn-internal terms.
3. **`advice/*.md`** — methodology (STAR/XYZ, quantification, readability). Agents already know to cite these; you do not need to re-brief.

Reviewers must use (2) in three directions:
- **Inflation / under-support check.** Any resume claim whose scope, number, or scale is not corroborated by `work-experience/` is a flag. Example: a QPS, revenue, or row-count figure on the resume should match the work-experience entry; unverifiable numbers are a `bar-raiser` / `future-self-skeptic` issue.
- **Buried-lead check.** Strong, well-quantified material in `work-experience/` (especially the `## Bullet Points` sections and high-impact projects) that is **missing from, weakly represented on, or out-ranked by weaker material on** `will_cygan_resume.typ` is a flag. This is usually a `hiring-manager`, `skip-level-exec`, `staff-ic-peer`, or `career-coach` issue.
- **Relevance Score calibration.** Each project in `work-experience/*.md` carries a `**Relevance:** N/5 — …` field documented in `work-experience/RELEVANCE.md`. Use the score as a prior: RS 5/4 projects missing from the resume are high-priority buried leads; RS 2/1 projects on the resume are wasted real estate. If a reviewer disagrees with a score (inflated or under-rated), it must say so — the score is human judgment being calibrated against, not gospel.

## Process

1. **Fan out.** In a single message, launch all 12 sub-agents in parallel using the Agent tool — one call per persona. Use the spawn prompt in `REFERENCE.md § Spawn Prompt` exactly as written; it encodes the source-of-truth hierarchy above.

2. **Collect.** As each returns, record its verdict, confidence, top issue, and line references in the summary table. Line refs land in `will_cygan_resume.typ`; evidence/counter-evidence citations land in `work-experience/*.md`.

3. **Tally consensus.** Count the verdicts across all 12. Identify the dominant verdict and any dissenters.

4. **Highlight dissent.** For each persona whose verdict disagrees with the majority, quote their strongest reason. Dissent is high-signal — surface it, don't average it away. If all 12 agree, say so explicitly.

5. **Deduplicate issues.** Merge top issues from all 12 into a ranked list of 10 max. Weight by cross-persona support (more personas raising the same issue = higher priority) and severity. A single strong technical-depth concern from `domain-sme-systems` — or a single well-evidenced buried-lead from `hiring-manager` citing a specific `work-experience/` bullet — may still rank above a broader but shallower complaint.

6. **Emit the dashboard.** Use the output format in `REFERENCE.md § Dashboard Format`. The Consolidated Top Issues section must cite `work-experience/` line refs whenever an issue is framed as inflation or a buried lead.

## Notes

- The 12 sub-agents are defined in `.claude/agents/` and already know which `/advice/*.md` files to cite. You do not need to brief them on methodology — but you DO need to brief them on the source-of-truth hierarchy above, since most personas' own definitions do not reference `work-experience/`.
- Expect sub-agent outputs to be noisy. Synthesize aggressively — 10 consolidated issues is the cap, not the target.
- Recommend a follow-up skill or command at the end of the dashboard based on the consolidated issues (e.g., `/resume-panel-focus`, `/resume-debate`, or a tactical skill from `resume-optimizer`).

See `REFERENCE.md` for the full persona roster, the exact spawn prompt, and the output template.
