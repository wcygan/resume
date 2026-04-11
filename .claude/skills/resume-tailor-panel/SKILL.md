---
name: resume-tailor-panel
description: Run a 4-persona panel targeted at a specific job description. Uses ats-parser, recruiter-triage, hiring-manager, and career-coach to evaluate will_cygan_resume.typ through the lens of the JD in $ARGUMENTS. Produces JD essentials extraction, keyword/stack gap analysis, and a prioritized tailoring action plan. Use when the user has a specific job posting and wants a rigorous multi-angle tailoring review — heavier than the single-voice tailor workflow in the resume-optimizer skill.
argument-hint: <job-description>
allowed-tools: Read, Grep, Glob, Agent, AskUserQuestion
---

# Tailoring Panel

Evaluate the resume against a specific job description using a 4-persona panel. Each persona reads the resume through a different tailoring lens, and their outputs merge into a single prioritized action plan.

## Process

1. **Validate input.** If `$ARGUMENTS` is empty or clearly not a full JD (single word, bare URL with no extracted text), stop and use AskUserQuestion to request the full JD text. Do not proceed with guesses.

2. **Extract JD essentials yourself first.** Before fanning out, pull out the fields in `REFERENCE.md § JD Essentials Extraction`. Include this extraction in the context you pass to every persona so all 4 are working from the same interpretation of the posting.

3. **Fan out the 4 personas in parallel.** Single Agent tool message, 4 calls. Each persona gets: (a) the resume path, (b) the JD essentials extraction, (c) the full JD text, (d) the persona-specific framing prompt from `REFERENCE.md § Per-Persona Framing`.

4. **Consolidate.** Merge the outputs into the tailoring plan defined in `REFERENCE.md § Output Format`. Deduplicate findings that multiple personas raised; weight repeated concerns higher in the action plan.

## Notes

- There is already a simpler `tailor` workflow inside the `resume-optimizer` skill that runs a single-voice tailoring pass. Use this skill when the user wants a more rigorous multi-voice read or when the stakes warrant 4 perspectives instead of 1.
- The 4 personas selected (ATS parser, recruiter, hiring manager, career coach) specifically cover the keyword pass, the sourcing scan, the team-fit read, and the positioning alignment. Do not add bar-raiser or technical-screener here — those are out of scope for tailoring.

See `REFERENCE.md` for the JD extraction protocol, per-persona prompts, and output template.
