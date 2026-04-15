// BROKEN: body text contains U+2018/U+2019 smart quotes (explicit Unicode
// to guarantee the defect regardless of Typst's smartquote setting).

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

- Led platform reliability across involuntary churn; shipped \u{2018}phoenix\u{2019} rewrite.

*Senior Engineer* at Globex \
Jun 2019 -- Dec 2021

- Owned order-processing pipeline serving 2k QPS.

= Projects

*open-source-thing*: a library for doing the thing.

= Skills

Languages: Python, Go, Rust, Java

= Education

*State University* -- B.S. Computer Science, 2018
