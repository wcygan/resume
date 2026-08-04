// Reusable renderer for the Golden Resume and its controlled stress fixtures.
#let render-resume(
  data,
  font: "Source Sans 3",
  large-body: true,
  compact-leading: true,
  compact-organization: true,
) = {
  let resume-body-size = if large-body { 10.25pt } else { 10pt }
  let resume-leading = if compact-leading { 0.45em } else { 0.6em }

  set document(
    title: data.document.title,
    author: data.document.author,
    keywords: data.document.keywords,
  )
  set page(width: 8.5in, height: 11in, margin: (x: 0.62in, y: 0.44in))
  set text(
    font: font,
    size: resume-body-size,
    fill: rgb("17212b"),
    lang: "en",
    hyphenate: false,
  )
  set par(leading: resume-leading, justify: false)
  set heading(numbering: none)

  let accent = rgb("165d78")
  let muted = rgb("4e5a66")
  let section-heading-size = 12.75pt
  let organization-name-size = if compact-organization { 10.85pt } else { 11.1pt }
  let role-title-size = 10.25pt
  let major-section-above = 1.85em
  let major-section-below = 0.8em
  let experience-entry-gap = 1em
  let experience-bullet-gap = 0.2em

  show heading.where(level: 2): set block(
    above: major-section-above,
    below: major-section-below,
  )

  let section(title) = heading(level: 2, outlined: false)[
    #text(fill: accent, size: section-heading-size, weight: "bold")[#title]
  ]

  let contact(destination, label) = link(destination)[#label]
  let contact-box(destination, label) = box(contact(destination, label))
  let organization(name) = text(size: organization-name-size)[#strong(name)]
  let role-title(title) = text(size: role-title-size)[#emph(title)]
  let accomplishment-content(item) = {
    if type(item) == str {
      [#item]
    } else {
      for segment in item.segments {
        let destination = segment.at("uri", default: none)
        if destination == none {
          [#segment.text]
        } else {
          box(link(destination)[#segment.text])
        }
      }
    }
  }
  let content-width = 8.5in - 2 * 0.62in

  let metadata-row(left-content, metadata-content) = context {
    let minimum-gap = 10pt
    let fits-one-row = (
      measure(left-content).width
        + measure(metadata-content).width
        + minimum-gap
        <= content-width
    )
    if fits-one-row {
      box(width: 100%)[#(left-content)#h(1fr)#(metadata-content)]
    } else {
      block[
        #(left-content) \
        #box(width: 100%)[#h(1fr)#(metadata-content)]
      ]
    }
  }

  let contact-links(contact-data) = context {
    let separator = [#h(0.75em) | #h(0.75em)]
    let portfolio-link = contact(
      contact-data.portfolio.uri,
      contact-data.portfolio.display,
    )
    let github-link = contact(contact-data.github.uri, contact-data.github.display)
    let linkedin-link = contact(
      contact-data.linkedin.uri,
      contact-data.linkedin.display,
    )
    let portfolio = contact-box(
      contact-data.portfolio.uri,
      contact-data.portfolio.display,
    )
    let github = contact-box(contact-data.github.uri, contact-data.github.display)
    let linkedin = contact-box(
      contact-data.linkedin.uri,
      contact-data.linkedin.display,
    )
    let all-links = [#portfolio-link#separator#github-link#separator#linkedin-link]
    let final-pair = [#github#separator#linkedin]
    if measure(all-links).width <= content-width {
      all-links
    } else if measure(final-pair).width <= content-width {
      [#portfolio \ #final-pair]
    } else {
      [#portfolio \ #github \ #linkedin]
    }
  }

  let experience(company, dates, role, location, accomplishments) = {
    let has-accomplishments = accomplishments.len() > 0
    block(
      breakable: false,
      below: experience-entry-gap,
    )[
      #metadata-row(
        [
          #organization(company)
          #h(0.45em) — #h(0.45em)
          #role-title(role)
        ],
        text(fill: muted)[Dates: #dates #h(0.45em) · #h(0.45em) Location: #location],
      )
      #if has-accomplishments [
        #block(inset: (top: experience-bullet-gap))[
          #list(..accomplishments.map(item => [#accomplishment-content(item)]))
        ]
      ]
    ]
  }

  let project(name, descriptor, focus, accomplishments, repository: none) = block(
    breakable: false,
  )[
    #let project-focus = if repository == none {
      [Focus: #focus]
    } else {
      [
        Focus: #focus #h(0.45em) · #h(0.45em)
        Repository: #link(repository.uri)[#repository.display]
      ]
    }
    #metadata-row(
      [
        #organization(name)
        #h(0.45em) — #h(0.45em)
        #role-title(descriptor)
      ],
      text(fill: muted)[#project-focus],
    )
    #block(inset: (top: experience-bullet-gap))[
      #list(..accomplishments.map(item => [#accomplishment-content(item)]))
    ]
  ]

  [
    #align(center)[
      #heading(level: 1, outlined: false)[#text(size: 22pt, weight: "bold")[#data.contact.name]]
      #set par(leading: 0.72em)
      #contact(data.contact.email.uri, data.contact.email.display)
      #if data.contact.location != none [
        #h(0.75em) | #h(0.75em)
        #data.contact.location
      ]
      \
      #contact-links(data.contact) \
      #if data.contact.work_authorization != none [
        #text(fill: muted)[#data.contact.work_authorization]
      ]
    ]

    #if data.profile != none [
      #section("PROFILE")
      #data.profile
    ]

    #section("EXPERIENCE")
    #for job in data.experience {
      experience(
        job.company,
        job.dates,
        job.role,
        job.location,
        job.accomplishments,
      )
    }

    #section("PROJECTS")
    #for item in data.projects {
      project(
        item.name,
        item.descriptor,
        item.focus,
        item.accomplishments,
        repository: item.at("repository", default: none),
      )
    }

    #section("EDUCATION")
    #organization(data.education.institution)
    #h(0.75em)
    #text(fill: muted)[Graduation: #data.education.graduation] \
    #data.education.degree

    #section("SKILLS")
    #for skill in data.skills [
      #strong(skill.label) #skill.values \
    ]
  ]
}
