// Vendored from https://github.com/ptsouchlos/modern-cv @ tag 0.8.0.
// MIT License — Copyright (c) 2024 Paul Tsouchlos.
// Trimmed: cover-letter templates removed; linguify dropped (English inlined);
// `type(x) == "string"` updated to `type(x) == str` for typst 0.13+.

#import "@preview/fontawesome:0.5.0": *

#let color-darknight = rgb("#131A28")
#let color-darkgray = rgb("#333333")
#let color-gray = rgb("#5d5d5d")
#let default-accent-color = rgb("#262F99")
#let default-location-color = rgb("#333333")

#let linkedin-icon = box(fa-icon("linkedin", fill: color-darknight))
#let github-icon = box(fa-icon("github", fill: color-darknight))
#let twitter-icon = box(fa-icon("twitter", fill: color-darknight))
#let google-scholar-icon = box(fa-icon("google-scholar", fill: color-darknight))
#let orcid-icon = box(fa-icon("orcid", fill: color-darknight))
#let phone-icon = box(fa-icon("square-phone", fill: color-darknight))
#let email-icon = box(fa-icon("envelope", fill: color-darknight))
#let birth-icon = box(fa-icon("cake", fill: color-darknight))
#let homepage-icon = box(fa-icon("home", fill: color-darknight))
#let website-icon = box(fa-icon("globe", fill: color-darknight))

#let __justify_align(left_body, right_body) = {
  block[
    #left_body
    #box(width: 1fr)[
      #align(right)[
        #right_body
      ]
    ]
  ]
}

#let __justify_align_3(left_body, mid_body, right_body) = {
  block[
    #box(width: 1fr)[#align(left)[#left_body]]
    #box(width: 1fr)[#align(center)[#mid_body]]
    #box(width: 1fr)[#align(right)[#right_body]]
  ]
}

#let __resume_footer(author, language, date) = {
  set text(fill: gray, size: 8pt)
  __justify_align_3[
    #smallcaps[#date]
  ][
    #smallcaps[
      #if language == "zh" or language == "ja" [
        #author.firstname#author.lastname
      ] else [
        #author.firstname#sym.space#author.lastname
      ]
      #sym.dot.c
      Résumé
    ]
  ][
    #context { counter(page).display() }
  ]
}

#let github-link(github-path) = {
  set box(height: 11pt)
  align(right + horizon)[
    #fa-icon("github", fill: color-darkgray) #link(
      "https://github.com/" + github-path,
      github-path,
    )
  ]
}

#let secondary-right-header(body) = {
  set text(size: 11pt, weight: "medium")
  body
}

#let tertiary-right-header(body) = {
  set text(weight: "light", size: 9pt)
  body
}

#let justified-header(primary, secondary) = {
  set block(above: 0.7em, below: 0.7em)
  pad[
    #__justify_align[
      == #primary
    ][
      #secondary-right-header[#secondary]
    ]
  ]
}

#let secondary-justified-header(primary, secondary) = {
  __justify_align[
    === #primary
  ][
    #tertiary-right-header[#secondary]
  ]
}

#let resume(
  author: (:),
  profile-picture: image,
  date: datetime.today().display("[month repr:long] [day], [year]"),
  accent-color: default-accent-color,
  colored-headers: true,
  show-footer: true,
  language: "en",
  font: ("Source Sans Pro", "Source Sans 3"),
  header-font: ("Roboto"),
  paper-size: "a4",
  body,
) = {
  if type(accent-color) == str {
    accent-color = rgb(accent-color)
  }

  show: body => context {
    set document(
      author: author.firstname + " " + author.lastname,
      title: "Résumé",
    )
    body
  }

  set text(
    font: font,
    lang: language,
    size: 11pt,
    fill: color-darkgray,
    fallback: true,
  )

  set page(
    paper: paper-size,
    margin: (left: 15mm, right: 15mm, top: 10mm, bottom: 10mm),
    footer: if show-footer [
      #__resume_footer(author, language, date)
    ] else [],
    footer-descent: 0pt,
  )

  set par(spacing: 0.75em, justify: true)

  set heading(numbering: none, outlined: false)

  show heading.where(level: 1): it => [
    #set text(size: 16pt, weight: "regular")
    #set align(left)
    #set block(above: 1em)
    #let color = if colored-headers { accent-color } else { color-darkgray }
    #text[#strong[#text(color)[#it.body]]]
    #box(width: 1fr, line(length: 100%))
  ]

  show heading.where(level: 2): it => {
    set text(color-darkgray, size: 12pt, style: "normal", weight: "bold")
    it.body
  }

  show heading.where(level: 3): it => {
    set text(size: 10pt, weight: "regular")
    smallcaps[#it.body]
  }

  let name = {
    align(center)[
      #pad(bottom: 5pt)[
        #block[
          #set text(size: 32pt, style: "normal", font: header-font)
          #if language == "zh" or language == "ja" [
            #text(accent-color, weight: "thin")[#author.firstname]#text(weight: "bold")[#author.lastname]
          ] else [
            #text(accent-color, weight: "thin")[#author.firstname]
            #text(weight: "bold")[#author.lastname]
          ]
        ]
      ]
    ]
  }

  let positions = {
    set text(accent-color, size: 9pt, weight: "regular")
    align(center)[
      #smallcaps[
        #author.positions.join(text[#"  "#sym.dot.c#"  "])
      ]
    ]
  }

  let address = {
    set text(size: 9pt, weight: "regular")
    align(center)[
      #if ("address" in author) [ #author.address ]
    ]
  }

  let contacts = {
    set box(height: 9pt)
    let separator = box(width: 5pt)

    align(center)[
      #set text(size: 9pt, weight: "regular", style: "normal")
      #block[
        #align(horizon)[
          #if ("birth" in author) [
            #birth-icon
            #box[#text(author.birth)]
            #separator
          ]
          #if ("phone" in author) [
            #phone-icon
            #box[#text(author.phone)]
            #separator
          ]
          #if ("email" in author) [
            #email-icon
            #box[#link("mailto:" + author.email)[#author.email]]
          ]
          #if ("homepage" in author) [
            #separator
            #homepage-icon
            // Strip scheme in display text so Tika's URL block (which echoes
            // every http(s) target) doesn't look like a duplicate of the
            // visible text — stays readable, keeps the hyperlink intact.
            #box[#link(author.homepage)[#author.homepage.replace(regex("^https?://"), "")]]
          ]
          #if ("github" in author) [
            #separator
            #github-icon
            #box[#link("https://github.com/" + author.github)[#author.github]]
          ]
          #if ("linkedin" in author) [
            #separator
            #linkedin-icon
            #box[
              // Display the LinkedIn handle (matches github/twitter pattern)
              // rather than the full name, to avoid duplicating the candidate's
              // name in ATS-extracted text (Tika emits link display text).
              #link("https://www.linkedin.com/in/" + author.linkedin)[#author.linkedin]
            ]
          ]
          #if ("twitter" in author) [
            #separator
            #twitter-icon
            #box[#link("https://twitter.com/" + author.twitter)[\@#author.twitter]]
          ]
          #if ("scholar" in author) [
            #let fullname = str(author.firstname + " " + author.lastname)
            #separator
            #google-scholar-icon
            #box[#link("https://scholar.google.com/citations?user=" + author.scholar)[#fullname]]
          ]
          #if ("orcid" in author) [
            #separator
            #orcid-icon
            #box[#link("https://orcid.org/" + author.orcid)[#author.orcid]]
          ]
          #if ("website" in author) [
            #separator
            #website-icon
            #box[#link(author.website)[#author.website]]
          ]
        ]
      ]
    ]
  }

  if profile-picture != none {
    grid(
      columns: (100% - 4cm, 4cm),
      rows: (100pt),
      gutter: 10pt,
      [
        #name
        #positions
        #address
        #contacts
      ],
      align(left + horizon)[
        #block(
          clip: true,
          stroke: 0pt,
          radius: 2cm,
          width: 4cm,
          height: 4cm,
          profile-picture,
        )
      ],
    )
  } else {
    name
    positions
    address
    contacts
  }

  body
}

#let resume-item(body) = {
  set text(size: 10pt, style: "normal", weight: "light", fill: color-darknight)
  set block(above: 0.75em, below: 1.25em)
  set par(leading: 0.65em)
  block(above: 0.5em)[
    #body
  ]
}

#let resume-entry(
  title: none,
  location: "",
  date: "",
  description: "",
  title-link: none,
  accent-color: default-accent-color,
  location-color: default-location-color,
) = {
  let title-content
  if type(title-link) == str {
    title-content = link(title-link)[#title]
  } else {
    title-content = title
  }
  block(above: 1em, below: 0.65em)[
    #pad[
      #justified-header(title-content, location)
      #if description != "" or date != "" [
        #secondary-justified-header(description, date)
      ]
    ]
  ]
}

#let resume-gpa(numerator, denominator) = {
  set text(size: 12pt, style: "italic", weight: "light")
  text[Cumulative GPA: #box[#strong[#numerator] / #denominator]]
}

#let resume-certification(certification, date) = {
  justified-header(certification, date)
}

#let resume-skill-item(category, items) = {
  set block(below: 0.65em)
  set pad(top: 2pt)
  pad[
    #grid(
      columns: (20fr, 80fr),
      gutter: 10pt,
      align(right)[
        #set text(hyphenate: false)
        == #category
      ],
      align(left)[
        #set text(size: 11pt, style: "normal", weight: "light")
        #items.join(", ")
      ],
    )
  ]
}
