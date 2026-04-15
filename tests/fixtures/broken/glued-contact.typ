// BROKEN: name and email touch (no whitespace/newline between them).
// Should fail assertion 3-name-contact (glue detected).

#set page(paper: "us-letter", margin: 0.6in)
#set text(font: "New Computer Modern", size: 10pt)

// Forcing name and email into the same run with no separator. Modeling
// the "two floating text boxes got merged by the PDF text stream"
// failure mode.
#align(center)[
  #text(size: 16pt, weight: "bold")[Jane Doe]#text(size: 10pt)[jane\@example.com]
]

#v(0.3em)

= Work Experience

*Staff Engineer* at Acme Corp \
Jan 2022 -- Present

- Led platform reliability initiative across three services.

*Senior Engineer* at Globex \
Jun 2019 -- Dec 2021

- Owned order-processing pipeline serving 2k QPS.

= Projects

*open-source-thing*: a library for doing the thing.

= Skills

Languages: Python, Go, Rust, Java

= Education

*State University* -- B.S. Computer Science, 2018
