# Interview Rehearsal Reference

## Interviewer Personas (3)

All defined in `.claude/agents/`.

- **`hiring-manager`** — asks about fit, motivation, tech-stack overlap, and collaboration. Questions that reveal whether the candidate can do the work and work with the team.
- **`bar-raiser`** — asks questions designed to probe inflation. "Walk me through exactly how you did X." "What was your specific contribution vs. the team's?" "Why this number and not that one?" Questions that reveal whether claims survive scrutiny.
- **`domain-sme-systems`** — asks technical deep-dive questions on any distributed-systems claims in the resume. Questions that reveal whether the candidate understands mechanisms, not just vocabulary.

## Question Generation Prompt

Send to all 3 personas in a single parallel Agent tool message. If `$ARGUMENTS` is non-empty, splice it in as target-role context.

> You are preparing for an interview with this candidate. Read `will_cygan_resume.typ`.
>
> [If $ARGUMENTS is non-empty:] The target role is described in this job description: "[$ARGUMENTS]". Weight your questions toward the role's responsibilities and tech stack.
>
> Generate exactly 5 questions you would ask this candidate, in your persona's voice. For each question, include:
>
> 1. The question itself (exact wording)
> 2. The line or bullet from the resume that prompted it
> 3. The one-line reason you're asking it
> 4. What a strong answer would include (3 bullets)
>
> Do NOT generate generic questions. Every question must be grounded in a specific part of this resume.

Expect 15 questions total (5 per persona). Collect all three before deduplication.

## Deduplication

Two questions are "essentially the same" if they target the same bullet and probe the same underlying claim. When you find a duplicate:

- Keep the more specific or harder phrasing
- Attribute it to both personas
- Preserve the union of the "what a strong answer includes" bullets from both

After dedup, expect 10-14 unique questions.

## Difficulty Tiers

Rank every merged question into one of four tiers:

- **Softball** — surface-level, expected, easy to rehearse. Examples: "Tell me about your work on X project." "What was your role on the team?"
- **Standard** — reasonable depth, testable with a good story. Examples: "Walk me through how you decided on Kafka for this use case." "How did you measure the 40% latency improvement?"
- **Hard** — requires deep understanding of the specific work; hard to bluff. Examples: "What were the trade-offs between sticky sessions and distributed locks for maintaining consistency?" "Why did you choose Spark over Flink for the deletion pipeline?"
- **Trap** — designed to catch inflation; wrong answer reveals the bullet was overclaim. Examples: "Who else was on the team that built X?" "What would the post-mortem say about your specific contribution?"

## Coverage Audit

After ranking, scan the resume again for bullets with any of these high-stakes markers:

- Large dollar figures (`$2M`, `$10M`, etc.)
- High QPS or throughput numbers (`100,000+ QPS`, `50TB+ weekly`)
- Strong ownership verbs (`architected`, `led`, `drove`, `spearheaded`)
- Large team/adoption claims (`12 teams adopted`, `10M+ users`)
- Latency/performance deltas (`86% reduction`, `40% improvement`)

Any such bullet that no persona asked about is a **coverage gap**. Explicitly flag it. Those are the bullets most likely to be probed in a real interview loop, so a gap in the rehearsal is a real risk.

## Prep Sheet Format

### Interview Rehearsal Prep Sheet

**Scope:** [generic interview | interview for target role: "[role title]"]
**Personas Generating Questions:** hiring-manager, bar-raiser, domain-sme-systems
**Total Questions:** N (after deduplication)

---

**Question Set — Ranked by Difficulty** (hardest first)

For each question, present:

---

**Q[#]** — Difficulty: [softball | standard | hard | trap]
**Asked by:** [persona name(s)]
**Question:** "[exact question text]"
**What bullet it probes:** line N — *"[quoted phrase from the resume]"*
**Why they're asking:** [one line]
**What a strong answer includes:**
- [bullet 1]
- [bullet 2]
- [bullet 3]

---

**Coverage Gaps**

Bullets on the resume that no persona asked about but probably should have. For each, include the line number, quote the claim, and one sentence on why it's likely to be probed in a real loop.

**Top 5 to Drill**

The five highest-priority questions in priority order. Copy them as a compact drill list the user can practice from directly.

**Rehearsal Strategy**

One paragraph on how to use this prep sheet. General guidance: rehearse trap questions first (wrong answers actively damage you), hard questions second (you can't bluff your way through these), standard questions third (these are the most common), softballs last (handle on instinct).
