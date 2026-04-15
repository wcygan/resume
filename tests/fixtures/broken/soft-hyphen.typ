// Defect: a literal U+00AD soft hyphen is embedded mid-word, and the word is
// placed in a narrow block that forces it to actually wrap at the soft hyphen.
// Real ATS pipelines (Tika/PDFBox) split the wrapped word into two paragraphs
// with a blank line between — that's the production-level failure this
// assertion guards against. Forcing the wrap (not just embedding the codepoint
// in-line) is what makes the fixture reproduce on Linux CI too: Linux poppler
// silently strips U+00AD from extracted text when no wrap occurs.

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

// Narrow column: the long word can't fit on one line and is forced to break
// at the embedded U+00AD, which pdftotext and Tika then emit in the extracted
// text stream.
#block(width: 0.5in)[
  #"invol\u{AD}untary"
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
