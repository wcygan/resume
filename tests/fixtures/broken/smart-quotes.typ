// BROKEN: body text contains U+2018/U+2019 smart quotes.
// Should fail assertion 6-mojibake (flagged chars present).
//
// Typst by default converts straight quotes to smart quotes in text
// mode. To keep the baseline clean we use the `smartquote: false`
// setting there; here we leave it enabled AND use explicit Unicode
// smart quotes so the defect is guaranteed regardless of Typst version.

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

- Led platform reliability initiative; shipped the \u{2018}phoenix\u{2019} rewrite.

*Senior Engineer* at Globex \
Jun 2019 -- Dec 2021

- Owned order-processing pipeline serving 2k QPS.

= Projects

*open-source-thing*: a library for doing the thing.

= Skills

Languages: Python, Go, Rust, Java

= Education

*State University* -- B.S. Computer Science, 2018
