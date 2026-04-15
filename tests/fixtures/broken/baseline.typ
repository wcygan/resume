// Clean skeleton — should pass every assertion against baseline.fixtures.toml.
// The broken/*.typ fixtures in this directory mutate exactly one line
// (or add one) from this file to exercise a specific failure mode.

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

- Led platform reliability initiative across three services.
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
