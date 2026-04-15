// BROKEN: two-column layout places job titles in the left column and
// companies+dates in the right column. The naive pdftotext pass may
// read top-to-bottom column by column; pdftotext -layout preserves
// spatial order. This is the canonical reading-order scramble the
// spec's supporting evidence calls out ("Java XYZ Engineering
// College" — left-column skills merging with right-column education).
//
// Target assertion: either
//   - 4-job-contiguity (title/company/date no longer within 300 chars
//     in naive extraction because the left column is dumped first,
//     then the right), or
//   - 7-cross-extractor (job count / section order differs between
//     pdftotext and pdftotext -layout / tika).
//
// Expected collateral on assertion 2 is possible if the section
// headers themselves get reordered across columns. That is acceptable
// — it's the same underlying bug.

#set page(paper: "us-letter", margin: 0.6in)
#set text(font: "New Computer Modern", size: 10pt)

#align(center)[
  #text(size: 16pt, weight: "bold")[Jane Doe] \
  jane\@example.com
]

#v(0.3em)

= Work Experience

// Two-column layout: titles on the left, company+dates on the right.
// In the naive pdftotext pass this typically reads as:
//   Staff Engineer
//   Senior Engineer
//   Acme Corp
//   Jan 2022 -- Present
//   Globex
//   Jun 2019 -- Dec 2021
// which puts the Staff Engineer title nowhere near "Acme Corp" or
// the date range, breaking the 300-char contiguity window.
#grid(
  columns: (1fr, 1fr),
  column-gutter: 2em,
  row-gutter: 2em,
  [
    *Staff Engineer* \
    #v(6em)
    *Senior Engineer*
  ],
  [
    Acme Corp \
    Jan 2022 -- Present
    #v(4em)
    Globex \
    Jun 2019 -- Dec 2021
  ],
)

= Projects

*open-source-thing*: a library for doing the thing.

= Skills

Languages: Python, Go, Rust, Java

= Education

*State University* -- B.S. Computer Science, 2018
