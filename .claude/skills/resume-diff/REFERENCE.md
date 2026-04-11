# Resume Diff Reference

## Git Extraction

Resolve `$ARGUMENTS` as follows:

- **Empty** → compare against `HEAD` (the last committed version)
- **A git ref** (SHA, branch name, `HEAD~3`, tag) → compare against that ref
- **A file path** (absolute or relative, exists on disk) → compare against that file directly

To extract the "before" version from git:

```bash
git show <ref>:will_cygan_resume.typ > /tmp/resume-before.typ
```

Verify the file was written and is non-empty. If `git show` fails (ref doesn't exist, file wasn't in that commit), report the failure clearly and stop.

## Byte-Equal Guard

Before running any sub-agents, diff the before file and the current working-tree resume. If they're byte-identical, say *"no changes between these two versions — nothing to diff"* and stop. Do not waste 10 sub-agent calls on an empty diff.

## Raw Diff

Generate a human-readable diff of only the changed regions:

```bash
diff -u /tmp/resume-before.typ will_cygan_resume.typ
```

Or equivalently `git diff --no-index`. Include this in the output before the panel results.

## Panel Subset (5 personas)

- `hiring-manager`
- `bar-raiser`
- `staff-ic-peer`
- `ats-parser`
- `career-coach`

These cover screening, scrutiny, peer calibration, mechanical checks, and narrative — broad enough to detect regressions without the full 12-persona overhead.

## Spawn Prompt

Send to each persona twice (once per version). All 10 calls go in a **single** parallel Agent tool message:

> Review the resume at `<path>`. Produce your standard output: VERDICT, CONFIDENCE, TOP ISSUES (with line refs), WHAT'S WORKING. Cap at 5 issues.

Use `/tmp/resume-before.typ` for the before calls and `will_cygan_resume.typ` for the current calls.

## Diff Logic

For each persona, compare their before-issues list to their current-issues list:

- **Fixed** — issue appeared in before, not in current
- **Still Present** — issue appeared in both (compare by semantic match, not exact string)
- **New** — issue appeared in current, not in before

Aggregate across all 5 personas. Deduplicate issues that multiple personas raised by merging them and listing all personas that flagged the issue.

Track each persona's verdict shift:
- *up* — borderline → advance, or reject → borderline/advance
- *down* — advance → borderline/reject, or borderline → reject
- *flat* — no change

## Output Format

### Resume Diff Review: [before ref] → working tree

**What Changed**

One sentence summarizing the diff — e.g., *"Rewrote 3 bullets in the current role and tightened the skills section."*

**Raw Diff**

```diff
[actual diff output, scoped to changed regions]
```

**Verdict Delta**

| Persona | Before | After | Moved? |
|---|---|---|---|
| hiring-manager | borderline | advance | ↑ up |
| bar-raiser | reject | borderline | ↑ up |
| staff-ic-peer | ... | ... | ... |
| ats-parser | ... | ... | ... |
| career-coach | ... | ... | ... |

**Fixed** (issues your edits resolved)

1. [issue] — was raised by: [persona names] — now gone
2. ...

**Still Present** (issues your edits did not touch)

1. [issue] — still raised by: [persona names] — [line refs in current version]
2. ...

**New** (issues your edits introduced)

1. **[severity]** [issue] — raised by: [persona names] — [line refs]
   Suggestion: [fix]
2. ...

**Net Score**

- Fixed: N issues
- Still Present: M issues
- New: K issues
- **Net change: (N − K) issues resolved**

**Recommendation**

One sentence on whether the edits were net positive and what to tackle next.
