// Defect: `show heading` override collapses the block-level spacing around
// section headings, so Skills content runs directly into the Education header
// in pdftotext -layout output — no blank line between adjacent sections. A
// section-boundary ATS parser merges the two sections.

#set page(paper: "us-letter", margin: 0.6in)
#set text(font: "New Computer Modern", size: 10pt)
#show heading: it => text(weight: "bold")[#it.body]
#set par(spacing: 0pt, leading: 0.5em)

#align(center)[
  #text(size: 16pt, weight: "bold")[Jane Doe] \
  jane\@example.com
]

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
