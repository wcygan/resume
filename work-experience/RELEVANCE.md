# Relevance Score

Each project and major deliverable in `work-experience/*.md` carries a **Relevance Score** (1–5) plus a one-sentence rationale. The score is the author's judgment of how heavily this deliverable should weigh on a resume — independent of how it is currently represented in `will_cygan_resume-data.json`.

## Why this exists

Without a score, AI agents reviewing or rewriting the resume must *infer* importance from prose — a noisy signal that over-weights whatever happens to be quantified and under-weights mechanism-level work that's harder to condense into a line. The score is an explicit prior: it tells agents how the author ranks real-world impact, so cross-references against the resume can flag **buried leads** (high-RS material missing from the resume) and **wasted real estate** (low-RS material on it).

## Rubric

| RS | Label | Heuristic |
|----|-------|-----------|
| **5** | **Headline** — belongs on every resume | Quantified $M / QPS / scale *plus* org-wide scope *plus* technically defensible in a 30-minute deep-dive *plus* differentiating from peers at the same level. |
| **4** | **Strong supporting** — drop first only when space-constrained | Quantified with clear ownership; narrower scope than a headline; the candidate can defend its mechanism and attribution in depth. |
| **3** | **Solid filler** — fits tailored resumes | Credible accomplishment; targeted usefulness when JD keywords match; strengthens but is not essential. |
| **2** | **Interview-story only** — weak as a resume bullet | Real work, useful for conversation; vague or undifferentiated impact; hard to quantify compellingly in one line. |
| **1** | **Log-only** — do not surface | Raw-material value only; captured here for trajectory; scoped out of external positioning. |

## Field format

Add as the **last** field in every `### [Project name]` entry under Section 3 (Projects & Initiatives):

```markdown
- **Relevance:** N/5 — <one sentence: the specific fact(s) that justify this level>
```

Examples (drawn from the LinkedIn logs):

- `**Relevance:** 5/5 — $2M+ annualized revenue + 100K QPS read path + commerce-critical alerting surface with 3 partner-team extensions.`
- `**Relevance:** 4/5 — 37%/40% p95/avg latency wins on a 20B-row / 12TB backend; strong but narrower than the migration itself.`
- `**Relevance:** 3/5 — Company-wide gRPC migration shipped across 4 production services; useful on JDs that emphasize service modernization.`
- `**Relevance:** 2/5 — Shipped and reliable, but impact is internal-tooling convenience — hard to quantify compellingly in one line.`

## Scoring heuristics

- **When in doubt, go lower.** A resume is scarcity-driven; over-rating inflates noise and defeats the whole point of the prior.
- **Quantify the rationale.** "It was important" is not a rationale — `$2M + 10 teams + 100K QPS` is.
- **Re-score after milestones.** A project's RS can rise (scope expanded, another team adopted) or fall (a replacement shipped, impact didn't stick). Annotate when it changes.
- **Score the project, not the bullet.** One project may yield several bullet variants on the resume; the score attaches to the underlying work. If an RS-5 project is phrased weakly on the resume, the fix is rewrite, not re-score.
- **Section 4 (Performance, Reliability & Cost) items are unscored by default.** They're typically interview-story material; score only when one rises to project-level impact (e.g., the JVM / GC tuning work in `01-linkedin-swe.md` arguably warrants a score).
- **In-flight work is scorable.** Score against *expected* impact and tag the uncertainty: `**Relevance:** 4/5 (in-flight — will rise to 5 if the 33% reduction lands as scoped).`

## How resume review uses it

The project-local `$resume-review` skill treats the score as a **calibration prior, not gospel**:

- **Buried-lead flag.** An RS 5/4 project missing from or weakly represented in `will_cygan_resume-data.json` is a high-priority issue — cite the `work-experience/*.md` line.
- **Real-estate flag.** RS 2/1 project appearing on the resume is low-priority content that could be cut in favor of higher-RS material.
- **Interview prep weighting.** Coverage gaps on high-RS bullets are more severe than gaps on low-RS bullets (a question-generation pass should prioritize RS 5/4 material).
- **Disagreement is signal.** If a reviewer thinks an RS 5 is inflated or an RS 3 is under-rated, it must say so explicitly. That is cheap calibration for the author — the author can re-score or leave it as a documented minority view.

## FAQ

**Do personal projects get scored?** Yes. `work-experience/99-personal-projects.md` uses the same rubric.

**What about roles pre-LinkedIn if we ever backfill them?** Same rubric. The score is a property of the deliverable, not the employer.

**Should the resume itself (`will_cygan_resume-data.json`) carry scores?** No. The resume is the distilled artifact; scores live on the raw log so reviewers can compare the two.
