# Tailoring Panel Reference

## Panel (4 personas)

All defined in `.claude/agents/`.

- `ats-parser` — scores keyword and title match against the JD; reports missing keywords and title-match risk
- `recruiter-triage` — evaluates the sourcing scan against the JD's search criteria
- `hiring-manager` — grades tech-stack overlap, flags bullets that need rewriting to mirror JD language
- `career-coach` — evaluates whether the resume's positioning aligns with or fights against what the JD is selling

## JD Essentials Extraction

Before spawning any persona, extract these fields from the JD yourself:

- **Target Title** — the exact role title on the posting (matters for ATS title-match)
- **Top Keywords** — 5-7 technologies, frameworks, and concepts that appear prominently
- **Seniority Level** — junior / mid / senior / staff / principal (inferred from years and responsibilities)
- **Key Responsibilities** — top 3-5 responsibility bullets
- **Hard Requirements** — years of experience, clearance, degree, location, visa

Include this full extraction (plus the verbatim JD text) in every persona's prompt so they can verify your extraction and work from the same baseline.

## Per-Persona Framing

Prepend each persona's standard prompt with your JD extraction and the full JD text, then append the persona-specific framing:

- **ats-parser:**
  > Score this resume's keyword and title match against the JD I'm giving you. Report missing keywords (ranked by JD prominence) and any title-match risk. Use your standard output format (VERDICT, CONFIDENCE, TOP ISSUES, WHAT'S WORKING).

- **recruiter-triage:**
  > Imagine you're sourcing for the role described in this JD. Would you forward this resume to the hiring manager after a 10-second scan? Use your standard output format.

- **hiring-manager:**
  > Imagine this JD is for a role on your team. Evaluate the resume for tech-stack overlap and tailor-fit. Identify specific bullets that need rewriting to align with the JD's language. Use your standard output format.

- **career-coach:**
  > Evaluate whether this resume's current positioning aligns with what this JD is selling. Identify narrative gaps between the resume's story and the role's story. Use your standard output format.

All 4 calls go in a single parallel Agent tool message.

## Output Format

### Tailoring Panel Review for: [Target Job Title]

**Job Description Essentials**

- **Target Title:** ...
- **Top Keywords:** ...
- **Seniority:** ...
- **Key Responsibilities:** ...
- **Hard Requirements:** ...

**Panel Consensus:** [strong fit | fit with gaps | weak fit | no fit]

**Per-Persona Summary**

| Persona | Verdict | Top Finding |
|---|---|---|
| ats-parser | ... | ... |
| recruiter-triage | ... | ... |
| hiring-manager | ... | ... |
| career-coach | ... | ... |

**Gap Analysis**

| Category | What JD Wants | What Resume Has | Gap |
|---|---|---|---|
| Keywords | [top 5 from JD] | [match status each] | ... |
| Tech Stack | [required] | [overlap] | ... |
| Scope / Level | [implied level] | [resume's effective level] | ... |
| Positioning | [role's story] | [resume's story] | ... |

**Prioritized Tailoring Actions** (ranked by impact × effort)

1. **[severity]** [specific action] — flagged by: [persona name(s)]
   - Original line (if applicable): [quote]
   - Suggested revision: [rewrite]
2. ...

**Should You Apply for This Role?**

One-sentence verdict: *yes / yes with tailoring / only if strategically worth it / no*.
