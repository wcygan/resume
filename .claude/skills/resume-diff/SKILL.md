---
name: resume-diff
description: Before/after resume review. Compares working-tree will_cygan_resume.typ to a previous version (defaults to git HEAD, accepts any git ref or file path as $ARGUMENTS) and runs a 5-persona panel on both versions. Reports which issues the user's edits resolved, which remain, and which are new. Use when the user has just made edits and wants to know whether they improved the resume or introduced new problems, or when comparing two versions of the resume.
argument-hint: [git-ref]
allowed-tools: Read, Grep, Glob, Bash, Agent
---

# Resume Diff Review

Compare the working-tree resume to a previous version and run a focused panel on both to produce a Fixed / Still Present / New issue diff.

## Process

1. **Extract the "before" version.** See `REFERENCE.md § Git Extraction` for the exact commands and edge cases. Default to `HEAD` when `$ARGUMENTS` is empty.

2. **Stop if there's nothing to diff.** If the before and current versions are byte-identical, say so and return immediately. No panel run.

3. **Show the diff first.** Before spawning any sub-agents, output the actual diff of the changed regions so the user can see what changed. Keep it scoped to changed lines — don't dump unchanged context.

4. **Run the panel twice in parallel.** In a single Agent tool message, launch 10 sub-agents: the 5 reviewers in `REFERENCE.md § Panel Subset` × 2 versions (before and current). Use the spawn prompt in `REFERENCE.md § Spawn Prompt`.

5. **Build the diff.** For each persona, classify issues as Fixed, Still Present, or New using the logic in `REFERENCE.md § Diff Logic`. Track verdict deltas.

6. **Aggregate across personas and report.** Deduplicate issues that multiple personas raised. Use the output format in `REFERENCE.md § Output Format`.

## Notes

- This is the only skill in this set that needs Bash, because it has to call `git show` to extract the before version. Keep Bash usage scoped to the git extraction step — don't use it for anything else.
- Five personas, not twelve, because a diff is about showing *movement*, not exhaustive critique. Use `resume-panel` for exhaustive critique on a single version.
- If the user asks "did my edits help?", this is the skill to reach for.

See `REFERENCE.md` for the git extraction protocol, panel subset, diff logic, and output template.
