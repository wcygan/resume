// BROKEN: both jobs use numeric dates (MM/YYYY) instead of "Mon YYYY".
// Should fail BOTH:
//   - assertion 4-job-contiguity (date_start tokens from baseline.fixtures.toml
//     — "Jan 2022", "Jun 2019" — no longer appear in the extracted text).
//   - assertion 5-date-format (no date range matches the month-name regex).
//
// Collateral on assertion 4 is expected here: a numeric date format
// necessarily changes the date tokens we search for. The test checks
// for assertion 5 specifically because that's the cleaner signal, and
// documents assertion 4 as acceptable collateral.

#set page(paper: "us-letter", margin: 0.6in)
#set text(font: "New Computer Modern", size: 10pt)

#align(center)[
  #text(size: 16pt, weight: "bold")[Jane Doe] \
  jane\@example.com
]

#v(0.3em)

= Work Experience

*Staff Engineer* at Acme Corp \
01/2022 - Present

- Led platform reliability initiative across three services.

*Senior Engineer* at Globex \
06/2019 - 12/2021

- Owned order-processing pipeline serving 2k QPS.

= Projects

*open-source-thing*: a library for doing the thing.

= Skills

Languages: Python, Go, Rust, Java

= Education

*State University* -- B.S. Computer Science, 2018
