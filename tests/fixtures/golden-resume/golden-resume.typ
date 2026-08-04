// A one-page, normal-flow baseline for text-layer portability experiments.
#import "golden-resume-template.typ": render-resume

#let data-path = sys.inputs.at("data", default: "golden-resume-data.json")
#let resume-data = json(data-path)

#render-resume(
  resume-data,
  font: sys.inputs.at("font", default: "Source Sans 3"),
  large-body: sys.inputs.at("body-size", default: "large") == "large",
  compact-leading: sys.inputs.at("compact-leading", default: "true") == "true",
  compact-organization: sys.inputs.at("compact-organization", default: "true") == "true",
)
