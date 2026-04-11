---
name: resume-interview-rehearsal
description: Generate a ranked interview prep sheet from the resume. Three interviewer personas (hiring-manager, bar-raiser, domain-sme-systems) each generate 5 questions they would ask based on specific resume bullets. The questions are then deduplicated and ranked by difficulty tier (softball, standard, hard, trap). Includes a coverage audit flagging bullets no persona asked about. Optionally accepts a job description as $ARGUMENTS to target the questions for a specific role. Use when the user has an interview coming up, asks for interview prep, or wants to rehearse what they'd be asked about their resume.
argument-hint: [job-description]
allowed-tools: Read, Grep, Glob, Agent
---

# Interview Rehearsal

Generate a ranked interview question set from the resume by having three interviewer personas each propose questions, then merge, deduplicate, rank, and audit coverage.

## Process

1. **Generate questions in parallel.** Launch the 3 interviewer sub-agents in a single Agent tool message. Each generates exactly 5 questions grounded in specific lines of the resume. Use the prompt in `REFERENCE.md § Question Generation Prompt`. Pass `$ARGUMENTS` as target-role context if non-empty.

2. **Deduplicate and merge.** When two personas target the same bullet with essentially the same question, keep the more specific or harder version and attribute it to both personas.

3. **Rank by difficulty.** Apply the tiers in `REFERENCE.md § Difficulty Tiers`.

4. **Coverage audit.** Scan the resume for bullets with big numbers, big ownership claims, or strong impact verbs. Any such bullet that no persona asked about is a coverage gap — flag it explicitly. See `REFERENCE.md § Coverage Audit`.

5. **Emit the prep sheet.** Use the format in `REFERENCE.md § Prep Sheet Format`.

## Notes

- This is a prep tool, not a review tool. The output is questions for the candidate to rehearse answers to — not feedback on the resume itself.
- Every question MUST be grounded in a specific line of the resume. Reject generic questions ("tell me about yourself", "what's your biggest weakness") — those aren't what this skill is for.
- If `$ARGUMENTS` contains a job description, the personas should generate questions weighted toward the JD's responsibilities and tech stack.

See `REFERENCE.md` for the generation prompt, difficulty tiers, coverage audit protocol, and output template.
