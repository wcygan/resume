# Controlled experiments

Use experiments to answer causal questions such as "Does this one Typst
primitive change extraction?" A varied collection of resumes is a challenge
set, not a causal experiment.

## Experiment contract

Record before compiling:

```text
Question:
Baseline source and PDF hash:
One primary variable:
Facts held constant:
Reviewed oracle and association windows:
Expected mechanism:
Compiler flags:
Tool versions and environment:
Pass, Conditional, and Fail gates:
Negative or positive control:
Output directory:
```

## Procedure

1. Create one semantic-flow baseline with synthetic but realistic facts.
2. Centralize factual content so variants cannot drift silently.
3. Change one narrowly named structural or export variable per variant.
4. When a full resume introduces interactions, create a micro-probe that
   isolates the target phrase or ordering behavior.
5. Compile every run with the same compiler, fonts, root, and environment.
6. Preserve compiler logs, PDFs, raw text/XML/XHTML, PDF audits, QDF, and
   renders for each run.
7. Compute observed gates from evidence. Do not copy an expected label into the
   actual result.
8. Compare raw evidence first, then the strictly bounded canonical view.
9. Inspect the render; geometry controls can fail even when marker counts pass.
10. Report interactions and failed controls instead of forcing a causal story.

## High-value probes

- semantic headings versus bold-only labels;
- native lists versus literal bullet blocks;
- tags enabled versus `--no-pdf-tags`;
- normal export versus PDF/UA-1;
- hyphenation off versus on around one forced wrap;
- sequential flow versus a grid for the same metadata;
- source order aligned with coordinates versus deliberately conflicting
  absolute coordinates;
- body-held contact versus page-header contact;
- one column versus two occupied columns; and
- visible canonical text versus a hidden duplicate negative control.

## Content-length stress matrices

Template robustness needs a second experiment type: hold the renderer, fonts,
compiler flags, and base facts constant while substituting one unusually long
value. Keep canonical content in data, not duplicated Typst sources. Define
each case as explicit reviewed data and oracle patches with the old value as a
precondition, then compile the same fixture adapter with a data-path input.

The Golden matrix covers long company, role, location, date, contact URL, and
project metadata values plus a combined-pressure case. Deliberately
unbreakable company and location tokens are negative controls. Freeze hashes
for the fixture adapter, renderer, base data, and base oracle, and recheck them
around every compilation so stale patches or concurrent drift stop the run
before evidence is interpreted.

For every case, preserve the materialized data and oracle, compile command,
Typst dependency list, hashes, PDF, raw extractor outputs, geometry results,
page count, and renders for every page. A supported case passes only when the
deep oracle and PDF gates pass and the result stays within the declared page
budget. A negative control succeeds only when its failed-gate set exactly
matches the reviewed expectation; an unexpected pass or collateral failure is
a control malfunction.

## Oracle design

Use unique synthetic values where possible. For each entity, define:

- fields expected exactly once;
- canonical order;
- the next entity or section boundary; and
- expected URI destinations.

Test jobs, education, and skills. An evidence span somewhere on the page is not
enough.

## Isolation failure to avoid

The manual-bullet experiment initially changed more than bullet semantics. It
had to be corrected to reuse baseline metadata, add only the required paragraph
break, and replace native list items with literal bullet blocks. Even then, a
Poppler metadata association failed. The correct conclusion was an interaction
failure in the full construction, not "manual bullets are always bad."

## Evidence directory safety

Write generated evidence only below a deliberate new or empty directory. A
safe default is `mktemp -d`. Reject `/`, the repository root, and non-empty
user directories. Do not delete broad paths during cleanup.

## Classification

- Pass only when all declared positive gates pass.
- Fail a negative control when the intended defect is detected; that is a
  successful experiment but a failing resume pattern.
- Use Conditional for tool-dependent behavior or retained content with missing
  semantics.
- Mark a control malfunction explicitly when its expected defect was not
  observed.
- Preserve residual uncertainty and never promote local results into vendor or
  hiring claims.
