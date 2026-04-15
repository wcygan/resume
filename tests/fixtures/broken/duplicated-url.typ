// Defect: the same URL is used as the link target for multiple visible labels.
// Tika dedupes on the target URL in its trailing URL block; this fixture emits
// the same URL three times in extracted output, tripping 10-url-dedup.

#set page(paper: "us-letter", margin: 0.6in)
#set text(font: "New Computer Modern", size: 10pt)

#align(center)[
  #text(size: 16pt, weight: "bold")[Jane Doe] \
  jane\@example.com
]

#v(0.3em)

= Work Experience

#link("https://example.com/profile/jane")[*Staff Engineer*] at Acme Corp \
Jan 2022 -- Present

- Led platform reliability initiative across three services.

#link("https://example.com/profile/jane")[*Senior Engineer*] at Globex \
Jun 2019 -- Dec 2021

- Owned order-processing pipeline serving 2k QPS.

= Projects

#link("https://example.com/profile/jane")[*open-source-thing*]: a library.

= Skills

Languages: Python, Go, Rust, Java

= Education

*State University* -- B.S. Computer Science, 2018
