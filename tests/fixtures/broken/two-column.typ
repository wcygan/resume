// BROKEN: two-column layout — titles on the left, companies/dates on the
// right — the canonical reading-order scramble.

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
