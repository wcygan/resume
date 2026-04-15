# Bootstrap Skeletons

Starters for authoring a new in-house template (Workflow B). Pick the closest fit, copy into `template/<name>.typ`, then trim or extend. All skeletons assume typst 0.13+.

## Conventions across all skeletons

- Public function names should be **prefixed** with the template name to avoid collisions when multiple templates are imported side-by-side (`cover-letter-block`, not `block`).
- Top-of-file comment: `// In-house template authored <YYYY-MM-DD> for <use case>.`
- Default to `paper-size: "us-letter"` for US audiences, `"a4"` otherwise.
- `fallback: true` on `set text(...)` — saves you from missing-font crashes.
- No speculative helpers. Add `resume-entry`-style functions only when the user asks.

---

## Skeleton: Resume (the default)

Used as the baseline for `template/modern-cv.typ`. One main template function, heading show rules, contact row, body.

```typ
// In-house template authored YYYY-MM-DD for resume/CV use.

#import "@preview/fontawesome:0.5.0": *

#let color-accent = rgb("#262F99")
#let color-body = rgb("#333333")
#let color-muted = rgb("#5d5d5d")

#let resume(
  author: (:),
  paper-size: "us-letter",
  accent-color: color-accent,
  body,
) = {
  set document(
    author: author.firstname + " " + author.lastname,
    title: "Résumé",
  )
  set text(
    font: ("Source Sans Pro", "Source Sans 3"),
    size: 11pt,
    fill: color-body,
    fallback: true,
  )
  set page(paper: paper-size, margin: (x: 15mm, y: 10mm))
  set par(spacing: 0.75em, justify: true)
  set heading(numbering: none, outlined: false)

  show heading.where(level: 1): it => [
    #set text(size: 16pt, weight: "regular", fill: accent-color)
    #strong[#it.body]
    #box(width: 1fr, line(length: 100%))
  ]

  align(center)[
    #text(size: 28pt, weight: "bold")[
      #author.firstname #author.lastname
    ]
  ]

  body
}
```

---

## Skeleton: Cover letter

Right-aligned heading block, salutation, body, signature.

```typ
// In-house cover-letter template authored YYYY-MM-DD.

#let cover-letter(
  author: (:),
  recipient: (:),
  date: datetime.today().display("[month repr:long] [day], [year]"),
  paper-size: "us-letter",
  body,
) = {
  set document(
    author: author.firstname + " " + author.lastname,
    title: "Cover Letter",
  )
  set text(font: ("Source Sans Pro",), size: 11pt, fallback: true)
  set page(paper: paper-size, margin: (x: 20mm, y: 20mm))
  set par(spacing: 1em, justify: true)

  align(right)[
    #text(weight: "bold", size: 14pt)[#author.firstname #author.lastname] \
    #if "email" in author [#author.email \ ]
    #date
  ]

  v(2em)

  if "name" in recipient [
    #recipient.name \
    #if "title" in recipient [#recipient.title \ ]
    #if "company" in recipient [#recipient.company \ ]
  ]

  v(1em)

  [Dear #if "name" in recipient { recipient.name } else { "Hiring Manager" },]

  body

  v(1em)
  [Sincerely,] \
  v(1em)
  [#author.firstname #author.lastname]
}
```

---

## Skeleton: Academic CV

Resume-shaped but expects multiple long-form sections (Publications, Grants, Teaching, Service). Minor tweaks: wider margins, smaller base font, section-entry helper.

```typ
// In-house academic-CV template authored YYYY-MM-DD.

#let color-accent = rgb("#1a3d7c")

#let academic-cv(
  author: (:),
  paper-size: "us-letter",
  body,
) = {
  set document(
    author: author.firstname + " " + author.lastname,
    title: "Curriculum Vitae",
  )
  set text(font: ("EB Garamond", "Source Serif Pro"), size: 10.5pt, fallback: true)
  set page(paper: paper-size, margin: (x: 18mm, y: 16mm))
  set par(spacing: 0.7em, justify: true, leading: 0.55em)
  set heading(numbering: none, outlined: false)

  show heading.where(level: 1): it => [
    #v(0.8em)
    #text(size: 12pt, weight: "bold", tracking: 1pt, fill: color-accent)[
      #upper(it.body)
    ]
    #line(length: 100%, stroke: 0.5pt + color-accent)
    #v(0.2em)
  ]

  align(center)[
    #text(size: 20pt, weight: "semibold")[#author.firstname #author.lastname] \
    #if "affiliation" in author { text(size: 10pt)[#author.affiliation] }
  ]

  body
}

#let academic-entry(title: "", venue: "", date: "", body) = {
  block(above: 0.8em, below: 0.6em)[
    #grid(
      columns: (1fr, auto),
      align: (left, right),
      strong(title), emph(date),
    )
    #if venue != "" { emph(venue) }
    #body
  ]
}
```

---

## Skeleton: Slide deck (touying)

Touying is the canonical modern slide framework. Keep the import; don't try to fork it.

```typ
// In-house slide template authored YYYY-MM-DD, built on touying.

#import "@preview/touying:0.5.5": *
#import themes.simple: *

#show: simple-theme.with(
  aspect-ratio: "16-9",
  footer: [My Deck],
)

#title-slide[
  = Title
  Will Cygan · YYYY-MM-DD
]

#slide[
  == Section

  - Point one
  - Point two
]
```

Pin `touying` to a tested version. Bumping touying majors is the #1 source of slide-template breakage.

---

## When to add helpers

Don't pre-populate with `<name>-entry`, `<name>-item`, `<name>-skill-row` functions. Each one is surface you'll have to maintain. Let the first real use of the template drive which helpers earn their place.
