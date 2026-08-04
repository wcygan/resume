# Evidence register

This register identifies which sources can support which claims. It is a
routing index, not a collection of universal resume laws.

## Direct project evidence

| Source | Type | Supports | Limitations |
| --- | --- | --- | --- |
| `will_cygan_resume-data.json` | authoritative project artifact | Current resume wording and included facts | Does not prove that every claim is externally verified |
| `will_cygan_resume.pdf` | rendered artifact | Actual hierarchy, density, page fit, and visible content | Must be rebuilt after source changes |
| `work-experience/*.md` | user-maintained supporting record | Project context, mechanism, status, metrics, and ownership | May include drafts, targets, or in-flight work; reconcile conflicts with the user |
| `work-experience/RELEVANCE.md` and per-project scores | user preference | Relative importance and intended positioning | A prior, not hiring research or factual verification |
| Extraction scripts, fixtures, and raw reports | local test evidence | Behavior of named tools and reviewed assertions under the recorded environment | Does not reproduce commercial ATS or predict hiring outcomes |

## External sources

| Source | Type | Useful claims | Limitations |
| --- | --- | --- | --- |
| [Greenhouse: Unsuccessful resume parse](https://support.greenhouse.io/hc/en-us/articles/200989175-Unsuccessful-resume-parse) | vendor documentation, verified 2026-08-05 | Greenhouse's stated parsing behavior and formatting failure modes | Does not document its full implementation or validate other ATS products |
| [Harvard FAS: Create impactful resumes and cover letters](https://careerservices.fas.harvard.edu/resources/hes-create-impactful-resumes-and-cover-letters/) | university career-services guidance, verified 2026-08-05 | Clear, direct, fact-based, tailored, readable content and communicating impact | Professional guidance, not causal callback research |
| [Tech Interview Handbook resume guide](https://www.techinterviewhandbook.org/resume/) | practitioner guidance | Engineering-resume organization and examples | Opinions may be audience-specific and can change; verify current page before precise attribution |
| [Engineering Resumes community](https://www.reddit.com/r/EngineeringResumes/) | community/practitioner source | Examples of recurring readability and content critiques | Anecdotal, self-selected, and not independent hiring-outcome evidence |
| [Chip Huyen: What we look for in a candidate](https://huyenchip.com/2023/01/24/what-we-look-for-in-a-candidate.html) | individual hiring perspective | One practitioner's view of demonstrated expertise, execution, and distinctive evidence | One person's context; do not generalize to all employers |

## Repository advice archive

`advice/` contains excerpts, summaries, and practitioner notes. Use those files
only after identifying their original source and source type. Similar advice
across copied notes is not independent confirmation when the notes repeat one
another or trace back to the same author.

Do not use unsourced exact statistics, recruiter scan-time claims, keyword
density targets, title multipliers, ATS scores, or callback predictions. To
promote any such claim into active guidance, record the primary source,
methodology, population, publication date, and material limitations here.

## Maintenance

For a time-sensitive external claim:

1. revisit the primary or vendor source;
2. record the verification date;
3. state exactly what it supports;
4. preserve limitations; and
5. remove or downgrade the claim when the source no longer supports it.
