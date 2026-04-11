---
name: resume-panel-focus
description: Run a section-focused resume review panel. Routes to a curated subset of the 12 reviewer sub-agents based on the section argument (work-experience, skills, projects, formatting, narrative, or header). Faster and more targeted than a full panel — uses 3-6 relevant personas instead of all 12. Use when the user wants to review only a specific part of their resume, has just edited one section, or asks about one area like "the skills section" or "the formatting" or "my bullets".
argument-hint: <section>
allowed-tools: Read, Grep, Glob, Agent, AskUserQuestion
---

# Section-Focused Resume Panel

Route the section alias in `$ARGUMENTS` to a curated subset of reviewer sub-agents defined in `.claude/agents/`, fan out in parallel, and synthesize a focused report.

## Process

1. **Parse section argument.** Match `$ARGUMENTS` (case-insensitive) against the aliases in `REFERENCE.md § Section Routing`. If `$ARGUMENTS` is empty or matches no alias, use AskUserQuestion to prompt the user, listing the valid aliases.

2. **Fan out matched personas.** Launch them in parallel via a single Agent tool message. Use the spawn prompt in `REFERENCE.md § Spawn Prompt`.

3. **Collect and synthesize.** Build the focused report using the output format in `REFERENCE.md § Output Format`.

4. **Flag spillover.** If a persona's feedback reveals an issue that actually lives in a *different* section (e.g., `career-coach` says "the projects contradict the positioning in work experience"), note it briefly under "Spillover" — but do not expand scope.

## Notes

- This skill deliberately uses fewer personas than `resume-panel` so you get sharper, faster feedback when you know which section matters.
- The section-to-persona routing is opinionated: each section maps to the personas whose expertise is most relevant. Do not spawn personas outside the routing unless the user explicitly asks.

See `REFERENCE.md` for the full routing table, spawn prompt, and output format.
