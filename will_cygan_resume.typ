#import "tests/fixtures/golden-resume/golden-resume-template.typ": render-resume

#let resume-data = json("will_cygan_resume-data.json")

#render-resume(
  resume-data,
  font: "Source Sans 3",
  large-body: false,
  compact-leading: true,
  compact-organization: true,
)
