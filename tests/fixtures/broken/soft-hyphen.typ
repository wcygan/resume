// Defect: leaves automatic hyphenation on (Typst default for many langs). The
// long technical word in the bullet wraps across the narrow left column with a
// soft hyphen (U+00AD), which pdftotext / Tika emit verbatim and then split
// the word across a paragraph boundary.

#set page(paper: "us-letter", margin: 0.6in)
#set text(font: "New Computer Modern", size: 10pt, lang: "en", hyphenate: true)

#align(center)[
  #text(size: 16pt, weight: "bold")[Jane Doe] \
  jane\@example.com
]

#v(0.3em)

= Work Experience

*Staff Engineer* at Acme Corp \
Jan 2022 -- Present

// Narrow block forces wrap inside the long word. Soft hyphen will fire.
#block(width: 2in)[
  - Maintained the electroencephalographically-sampled
    pseudopseudohypoparathyroidism telemetry platform end-to-end.
]

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
