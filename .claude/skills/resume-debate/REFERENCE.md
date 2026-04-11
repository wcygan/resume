# Debate Reference

## Debate Participants

All three sub-agents are defined in `.claude/agents/`.

- **`hiring-manager`** — argues from "is this bullet believable and tech-stack-relevant?" Defends bullets that read as real engineering work.
- **`bar-raiser`** — attacks round numbers, unfalsifiable claims, and ownership inflation. Looks for the gap between what a bullet implies and what the candidate could actually defend.
- **`future-self-skeptic`** — flags things that are technically true but framed to flatter; asks what future-you will wince at in 2 years.

## Bullet Resolution

If `$ARGUMENTS` is a line number or the phrase "line N":
- Read `will_cygan_resume.typ`
- Extract line N verbatim
- Use that as the bullet text

If `$ARGUMENTS` is bullet text (anything longer than a few characters, containing multiple words):
- Use it directly
- Do not try to locate it in the resume — the user may be debating a proposed rewrite that isn't in the file yet

If `$ARGUMENTS` is empty:
- Call AskUserQuestion with two options: (1) "I'll paste the bullet text" (2) "Use this line number"
- Do not proceed with a default

## Round Protocol

### Round 1 — Opening Critiques

Send to all 3 personas in a single parallel Agent tool message:

> The following bullet from `will_cygan_resume.typ` is under review:
>
> "[BULLET TEXT]"
>
> Evaluate it in your voice. Is it strong, borderline, or weak? Give your top 2 concrete reasons and (if applicable) the one question you'd ask to probe it. Do NOT propose rewrites yet — just the critique.

Collect the three responses before proceeding to round 2.

### Round 2 — Rebuttals

Send to each persona, now including the other two's Round 1 responses. Three parallel calls:

> Here is your previous critique of this bullet:
>
> "[YOUR ROUND 1]"
>
> Here are the critiques from the other two reviewers:
>
> Reviewer A: "[OTHER 1 ROUND 1]"
> Reviewer B: "[OTHER 2 ROUND 1]"
>
> Do you stand by your position, modify it, or concede? Respond with:
> 1. STANCE: hold / soften / concede
> 2. Your strongest counter-argument to at least one other reviewer
> 3. Whether you now believe the bullet is strong / borderline / weak
>
> Still no rewrites.

Collect the three responses before proceeding to round 3.

### Round 3 — Candidate Rewrites

Send to each persona, including rounds 1 and 2 from everyone. Three parallel calls:

> Given the debate so far, propose your single best rewrite of the bullet. One line. Keep it in Typst-compatible plain text. The rewrite should be defensible under your persona's standards while acknowledging valid points from the other reviewers.

Collect the three candidate rewrites.

## Synthesis Rules

- **Full consensus** — all 3 rewrites converge on the same core shape (same structure, same key numbers, same verbs) → present it as **the** consensus rewrite.
- **Majority consensus** — 2 of 3 rewrites converge → present the majority rewrite and note the dissenter's alternative with their reasoning.
- **Full disagreement** — all 3 diverge → present all 3 side-by-side. This is a valid outcome; disagreement between personas is information the user needs.

## Output Format

### Bullet Debate

**Bullet Under Review**

> [the bullet text, from will_cygan_resume.typ line N if applicable]

**Round 1 — Opening Critiques**

| Persona | Verdict | Strongest Reason | Probing Question |
|---|---|---|---|
| hiring-manager | strong/borderline/weak | ... | ... |
| bar-raiser | ... | ... | ... |
| future-self-skeptic | ... | ... | ... |

**Round 2 — Rebuttals**

| Persona | Stance | Counter-Argument | Updated Verdict |
|---|---|---|---|
| hiring-manager | hold/soften/concede | ... | ... |
| bar-raiser | ... | ... | ... |
| future-self-skeptic | ... | ... | ... |

**Round 3 — Candidate Rewrites**

- **hiring-manager's rewrite:** `[text]`
- **bar-raiser's rewrite:** `[text]`
- **future-self-skeptic's rewrite:** `[text]`

**Consensus**

One of: *full consensus*, *majority rewrite with dissent*, or *articulated disagreement*.

**Recommended Action**

State plainly which rewrite (if any) the user should adopt, and why.

- If consensus: *"Replace line N with the consensus text."*
- If majority: *"Consider the majority rewrite, but weigh the dissenter's alternative — it protects against [specific risk]."*
- If disagreement: *"This bullet involves a real judgment call. Choose based on which reviewer's standards matter most for your target roles."*
