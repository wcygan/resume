---
name: resume-panel
description: Fan out a 12-persona review panel against will_cygan_resume.typ in parallel and produce a consolidated dashboard with consensus verdict, dissent highlights, and deduplicated top issues. Use when the user wants a comprehensive multi-angle resume review, asks for a "panel review", "full review", "multi-angle review", or wants every reviewer to weigh in at once. Covers ATS parsing, recruiter triage, hiring manager, technical screener, bar raiser, staff IC peer, leveling committee, skip-level exec, domain SME, typography, future-self skeptic, and career coach perspectives.
allowed-tools: Read, Grep, Glob, Agent
---

# Resume Panel Review

Run a parallel fan-out of all 12 reviewer sub-agents defined in `.claude/agents/` against `will_cygan_resume.typ`, then synthesize their outputs into a single dashboard.

## Process

1. **Fan out.** In a single message, launch all 12 sub-agents in parallel using the Agent tool — one call per persona. Use the spawn prompt in `REFERENCE.md § Spawn Prompt`.

2. **Collect.** As each returns, record its verdict, confidence, top issue, and line references in the summary table.

3. **Tally consensus.** Count the verdicts across all 12. Identify the dominant verdict and any dissenters.

4. **Highlight dissent.** For each persona whose verdict disagrees with the majority, quote their strongest reason. Dissent is high-signal — surface it, don't average it away. If all 12 agree, say so explicitly.

5. **Deduplicate issues.** Merge top issues from all 12 into a ranked list of 10 max. Weight by cross-persona support (more personas raising the same issue = higher priority) and severity. A single strong technical-depth concern from `domain-sme-systems` may still rank above a broader but shallower complaint.

6. **Emit the dashboard.** Use the output format in `REFERENCE.md § Dashboard Format`.

## Notes

- The 12 sub-agents are defined in `.claude/agents/` and already know which `/advice/*.md` files to cite. You do not need to brief them on knowledge.
- Expect sub-agent outputs to be noisy. Synthesize aggressively — 10 consolidated issues is the cap, not the target.
- Recommend a follow-up skill or command at the end of the dashboard based on the consolidated issues (e.g., `/resume-panel-focus`, `/resume-debate`, or a tactical skill from `resume-optimizer`).

See `REFERENCE.md` for the full persona roster, the exact spawn prompt, and the output template.
