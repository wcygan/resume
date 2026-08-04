# Typst implementation patterns

Load the current `typst-author` skill before writing or changing Typst. Confirm
syntax and export behavior against its local documentation, then format and
compile according to that skill.

## Contents

- Semantic baseline
- Experience, education, skills, and contact contracts
- Export and post-edit validation

## Semantic baseline

Build the resume from semantic elements in normal flow:

- one level-1 heading for the candidate name when appropriate;
- level-2 headings for sections;
- native lists for accomplishments;
- real links with human-readable visible text;
- sequential content blocks for each record; and
- direct text for all canonical facts.

Prefer global defaults equivalent to:

```typst
#set text(lang: "en", hyphenate: false)
#set par(justify: false)
#set heading(numbering: none)
```

Verify these against the installed Typst version before using them in a target
document.

## Experience entry contract

A robust entry macro should accept semantically named arguments:

```text
company
date range
role
location
accomplishments
```

Emit those fields once, contiguously, and in the declared source order. Do not
repurpose a generic `description` field for employer, degree, or another fact
whose meaning changes by section.

The tested right-aligned golden entry used:

- an unbreakable normal-flow block;
- company and role together on the left of one metadata row;
- one labeled `Dates:` and `Location:` unit flush-right on that row;
- flexible horizontal spacing only inside that single bounded row; and
- a native list immediately after the metadata.

The source-order contract matters more than the visual row count. Validate the
compiled output before adopting the component elsewhere.

A representative construction is:

```typst
#box(width: 100%)[
  #organization(company)
  #h(0.45em) — #h(0.45em)
  #role-title(role)
  #h(1fr)
  #text(fill: muted)[
    Dates: #dates #h(0.45em) · #h(0.45em) Location: #location
  ]
]
```

This is not a universal macro: long real company names, roles, dates, or
locations can collide or wrap. The Golden renderer now measures the complete
left and right units before layout. It keeps both on one row when they fit and
otherwise places the complete labeled right unit on the next line, still
right-aligned and still after the left unit in source order. Never allow a
`Dates:` or `Location:` label to wrap away from its value. Accept same-row
geometry only with positive clearance; accept the fallback only when the
right unit is below the left baseline, inside the content width, and shares the
reviewed right edge. Derive the content box from the page width and declared
margins; comparing the two text groups only to each other can miss consistent
off-page overflow.

## Education and skills

Keep short education facts in adjacent normal flow:

```text
University name
Graduation: May 2016
Bachelor of Science, Computer Science
```

Avoid independently right-aligning the graduation date unless an extractor
oracle proves it remains inside the Education boundary.

Prefer skills as labeled flow rows:

```text
Core Languages: Python, TypeScript, SQL, Rust
Technology Focus: Distributed services, event pipelines, observability
```

A compact skills table may be accepted conditionally after direct testing. A
grid is not a good default for job metadata.

## Profile and projects

Keep a Profile as ordinary normal-flow prose immediately after a true heading.
Do not place it in a page header, floating box, or occupied sidebar, and do not
use hidden keywords to supplement the visible paragraph.

Use a dedicated project function rather than forcing project facts into an
experience function with fabricated employer, date, or location fields. The
tested Golden project uses:

- one unbreakable normal-flow block;
- project name and plain-language descriptor together on the left;
- one labeled `Focus:` unit on the right of the same row;
- a native list immediately after the metadata; and
- a Projects boundary before Education.

This mirrors the visual hierarchy of Experience without pretending that a
project is employment. If a repository or portfolio link is included, keep
human-readable display text visible, label it when its purpose is ambiguous,
create one real link annotation, and add its destination to the reviewed URI
multiset. Re-test the row after any longer project name, descriptor, focus
text, font, or size change.

## Contact block

Place contact content in the document body, even if it is visually aligned at
the top. Include canonical, readable display values and real link destinations.
Labels are optional for self-identifying values such as email addresses and
LinkedIn or GitHub domains; retain a label when the destination's purpose would
otherwise be ambiguous. Do not use the page `header` or a floating box as the
only source of contact facts.

The visible value and URI destination are separate evidence. Test both.

Treat each visible URL as one indivisible flow unit. Measure the complete
contact row; when it does not fit, let whole URL units wrap into additional
centered rows rather than splitting a domain or path. This is a presentation
fallback, not permission to duplicate destinations or alter the URI multiset.

When the candidate has explicitly supplied verified citizenship, work
authorization, or sponsorship facts, emit the chosen statement once as direct,
visible body text after the contact links and before the first resume section.
Do not put it in a page header, floating element, icon, hidden text, or Profile
paragraph. The Golden contract verifies the exact statement between LinkedIn
and Profile in every extraction view. Do not infer these facts when adapting the
template for another person.

## Export

Compile normally with tags enabled. For an additional standards check:

```sh
typst compile --root "$repo_root" --pdf-standard ua-1 \
  "$source_typ" "$resume_pdf"
```

Do not use `--no-pdf-tags` for a deliverable. Typst's PDF documentation says
tags are enabled by default and disabling them makes the file inaccessible to
tag-dependent consumers.

## Post-edit validation

After every meaningful `.typ` change:

1. follow `typst-author` formatting checks;
2. compile the intended deliverable;
3. run the repository extraction gate;
4. compare raw extractor outputs when the layout changed;
5. audit tags, fonts, images, links, and qpdf integrity for structural changes;
6. render and inspect every page; and
7. confirm the reviewed oracle and association windows still pass.
