// Defect: a literal U+00AD soft hyphen is embedded in the bullet text. Under
// any reasonable line-wrap, or even without wrapping, pdftotext and Tika emit
// the U+00AD byte verbatim in the extracted text. Injecting the character
// directly (rather than relying on the Typst hyphenation engine) keeps the
// fixture deterministic across platforms — macOS and Linux Typst disagree on
// whether long invented words trigger auto-hyphenation, so a source-level
// soft hyphen is the only reliable regression signal.

#set page(paper: "us-letter", margin: 0.6in)
#set text(font: "New Computer Modern", size: 10pt)

#align(center)[
  #text(size: 16pt, weight: "bold")[Jane Doe] \
  jane\@example.com
]

#v(0.3em)

= Work Experience

*Staff Engineer* at Acme Corp \
Jan 2022 -- Present

- Led platform reliability across #"invol\u{AD}untary" churn workflows.
- Cut deploy time from 45 minutes to 6 minutes.

*Senior Engineer* at Globex \
Jun 2019 -- Dec 2021

- Owned order-processing pipeline serving 2k QPS.
- Reduced incident response from 30 min to 5 min median.

= Projects

*open-source-thing*: a library for doing the thing.

= Skills

Languages: Python, Go, Rust, Java

= Education

*State University* -- B.S. Computer Science, 2018
