---
name: resume-debate
description: Structured 3-round debate about a single resume bullet. Runs hiring-manager, bar-raiser, and future-self-skeptic through opening critique, rebuttal, and rewrite rounds. Produces either a consensus rewrite or an articulated disagreement for the user to adjudicate. Accepts either the bullet text or a line number as $ARGUMENTS. Use when the user is uncertain about a specific bullet, asks "is this bullet good?", wants multiple perspectives on one line, or says a reviewer flagged a specific bullet.
argument-hint: <bullet-text-or-line-number>
allowed-tools: Read, Grep, Glob, Agent, AskUserQuestion
---

# Bullet Debate

Orchestrate a 3-round structured debate between three personas about a single resume bullet, then synthesize the result.

## Process

1. **Resolve the bullet.** If `$ARGUMENTS` is a line number (e.g., `34`, `line 34`), read `will_cygan_resume.typ` and extract that line. If it's a full bullet text, use it directly. If `$ARGUMENTS` is empty, use AskUserQuestion to prompt for either a line number or the bullet text.

2. **Run the 3 rounds.** Each round is a single parallel Agent tool message with 3 calls (one per persona). See `REFERENCE.md § Round Protocol` for the exact prompts to send at each round. Rounds are sequential — round 2 depends on round 1's output, round 3 depends on rounds 1 and 2.

3. **Synthesize.** Compare the 3 candidate rewrites from round 3. Apply the synthesis rules in `REFERENCE.md § Synthesis Rules`.

4. **Report.** Use the output format in `REFERENCE.md § Output Format`.

## Agent teams note

If the user wants the three personas to truly argue in real time via SendMessage (rather than sequential rounds), that requires setting `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` and using TeamCreate. The default here is the sequential sub-agent approach — it works today, is deterministic, and produces the same debate structure.

## Notes

- Full disagreement is a valid outcome. If the three personas cannot converge after round 3, present all three rewrites side-by-side and let the user decide. Do not force consensus.
- Keep each round's prompts terse. Long prompts lead to long sub-agent responses that dilute the debate.

See `REFERENCE.md` for the round protocol, synthesis rules, and output template.
