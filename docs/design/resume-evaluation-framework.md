# Resume Evaluation Framework

Status: Design only  
Repository: `resume`  
Branch: `codex/evaluation-framework-design`  
Last updated: 2026-08-01

## 1. Purpose

Build a local-first, evidence-backed framework for evaluating resume PDF variants against structured job postings.

The framework should approximate the controllable parts of modern applicant tracking and recruiting pipelines without pretending to reproduce a particular employer's private ATS configuration. It must evaluate each layer separately:

1. PDF artifact integrity and text extraction.
2. Structured resume field mapping.
3. Job-posting ingestion and requirement normalization.
4. Objective eligibility and knockout criteria.
5. Lexical retrieval and terminology visibility.
6. Criterion-level semantic evidence matching.
7. Evidence strength, recency, scope, and specificity.
8. Optional LLM-assisted judgment.
9. Human readability and role-positioning review.
10. Cross-variant comparison and regression detection.

The framework exists to answer questions such as:

- Does this PDF extract cleanly across multiple parser families?
- Can a parser correctly associate titles, companies, dates, bullets, and skills?
- Which explicit job requirements are met, partially met, missing, contradicted, or unknown?
- What resume text supports each conclusion?
- Is an important skill only listed, or demonstrated in recent work?
- Does a rewrite improve one target job while damaging performance across related roles?
- Do deterministic, local-model, and cloud-model graders agree?
- How stable are results across models, prompts, extraction engines, and repeated runs?

The framework must not claim to predict callback probability or produce a universal "ATS score."

## 2. Core claim and boundaries

Nearly every controllable technical layer can run locally:

- Typst compilation and PDF rendering.
- PDF text extraction and layout diagnostics.
- OCR fallback.
- Resume section and field extraction.
- Job-posting capture and normalization.
- Rule-based and statistical matching.
- Local taxonomy lookup.
- BM25 and other lexical retrieval.
- Local embeddings and rerankers.
- Local LLM judgments.
- Variant generation, compilation, evaluation, and reporting.

The following cannot be reproduced exactly without authorized access to the employer's systems:

- Proprietary ATS parser models and versions.
- Employer-specific custom fields.
- Private requisition data.
- Screening-question knockout configuration.
- Search queries entered by recruiters.
- Ranking weights and recommendation models.
- Third-party integrations and enrichment data.
- Human review behavior.
- Advancement or callback outcomes.

Consequently, the strongest defensible claims are bounded claims such as:

- "Text-layer compatible with Poppler and Tika/PDFBox under the tested versions."
- "Nine of eleven locally modeled required criteria have explicit supporting evidence."
- "Variant B is preferred to Variant A by three of four configured judges."
- "The structured parser achieved 0.96 field-level F1 against the reviewed oracle."

The framework must never transform those statements into "ATS-safe," "92% likely to pass," or equivalent hiring predictions.

## 3. Design principles

### 3.1 Separate every evaluation layer

Parser readability, structured field mapping, eligibility, retrieval, ranking, and human fit are different problems. A pass in one layer must not imply a pass in another.

### 3.2 Deterministic core, model-assisted extensions

Compilation, extraction, schema validation, exact matching, date calculations, taxonomy lookup, report assembly, and regression assertions should be deterministic.

Models may assist with ambiguous interpretation, semantic matching, evidence quality, and prose comparison. Model output must never be the only representation of a source fact.

### 3.3 Evidence before conclusions

Every field and criterion judgment should retain source evidence:

- Source artifact hash.
- Extractor and version.
- Character or line span.
- Exact source text.
- Normalization method.
- Confidence.
- Human-review status.

An LLM judgment without evidence should be rejected or marked invalid.

### 3.4 Raw data is immutable

Downloaded job data, HTML, JSON-LD, parser text, and source resume artifacts should be content-addressed or hash-recorded and never silently rewritten.

Normalized records are derived artifacts with explicit schema and parser versions.

### 3.5 Explicit facts and inference are distinct

The system must distinguish:

- Text explicitly present in a posting or resume.
- Deterministically normalized aliases.
- Taxonomy-derived relationships.
- Model inference.
- Human annotation.

Inference must not silently become an employer requirement or candidate claim.

### 3.6 Local-first privacy

All deterministic processing and local-model evaluation should remain on the Mac. A provider manifest must state when visible resume or job text is sent to a cloud service.

### 3.7 No unconstrained resume invention

Variant generation may select, reorder, shorten, clarify, or accurately reframe supported claims. It may not invent metrics, dates, technologies, titles, ownership, credentials, scope, or results.

### 3.8 Preserve raw metrics

Any composite score must be optional, versioned, and accompanied by every component metric. A user-selected weighting profile is a preference, not ATS truth.

### 3.9 Optimize against held-out data

A resume optimized against one posting can overfit its vocabulary. Promotion requires checking target postings, related held-out postings, negative controls, and known mutation fixtures.

### 3.10 One command, reproducible output

Given a resume PDF and vendored job record, one local command should create a reproducible JSON result and a readable Markdown report.

### 3.11 Accepted implementation assumptions

The first implementation should proceed with these explicit assumptions:

- Job-posting URLs, copied text, HTML, JSON, and canonical records are supplied by the user and are trusted inputs.
- Adversarial prompt injection and hostile-source handling are outside the v1 threat model. The framework still must not execute active content from an input, and it must validate normalized output for structural correctness, provenance completeness, and unsupported inference.
- Python Pydantic models are the single authoritative definition of the canonical domain schema. JSON Schema is generated from those models for agents, editors, fixtures, and interoperability; YAML and JSON files are serializations of the same validated models, not separate schema authorities.
- Reproducibility is practical rather than hermetic. Runs should record useful input hashes, schema and prompt versions, tool versions, and provider/model identifiers when readily available, but v1 does not require containerized builds, a fully pinned operating-system toolchain, or byte-identical historical reruns.

## 4. Existing repository foundation

The repository already contains the first framework layer:

- `will_cygan_resume-data.json`: authoritative resume content.
- `will_cygan_resume.typ`: thin JSON-to-renderer adapter.
- `tests/fixtures/golden-resume/golden-resume-template.typ`: active shared
  renderer and controlled Golden fixture implementation.
- `will_cygan_resume.pdf`: compiled artifact.
- `scripts/extraction_check.py`: Poppler and Tika/PDFBox extraction diagnostics.
- `scripts/extraction-check.fixtures.toml`: expected extraction facts.
- `tests/fixtures/broken/`: controlled negative fixtures.
- `tests/test_extraction_check.py`: extraction regression suite.
- `work-experience/`: long-form evidence backing resume claims.
- `.agents/skills/resume-review/`: evidence-led content review, tailoring,
  comparison, bullet refinement, and interview preparation.
- `.agents/skills/resume-parsability/`: mechanical PDF evidence model, deep
  Golden evaluators, and external-ATS claim boundaries.

The current extraction layer checks:

- Nonempty output.
- Section order.
- Candidate name and contact proximity.
- Job title/company/date contiguity.
- Date consistency.
- Mojibake and private-use glyphs.
- Cross-extractor agreement.
- Soft hyphens.
- Keyword round-trip.
- URL duplication.
- Section boundaries.

This remains a hard gate and should be reused rather than replaced.

The project-local parsability skill now makes the intended boundary explicit:
clean extraction is local layer-one evidence, not proof that a named external
ATS will map every field or that the resume will produce a recruiting outcome.

## 5. Recruiting-system domain model

Recruiting platforms commonly distinguish the following entities:

```text
Job / Requisition
├── Opening(s): individual headcount slots
├── Posting(s): public or internal advertisements
├── Application form: candidate questions and required fields
└── Screening configuration: filters, knockouts, search, and ranking rules
```

A public careers page generally exposes a posting and sometimes the application form. It usually does not expose the private requisition, screening configuration, recruiter searches, or model weights.

The local framework should therefore model public evidence and represent private configuration as unknown unless the user supplies authorized data.

### 5.1 Source-agnostic ingestion boundary

The canonical `JobPosting` must not depend on the shape of any one vendor API. Greenhouse, Lever, Ashby, LinkedIn, Schema.org, arbitrary web pages, copied text, and manually authored records must all enter through one ingestion envelope.

Supported input kinds:

- `url`: a public job-posting URL supplied by the user.
- `text`: a copied plain-text job description.
- `html`: saved or pasted HTML.
- `json`: a vendor API response or JSON-LD record.
- `file`: a local artifact containing any supported media type.
- `canonical`: an already normalized record that still requires validation.

The first persisted object is a `SourceDocument`, not a `JobPosting`:

```yaml
source_document:
  artifact_id: source-linkedin-2026-08-01-001
  input_kind: text
  source_system: linkedin
  acquisition_method: user_copy_paste
  source_url: https://www.linkedin.com/jobs/view/123456789
  canonical_listing_url: null
  media_type: text/plain
  captured_at: 2026-08-01T18:00:00Z
  payload_sha256: "..."
  raw_artifact: jobs/raw/linkedin/123456789/source.txt
  supplied_by: user
  source_hint: linkedin
```

`source_system` is an open string, not a closed enum. Known values receive specialized adapters, while unknown values remain valid and route through generic normalization.

The ingestion boundary provides an anti-corruption layer:

```text
LinkedIn text or URL ─┐
Greenhouse JSON ──────┤
Lever JSON ───────────┤
Ashby JSON ───────────┼─> SourceDocument -> adapter -> canonical JobPosting
Schema.org JSON-LD ───┤
Arbitrary HTML ───────┤
Copied text blob ─────┘
```

Vendor-specific fields must not leak into core evaluator logic. The evaluator consumes only canonical records.

### 5.2 URL and copy/paste workflow

The primary user workflow should be deliberately simple:

1. Supply a URL, paste the full posting, or provide both.
2. Preserve the exact supplied input as a source artifact.
3. If a URL is present, attempt permitted public retrieval.
4. Prefer official vendor JSON or embedded Schema.org data when available.
5. Fall back to visible page text or the user-pasted text.
6. Normalize through deterministic rules and, optionally, an LLM.
7. Validate the result against the canonical schema.
8. Require evidence provenance for every populated field and criterion.
9. Surface unresolved or conflicting fields for review.
10. Save the canonical posting only after validation; human review is optional for exploratory runs and required for oracle cases.

If a URL cannot be fetched because of authentication, robots policy, rendering, or access controls, the framework should retain the URL as provenance and use the supplied text. It must not attempt to bypass access controls.

### 5.3 Agent-assisted normalization handoff

The user may paste a URL or text blob into Codex, Claude Code, Pi, or another agent and ask it to produce the canonical posting. That is a supported ingestion path. The agent output is an unreviewed derived artifact that must be validated for correctness and provenance before use; this validation is not based on an assumption that the user-supplied source is hostile.

The handoff bundle should contain:

```text
jobs/inbox/<ingestion-id>/
  source.txt | source.html | source.json
  source-manifest.yaml
  normalized-job.yaml
  normalization-manifest.yaml
  validation-report.json
```

The agent must be given:

- The canonical JSON Schema.
- A required/preferred classification rubric.
- Criterion-kind definitions.
- Instructions to preserve exact source wording.
- Instructions to use `null` or `unknown` when information is absent.
- Instructions not to infer private screening behavior.
- Instructions to attach source evidence to every populated field.
- A strict output format.

The framework validates agent output exactly as it validates an adapter result. No agent receives authority to change the schema, overwrite the source artifact, or mark its own output human-reviewed.

### 5.4 Field-level provenance

Top-level source provenance is insufficient because one canonical posting may combine a vendor API record, visible page text, copied text, and human correction.

Keep field provenance in a sidecar indexed by canonical JSON Pointer:

```yaml
field_provenance:
  /posting/title:
    - source_artifact_id: source-greenhouse-127817
      locator:
        kind: json_pointer
        value: /title
      source_text: Senior Software Engineer
      derivation: direct
      confidence: 1.0

  /posting/workplace_type:
    - source_artifact_id: source-linkedin-123456789
      locator:
        kind: text_span
        start: 42
        end: 48
      source_text: Remote
      derivation: normalized_alias
      confidence: 0.99

  /criteria/0:
    - source_artifact_id: source-linkedin-123456789
      locator:
        kind: text_span
        start: 812
        end: 849
      source_text: Production experience with Go or Rust
      derivation: llm_decomposition
      confidence: 0.91
```

Supported locator kinds:

- `json_pointer`
- `jsonpath`
- `text_span`
- `line_range`
- `xpath`
- `css_selector`
- `manual_annotation`

Supported derivation kinds:

- `direct`
- `normalized_alias`
- `deterministic_parse`
- `taxonomy_mapping`
- `llm_extraction`
- `llm_decomposition`
- `human_correction`

### 5.5 Missing, unknown, inferred, and conflicting values

The canonical model must preserve four distinct states:

- **Missing:** the schema field has no value in the available source.
- **Unknown:** the concept matters, but the source does not establish it.
- **Inferred:** a derivation proposes a value not stated directly.
- **Conflicting:** two source artifacts establish incompatible values.

Copy/pasted text commonly omits posting dates, IDs, compensation metadata, application URLs, structured locations, and application questions. The normalizer must leave these absent or unknown rather than generating plausible values.

### 5.6 Source extensions and lossless ingestion

The canonical schema should contain a stable common core plus a lossless extension area:

```yaml
source_extensions:
  greenhouse:
    requisition_id: "50"
    metadata: []
  lever:
    categories: null
  linkedin:
    integration_context: null
    external_job_posting_id: null
```

Core evaluators must ignore extensions unless an explicit optional evaluator understands them. Unrecognized vendor fields remain preserved in the raw source artifact even when no extension mapping exists.

### 5.7 Syndication and multi-source reconciliation

The same role may appear on LinkedIn and on an employer's Greenhouse, Lever, Ashby, or Workday board. These should be modeled as multiple source documents for one logical posting when the evidence supports that relationship.

Useful reconciliation signals:

- Employer apply URL.
- Vendor posting ID.
- External job posting ID.
- Requisition ID.
- Exact or near-exact title.
- Organization.
- Location.
- Description fingerprint.
- Publication time.

Reconciliation must be conservative. Similar postings are not automatically the same requisition.

```yaml
source_relationships:
  - relation: syndicated_copy_of
    from_artifact_id: source-linkedin-123456789
    to_artifact_id: source-greenhouse-127817
    confidence: 0.97
    reviewed: false
```

When sources disagree, preserve the disagreement. Prefer the employer's canonical apply destination for identity, but do not silently replace wording from the source being evaluated.

### 5.8 LinkedIn-specific boundary

LinkedIn's documented Job Posting API is an authorized partner interface for publishing and managing jobs. It is not assumed to be a general public API for downloading arbitrary LinkedIn listings.

The initial LinkedIn ingestion modes are therefore:

- User-pasted visible job text.
- User-supplied URL plus pasted text.
- Publicly retrievable page content when permitted.
- Embedded structured data when available.
- Authorized API or export data only when the user has legitimate access.

The LinkedIn adapter should understand LinkedIn's documented field vocabulary when those fields are present, including organization identity, apply URL, external posting ID, operation/lifecycle metadata, title, description, listing time, location, employment status, and workplace type. It should not require those fields for copied text.

### 5.9 Schema compatibility policy

Compatibility is maintained through:

1. A versioned canonical schema independent of vendors.
2. One adapter per known source shape.
3. Generic text/HTML/JSON adapters.
4. Immutable raw source artifacts.
5. Field-level provenance.
6. A source-extension namespace.
7. Explicit schema migrations.
8. Golden vendor fixtures.
9. Metamorphic equivalence tests across input formats.
10. Tolerant readers and strict writers.

An adapter upgrade may improve normalization, but it may not reinterpret historical output silently. Re-normalization creates a new derived record with a new normalizer version and hash.

## 6. System architecture

```text
Vendor job source
  -> immutable source snapshot
  -> source document envelope
  -> vendor-specific parser
  -> canonical JobPosting
  -> field provenance sidecar
  -> reviewed criteria oracle

Typst resume variant
  -> compiled PDF
  -> extraction engines
  -> extraction diagnostics
  -> canonical ResumeProfile
  -> reviewed profile oracle

JobPosting + ResumeProfile
  -> eligibility evaluator
  -> lexical matcher
  -> semantic retriever/reranker
  -> evidence-quality evaluator
  -> optional model judges
  -> result vector
  -> variant comparison
  -> human promotion decision
```

### 6.1 Architectural components

1. **Job vendor**
   Captures public API, JSON-LD, or HTML content with provenance and hashes.

2. **Job normalizer**
   Converts vendor-specific records into a canonical posting schema.

3. **Requirement extractor**
   Splits posting content into responsibilities, required criteria, preferred criteria, context, benefits, and application questions.

4. **Resume artifact pipeline**
   Compiles Typst variants, hashes artifacts, extracts text, and runs parseability assertions.

5. **Resume profile parser**
   Converts extracted text into structured experience, skills, education, projects, and certifications.

6. **Matcher**
   Matches each job criterion to one or more resume evidence spans.

7. **Grader registry**
   Runs deterministic, semantic, and model-assisted graders under a common contract.

8. **Evaluation runner**
   Executes a matrix of resume variants, postings, extractors, and providers.

9. **Report generator**
   Emits machine-readable results and a concise evidence-backed review.

10. **Variant generator**
    Creates bounded source modifications tied to approved claim IDs.

11. **Promotion gate**
    Compares a candidate variant with the baseline across target and held-out cases.

## 7. Proposed repository layout

The initial implementation should remain filesystem-first. A database is unnecessary until the run volume or query patterns justify one.

```text
resume/
  schemas/
    job-posting.schema.json
    resume-profile.schema.json
    criterion-match.schema.json
    evaluation-run.schema.json
    variant-manifest.schema.json

  jobs/
    inbox/
      <ingestion-id>/
        source.txt
        source-manifest.yaml
        normalized-job.yaml
        normalization-manifest.yaml
        validation-report.json
    raw/
      <source>/<job-id>/
        source.json
        source.html
        manifest.json
    normalized/
      <job-id>.yaml
    oracles/
      <job-id>.yaml

  resume-data/
    claims.yaml
    aliases.yaml
    profile-oracle.yaml

  variants/
    manifests/
      <variant-id>.yaml

  evaluators/
    artifact/
    resume_parser/
    job_parser/
    eligibility/
    lexical/
    semantic/
    evidence/
    judges/
    reporting/

  evals/
    cases/
      target/
      holdout/
      negative/
      mutations/
    prompts/
    results/
      .gitignore

  scripts/
    vendor_job.py
    import_job.py
    normalize_job.py
    parse_resume.py
    evaluate_resume.py
    compare_variants.py

  docs/design/resume-evaluation-framework.md
```

Generated PDFs, extracted text, model responses, and run results should default to a gitignored directory. Reviewed schemas, posting snapshots selected for long-term use, oracles, prompts, and small fixtures may be tracked deliberately.

## 8. Canonical job-posting model

### 8.1 Source provenance

Every job snapshot must record:

```yaml
schema_version: 1
identity:
  job_id: greenhouse-example-127817
  source_system: greenhouse
  source_external_id: "127817"
  source_url: https://example.com/jobs/127817
  captured_at: 2026-08-01T15:00:00Z
  source_sha256: "..."
  raw_artifact: jobs/raw/greenhouse/127817/source.json
```

The identity block describes the logical normalized posting. It does not replace the `SourceDocument` envelope or field-level provenance. A posting may reference more than one source artifact.

Recommended source systems for the first release:

- Greenhouse Job Board API.
- Lever Postings API.
- Ashby public Job Postings API.
- Schema.org `JobPosting` JSON-LD.
- Generic HTML fallback.

### 8.2 Canonical posting fields

```yaml
posting:
  title: Senior Software Engineer
  alternate_titles: []
  organization: Example Corp
  department: Infrastructure
  team: Runtime Systems
  employment_type: full_time
  workplace_type: remote
  locations:
    - city: Chicago
      region: Illinois
      country: US
  applicant_location_requirements:
    - country: US
  published_at: 2026-07-20T00:00:00Z
  valid_through: null
```

### 8.3 Compensation

```yaml
compensation:
  disclosed: true
  currency: USD
  interval: year
  minimum: 180000
  maximum: 230000
  equity: unknown
  bonus: unknown
  source_text: "$180,000-$230,000"
```

### 8.4 Content sections

```yaml
content:
  description_plain: "..."
  description_html: "..."
  summary:
    - id: summary-01
      text: "..."
      source_span: [0, 120]
  responsibilities:
    - id: resp-01
      text: Design distributed systems for...
      source_span: [421, 487]
  benefits: []
  equal_opportunity_text: "..."
```

### 8.5 Criteria

Each criterion must be atomic enough to evaluate independently.

```yaml
criteria:
  - id: req-01
    importance: required
    kind: skill
    text: Production experience with Go or Rust
    normalized_terms:
      - go
      - rust
    operator: any_of
    minimum: null
    unit: null
    explicit: true
    inferred: false
    confidence: 1.0
    evidence_span: [812, 849]
    reviewed: true

  - id: req-02
    importance: required
    kind: experience_years
    text: Five or more years of backend engineering experience
    normalized_terms:
      - backend engineering
    operator: minimum
    minimum: 5
    unit: years
    explicit: true
    inferred: false
    confidence: 1.0
    evidence_span: [850, 910]
    reviewed: true

  - id: pref-01
    importance: preferred
    kind: domain
    text: Experience with distributed databases
    normalized_terms:
      - distributed databases
    operator: evidence
    explicit: true
    inferred: false
    confidence: 1.0
    evidence_span: [1010, 1054]
    reviewed: true
```

Supported criterion kinds should include:

- `skill`
- `technology`
- `domain`
- `responsibility`
- `experience_years`
- `seniority`
- `leadership`
- `education`
- `certification`
- `clearance`
- `location`
- `work_authorization`
- `employment_type`
- `schedule`
- `travel`
- `language`
- `portfolio`
- `other`

Supported importance values:

- `required`
- `preferred`
- `context`
- `benefit`
- `unknown`

### 8.6 Application form and known knockouts

```yaml
application:
  questions:
    - id: q-01
      kind: work_authorization
      required: true
      text: Are you authorized to work in the United States?
      options: [yes, no]
      source_span: null
  known_knockouts: []
```

The system must not infer that a question is an automatic knockout unless the source or authorized configuration says so.

### 8.7 Normalization metadata

```yaml
normalization:
  normalizer: job-normalizer-v1
  normalizer_version: 1.0.0
  model_provider: null
  model: null
  prompt_version: null
  taxonomy_versions:
    onet: null
    esco: null
  reviewed: true
  reviewed_at: 2026-08-01T16:00:00Z
```

### 8.8 Schema versioning and migrations

Pydantic models are the single source of truth for the canonical schema and its validation rules. Generate JSON Schema from those models for agent handoffs and external tooling. Do not maintain an independent handwritten JSON Schema, YAML schema, and Python model that can drift apart.

The canonical record should include independent versions for:

- Canonical schema.
- Source adapter.
- Text cleaner.
- Requirement segmenter.
- Normalizer.
- Taxonomy mappings.
- Optional LLM prompt.

Schema migrations must be explicit pure transformations where practical:

```text
JobPosting v1 + migrate_v1_to_v2 -> JobPosting v2
```

The framework should retain the original normalized record or enough provenance to reproduce it. Generated results should declare the canonical schema version they consumed.

## 9. Job-posting ingestion

### 9.1 Capture order

Use the following source priority:

1. Official public vendor JSON API.
2. Schema.org `JobPosting` JSON-LD embedded in the official page.
3. Official page HTML.
4. User-provided text.

Do not scrape rendered text when a stable official JSON endpoint is available.

For a user-supplied URL, the importer should detect known hosts and embedded source clues before selecting an adapter. For a copied text blob, it should accept an optional source hint but must work with `source_system: unknown`.

### 9.2 Vendor adapters

Each adapter should implement a common interface:

```python
class JobSourceAdapter(Protocol):
    def supports(self, url: str) -> bool: ...
    async def fetch(self, url: str) -> RawJobArtifact: ...
    def normalize_source(self, artifact: RawJobArtifact) -> VendorJobRecord: ...
```

Initial adapters:

- `GreenhouseAdapter`
- `LeverAdapter`
- `AshbyAdapter`
- `LinkedInTextAdapter`
- `SchemaOrgAdapter`
- `HtmlFallbackAdapter`
- `PlainTextAdapter`
- `CanonicalRecordAdapter`

### 9.3 Snapshot rules

- Record retrieval time and HTTP metadata.
- Store the canonical source URL.
- Hash the exact downloaded bytes.
- Preserve raw HTML or JSON.
- Store a cleaned plain-text derivation separately.
- Never overwrite an existing snapshot with different bytes.
- Create a new snapshot or revision when content changes.
- Record redirect chains when relevant.
- Avoid vendoring authentication tokens, cookies, or session data.
- Review site terms before publishing captured job content outside a private repository.

### 9.4 Input routing

```python
class JobIngestionRequest(BaseModel):
    url: str | None = None
    text: str | None = None
    file: Path | None = None
    source_hint: str | None = None
    expected_source_system: str | None = None

    @model_validator(mode="after")
    def require_at_least_one_input(self) -> "JobIngestionRequest": ...
```

Routing rules:

1. Preserve every supplied input.
2. If URL and text are both present, keep both as linked source documents.
3. Prefer a known vendor adapter for official API data.
4. Prefer Schema.org when it is complete and directly sourced from the page.
5. Use visible or copied text to fill only fields it explicitly establishes.
6. Reconcile conflicts instead of overwriting them.
7. Produce one canonical record plus a provenance sidecar and validation report.

### 9.5 Requirement normalization

Requirement extraction should use a staged approach:

1. Deterministic section segmentation.
2. Bullet and sentence splitting.
3. Required/preferred lexical cues.
4. Criteria typing.
5. Skill and title normalization.
6. Optional LLM correction or decomposition.
7. Human review for oracle cases.

Useful lexical cues include:

- Required: `must`, `required`, `minimum`, `at least`, `need`, `will have`.
- Preferred: `preferred`, `nice to have`, `bonus`, `ideally`, `a plus`.
- Ambiguous: generic responsibility statements that do not state candidate qualifications.

The normalizer must preserve uncertainty rather than forcing every sentence into required or preferred.

### 9.6 LLM normalizer contract

An LLM normalizer should perform bounded extraction, not free-form rewriting.

Input:

- Source-document manifest.
- Exact source text.
- Canonical schema version.
- Criterion taxonomy.
- Required/preferred rubric.

Output:

- Canonical posting candidate.
- Field-provenance sidecar.
- Warnings.
- Unresolved ambiguities.

Hard requirements:

- Copy source wording for descriptions and criteria.
- Do not synthesize job IDs, dates, compensation, locations, or application questions.
- Do not combine distinct bullet requirements unless the source does.
- Do not split a single logical any-of requirement into multiple must-have requirements.
- Preserve modal language such as `must`, `preferred`, and `a plus`.
- Cite source spans.
- Use null/unknown when absent.
- Mark every model-derived interpretation as inferred until reviewed.

### 9.7 Normalization handoff validation

Whether normalization came from a Python adapter, Codex, Claude Code, Pi, or a local LLM, the same validation sequence applies:

1. JSON/YAML parse.
2. Canonical schema validation.
3. Provenance pointer validation.
4. Evidence-span bounds validation.
5. Source-text exactness validation.
6. Required/preferred consistency checks.
7. Criterion atomicity checks.
8. Duplicate-criterion detection.
9. Unsupported-inference warnings.
10. Optional human review.

## 10. Canonical resume model

### 10.1 Artifact identity

```yaml
document:
  artifact_id: resume-rust-infra-004
  source_variant_id: rust-infra-004
  source_typst_sha256: "..."
  pdf_sha256: "..."
  page_count: 1
  compiled_at: 2026-08-01T17:00:00Z
  typst_version: "..."
  font_manifest_sha256: "..."
```

### 10.2 Extraction results

```yaml
extractions:
  - extractor: poppler
    extractor_version: "..."
    mode: plain
    text_sha256: "..."
    text_artifact: ".eval-runs/.../pdftotext.txt"
    assertions:
      non_empty: pass
      section_order: pass
      job_contiguity: pass

  - extractor: poppler
    extractor_version: "..."
    mode: layout
    text_sha256: "..."
    text_artifact: ".eval-runs/.../pdftotext-layout.txt"

  - extractor: tika
    extractor_version: "..."
    parser_family: pdfbox
    text_sha256: "..."
    text_artifact: ".eval-runs/.../tika.txt"
```

### 10.3 Structured profile

```yaml
profile:
  candidate:
    name: Will Cygan
    location: null
    email: "..."
    phone: null
    links: []

  experience:
    - id: exp-01
      title: Senior Software Engineer
      company: Example Corp
      location: Remote
      start_date: 2022-02
      end_date: 2024-03
      bullets:
        - id: exp-01-b01
          text: Built...
          evidence_span: [1200, 1320]

  skills:
    - canonical: rust
      display: Rust
      category: language
      evidence_spans: [[500, 504], [1250, 1254]]

  education: []
  projects: []
  certifications: []
```

### 10.4 Parser metadata

```yaml
profile_parser:
  parser: resume-profile-v1
  parser_version: 1.0.0
  source_extractor: tika
  model_provider: null
  model: null
  reviewed: false
```

## 11. Resume structured parsing

Structured parsing should be layered:

1. Contact regex and normalization.
2. Section detection.
3. Experience-block segmentation.
4. Date parsing.
5. Company/title association.
6. Bullet association.
7. Skill dictionary and alias matching.
8. Statistical or model-assisted entity extraction.
9. Cross-extractor reconciliation.

When parser outputs disagree, retain all outputs and emit a diagnostic rather than silently choosing whichever yields the best evaluation.

### 11.1 Oracle evaluation

Create a manually reviewed `ResumeProfile` for the canonical resume and selected fixtures. Measure:

- Exact field precision, recall, and F1.
- Section detection accuracy.
- Experience-block accuracy.
- Date accuracy.
- Company/title/date association accuracy.
- Bullet association accuracy.
- Skill extraction precision and recall.
- Evidence-span accuracy.

A parser score is a parser score. It must not be reported as hiring fit.

## 12. Skill, title, and occupation normalization

Use multiple sources:

- A small repository-owned engineering alias map.
- O*NET occupation and technology datasets.
- ESCO occupations and skills.
- Exact vendor terminology from the posting.

Example aliases:

```yaml
aliases:
  postgres:
    canonical: postgresql
    labels: [Postgres, PostgreSQL]
  k8s:
    canonical: kubernetes
    labels: [K8s, Kubernetes]
  sre:
    canonical: site_reliability_engineering
    labels: [SRE, Site Reliability Engineering]
```

Normalization must not erase useful distinctions. For example, Java and JavaScript must never share a canonical identity merely because their labels are lexically related.

Every taxonomy release and alias-map hash should be recorded in the run manifest.

## 13. Criterion matching

### 13.1 Match result model

```json
{
  "criterion_id": "req-01",
  "status": "met",
  "method": "hybrid",
  "confidence": 0.91,
  "resume_evidence": [
    {
      "profile_path": "experience[0].bullets[1]",
      "section": "experience",
      "text": "Built Rust services...",
      "start": 1842,
      "end": 1908
    }
  ],
  "explanation": "Rust is explicitly demonstrated in production work.",
  "judge": {
    "kind": "deterministic",
    "provider": null,
    "model": null,
    "prompt_version": null
  }
}
```

### 13.2 Status vocabulary

- `met`
- `partially_met`
- `missing`
- `contradicted`
- `unknown`
- `not_applicable`

`unknown` is materially different from `missing`. A resume does not normally state work authorization, willingness to travel, or every employment preference.

### 13.3 Evidence rules

Each match must identify one or more evidence spans. Evidence can come from:

- Experience bullets.
- Role titles and companies.
- Skills section.
- Projects.
- Education.
- Certifications.
- Summary, if present.

Evidence should be classified by strength:

1. Recent production accomplishment with explicit technology and outcome.
2. Production responsibility with explicit technology or domain.
3. Substantial project with concrete implementation evidence.
4. Education or certification evidence.
5. Isolated skill-list mention.
6. Model inference without explicit wording.

The framework should not treat all mentions as equally strong.

## 14. Evaluation layers and graders

### 14.1 Artifact gate

This is pass/fail and remains outside weighted matching arithmetic.

Checks include:

- Compilation success.
- Page budget.
- Nonempty extraction.
- Reading order.
- Section order and boundaries.
- Contact integrity.
- Job-block contiguity.
- Date format.
- Unicode and glyph integrity.
- Link deduplication.
- Cross-extractor agreement.

### 14.2 Structured field grader

Compares the parsed `ResumeProfile` with a reviewed oracle.

Metrics:

- Precision.
- Recall.
- F1.
- Association accuracy.
- Evidence-span overlap.

### 14.3 Eligibility grader

Handles objective criteria using three-valued logic:

- `pass`
- `fail`
- `unknown`

Examples:

- Geographic eligibility.
- Work authorization.
- Clearance.
- Required certification.
- Degree requirement.
- Minimum years.
- Employment type.
- Schedule or travel constraints.

No missing fact becomes `fail` unless the evaluation profile explicitly defines that rule.

### 14.4 Lexical grader

Measures visible terminology using:

- Exact terms.
- Case-insensitive forms.
- Canonical aliases.
- Acronym/full-form pairs.
- Phrase matching.
- BM25 retrieval.

The lexical grader should report:

- Required terms found.
- Required terms absent.
- Preferred terms found.
- Where each term appears.
- Whether each term appears in evidence or only in a skill list.

It should not report keyword density or reward repeated stuffing.

### 14.5 Semantic retriever

Avoid one embedding for the entire resume and one for the entire posting.

Instead:

1. Split the posting into atomic criteria.
2. Split the resume into evidence units.
3. Embed each unit locally.
4. Retrieve top evidence candidates per criterion.
5. Optionally rerank criterion/evidence pairs with a cross-encoder.
6. Return evidence and confidence, not only cosine similarity.

Metrics:

- Recall@k against reviewed criterion/evidence pairs.
- Mean reciprocal rank.
- NDCG when multiple evidence items are relevant.
- False-positive rate on negative controls.

### 14.6 Evidence-quality grader

Evaluate:

- Explicitness.
- Context.
- Recency.
- Duration.
- Scope.
- Ownership.
- Production versus personal-project context.
- Quantified outcome.
- Repetition or corroboration.

These factors should remain visible. A single weighted value may be derived for sorting but must not replace the individual attributes.

### 14.7 LLM criterion judge

The model receives:

- One atomic criterion.
- A bounded set of retrieved resume evidence.
- Definitions for each status.
- A strict output schema.
- Instructions not to use outside knowledge.
- Instructions to cite evidence spans.

The model returns:

- Status.
- Confidence.
- Evidence IDs.
- Short explanation.
- Ambiguities.
- Missing information.

Reject or retry output that:

- Violates the schema.
- Cites nonexistent evidence.
- Claims facts absent from the supplied input.
- Treats preferred criteria as required.
- Treats unknown as failure without an explicit rule.

### 14.8 Human-lens judges

Optional judges may model distinct review questions:

- Recruiter triage.
- Hiring-manager relevance.
- Technical depth.
- Seniority and scope.
- Career narrative.
- Concision and scanability.

These are qualitative perspectives, not ATS replicas.

### 14.9 Pairwise variant judge

For ambiguous prose quality, prefer pairwise comparison:

> Given criterion X and evidence from variants A and B, which variant communicates stronger supported evidence, or are they equivalent?

Blind the judge to variant labels and randomize ordering to measure positional bias.

## 15. Evaluation output

The primary result is a vector, not a single score.

Example:

```text
Artifact extraction              PASS
Structured-field F1              0.96
Required criteria                8 met / 1 partial / 1 unknown
Preferred criteria               4 met / 3 missing
Objective knockouts              0 failed / 1 unknown
Unsupported claims               0
Lexical visibility               7 of 9 required terms visible
Semantic evidence retrieval      0.84 MRR
LLM pairwise win rate            68% over baseline
Judge disagreement               Moderate on req-07
Page budget                      PASS
```

### 15.1 Optional selection profiles

If a sortable aggregate is useful, define named profiles:

```yaml
profile: senior-infrastructure-v1
weights:
  required_criteria: 0.50
  preferred_criteria: 0.15
  evidence_quality: 0.20
  recruiter_readability: 0.15
hard_gates:
  artifact_extraction: pass
  unsupported_claims: 0
```

Rules:

- Profiles are user-selected.
- Profiles are versioned.
- Raw components remain visible.
- A profile score is never called ATS compatibility.
- Hard gates are evaluated before weighted components.

## 16. Provider architecture

The deterministic evaluator must not depend on an agent SDK.

Use a provider-neutral interface:

```python
class JudgeProvider(Protocol):
    async def evaluate(self, request: JudgeRequest) -> JudgeResult: ...
```

### 16.1 Initial providers

1. `DeterministicJudgeProvider`
2. `LocalOpenAICompatibleProvider`
3. `OpenAIProvider`
4. `PiSidecarProvider`
5. Optional experimental `ClaudeCodeProvider`
6. Optional experimental `CodexProvider`

### 16.2 Python core

Python is the recommended framework core because the repository already uses:

- Python scripts.
- `uv`.
- PEP 723 inline metadata.
- pytest.
- Existing extraction orchestration in Python.

The first release should preserve those conventions. If the project grows beyond a few scripts, introduce a `pyproject.toml` deliberately rather than immediately.

### 16.3 OpenAI boundary

Use a direct model call or Responses API adapter when the framework owns a simple scoring loop.

Use `openai-agents-python` only when the workflow benefits from:

- Managed tool loops.
- Specialist agents.
- Sessions.
- Tracing.
- Guardrails.
- Handoffs.
- Repeatable agent workflow evaluation.

The agent framework should not wrap deterministic local functions merely to make the system look agentic.

### 16.4 Pi boundary

Pi is useful for:

- In-process TypeScript access to multiple configured providers.
- Local model routing.
- Read-only custom tools.
- Structured event handling.
- Bounded mutation or review agents.

The first integration should be a small TypeScript JSON-in/JSON-out sidecar. It should:

- Use an in-memory session.
- Explicitly select the model/provider.
- Use no filesystem write tools for judging.
- Accept a strict request schema.
- Return a strict result schema.
- Record the resolved provider and model.
- Never silently fall back from local to cloud.

### 16.5 Claude Code and Codex boundary

Claude Code and Codex may be used as:

- Exploratory judges.
- Prompt critics.
- Mutation proposers.
- Independent reviewers.
- Framework implementation agents.

They should not initially be canonical graders because their model versions, hidden instructions, tools, and session context may change. Their outputs must be versioned as experimental provider results.

### 16.6 Local-model boundary

Local providers may run through llama.cpp, Ollama, LM Studio, or another OpenAI-compatible endpoint.

Record:

- Endpoint identity without secrets.
- Model ID and model file hash when available.
- Quantization.
- Context length.
- Temperature and sampling settings.
- Prompt version.
- Runtime version.
- Duration.
- Structured-output validity.

## 17. Privacy and data handling

### 17.1 Local processing

The following should remain local by default:

- PDF bytes.
- Extracted resume text.
- Contact details.
- Work-history evidence.
- Job snapshots.
- Local embeddings.
- Local model prompts and responses.
- Evaluation results.

### 17.2 Cloud processing

When using OpenAI, Anthropic, or another cloud provider, visible resume and job text leaves the Mac.

Every cloud-backed run should include:

```yaml
privacy:
  local_only: false
  transmitted_fields:
    - job_criteria
    - retrieved_resume_evidence
  contact_fields_redacted: true
  provider: openai
```

Prefer sending only atomic criteria and retrieved evidence, not the full resume, when the task permits.

### 17.3 Secrets

- Never commit API keys or OAuth tokens.
- Never include secrets in run manifests.
- Never copy provider credential stores into fixtures.
- Record only provider/model identifiers and redacted endpoint metadata.

## 18. Claim ledger and variant safety

### 18.1 Claim model

Create a structured ledger backed by `work-experience/`:

```yaml
claims:
  - id: linkedin-swe-017
    source_file: work-experience/01-linkedin-swe.md
    source_span: [1200, 1510]
    kind: accomplishment
    technologies: [rust, kafka]
    domains: [distributed_systems]
    metrics:
      - value: 40
        unit: percent
        meaning: latency reduction
    approved_resume_language:
      - "Reduced ..."
    sensitivity: public
    reviewed: true
```

### 18.2 Allowed transformations

- Select supported claims.
- Remove supported claims.
- Reorder claims or bullets.
- Shorten wording.
- Expand an acronym accurately.
- Substitute an accurate canonical technology label.
- Move an explicit skill into a relevant evidence-bearing bullet.
- Change emphasis without changing facts.
- Choose among reviewed formulations.

### 18.3 Forbidden transformations

- Invent metrics.
- Change employment dates.
- Change employer or title facts.
- Add technologies not supported by evidence.
- Add unsupported certifications or degrees.
- Inflate individual ownership.
- Turn team outcomes into individual outcomes without support.
- Upgrade prototype work to production work.
- Add an inferred qualification as an explicit fact.

### 18.4 Variant manifest

```yaml
variant_id: rust-infra-004
base_git_commit: "..."
target_jobs:
  - example-runtime-engineer
mutations:
  - kind: reorder
    claim_ids: [linkedin-swe-017, linkedin-swe-004, linkedin-swe-009]
  - kind: rewrite
    claim_ids: [linkedin-swe-017]
    prompt_version: concise-impact-v2
generator:
  kind: model
  provider: local
  model: "..."
source_sha256: "..."
pdf_sha256: "..."
```

Every generated variant should be reviewable as a source diff.

## 19. Optimization loop

The optimizer proposes; deterministic gates and human review decide.

### 19.1 Loop

1. Select target posting set and held-out set.
2. Establish baseline resume metrics.
3. Identify criteria with missing or weak evidence.
4. Search the claim ledger for relevant supported material.
5. Propose bounded source changes.
6. Compile candidate variants in isolated temporary directories.
7. Run artifact gates.
8. Parse and evaluate candidates.
9. Compare against baseline and other candidates.
10. Reject variants that introduce unsupported claims or hard regressions.
11. Inspect pairwise and held-out results.
12. Promote only through an explicit human decision.

### 19.2 Search strategy

Avoid brute-forcing every combination of bullets. Start with factorized experiments:

- Bullet selection.
- Bullet ordering.
- Skills ordering.
- Terminology formulation.
- Concision formulation.
- Section ordering.

Use a small beam or Pareto frontier instead of a single scalar objective.

### 19.3 Pareto dimensions

Potential optimization dimensions:

- Required-criterion coverage.
- Evidence strength.
- Preferred-criterion coverage.
- Recruiter scanability.
- Technical specificity.
- Page usage.
- Cross-role robustness.
- Model-judge agreement.

A variant dominated on every dimension should be removed. A variant with a meaningful tradeoff should remain visible for human selection.

## 20. Evaluation dataset

Use four groups.

### 20.1 Target postings

Jobs the resume may actually target. These drive job-specific tailoring.

Initial size: approximately five.

### 20.2 Role-family holdout

Related roles not used to generate the variant. These detect overfitting and loss of general usefulness.

Initial size: approximately ten.

### 20.3 Negative controls

Clearly different roles that should not receive strong matches. These test whether the evaluator is discriminative instead of generically flattering every resume.

Initial size: approximately three.

### 20.4 Mutation fixtures

Controlled resume defects with known expected consequences:

- Remove one required skill.
- Move a skill from evidence into an isolated list.
- Corrupt a date.
- Scramble reading order.
- Remove quantified impact.
- Replace a standard section heading.
- Add unsupported terminology.
- Duplicate a URL.
- Break contact-field boundaries.
- Replace a production claim with a vague responsibility.

Initial size: ten to fifteen.

## 21. Gold data and oracles

Model-based evaluation without reviewed reference data cannot establish accuracy.

Create small reviewed oracles for:

- Job section boundaries.
- Required/preferred classification.
- Atomic criteria.
- Criterion types.
- Skill aliases.
- Resume fields.
- Criterion-to-resume evidence.
- Expected eligibility states.
- Expected mutation regressions.

Oracle records should include reviewer, date, source hash, and notes about ambiguity.

Do not expand the oracle set until the first small suite proves useful.

## 22. Model evaluation methodology

### 22.1 Structured output

All providers must return a shared schema. Provider-specific prose should not leak into the core evaluation representation.

### 22.2 Repeated trials

For nondeterministic graders:

- Use low temperature where supported.
- Run multiple trials for important cases.
- Record every output.
- Report modal judgment and disagreement.
- Do not hide unstable cases behind an average.

### 22.3 Blind comparisons

- Replace variant names with neutral labels.
- Randomize A/B order.
- Remove irrelevant candidate identity where possible.
- Evaluate whether reversing order changes the winner.

### 22.4 Provider comparison

Compare:

- Deterministic baseline.
- Local model.
- OpenAI model.
- Optional Anthropic model.
- Optional Pi-routed equivalent.

Agreement does not prove correctness, but disagreement identifies cases for review.

### 22.5 Prompt versioning

Every prompt should have:

- Stable ID.
- Version.
- Input schema.
- Output schema.
- Status definitions.
- Evidence requirements.
- Regression cases.

Prompt changes require rerunning the relevant eval suite.

## 23. Reproducibility and manifests

The goal is to make a run explainable and reasonably rerunnable, not to reconstruct every historical execution byte for byte. Capture metadata that is inexpensive and useful for comparison; do not make a hermetic environment a prerequisite for evaluating a resume.

Every run should record:

```yaml
run:
  run_id: 2026-08-01T170000Z-rust-infra-004-example-runtime
  started_at: 2026-08-01T17:00:00Z
  finished_at: 2026-08-01T17:00:07Z
  git_commit: "..."
  git_dirty: false
  host_platform: macos

inputs:
  resume_pdf_sha256: "..."
  resume_source_sha256: "..."
  job_source_sha256: "..."
  job_normalized_sha256: "..."

tools:
  typst: "..."
  poppler: "..."
  tika: "..."
  python: "..."

providers:
  - provider: local
    model: "..."
    prompt_version: criterion-match-v1

taxonomies:
  alias_map_sha256: "..."
  onet_version: "..."
  esco_version: "..."
```

Deterministic layers should be stable under the recorded local environment, but exact historical reproduction across operating-system and tool upgrades is not a v1 requirement. Model outputs do not need to be byte-identical. Record enough provenance to explain material differences and rerun an evaluation on a best-effort basis. Vendoring every binary, pinning the host image, or containerizing the entire toolchain is optional and should be introduced only when a concrete regression problem justifies it.

## 24. CLI design

Proposed commands:

```bash
# Capture and normalize a public posting
uv run scripts/vendor_job.py <url>

# Import any combination of URL, pasted text, HTML, JSON, or canonical YAML
uv run scripts/import_job.py --url <url>
uv run scripts/import_job.py --stdin --source-hint linkedin
uv run scripts/import_job.py --file posting.txt --source-hint unknown
uv run scripts/import_job.py --url <url> --file copied-posting.txt

# Validate an agent-produced canonical record against its exact source
uv run scripts/import_job.py \
  --file jobs/inbox/example/source.txt \
  --canonical jobs/inbox/example/normalized-job.yaml \
  --validate-only

# Validate a normalized posting and inspect criteria
uv run scripts/normalize_job.py jobs/raw/.../manifest.json

# Compile and evaluate one resume against one job
uv run scripts/evaluate_resume.py \
  --resume will_cygan_resume.pdf \
  --job jobs/normalized/example-runtime-engineer.yaml

# Enable selected model providers
uv run scripts/evaluate_resume.py \
  --resume will_cygan_resume.pdf \
  --job jobs/normalized/example-runtime-engineer.yaml \
  --providers deterministic,local,openai

# Compare variants
uv run scripts/compare_variants.py \
  --job jobs/normalized/example-runtime-engineer.yaml \
  --variant baseline \
  --variant rust-infra-004

# Run the complete local evaluation suite
just evaluation-test
```

The first implementation may use PEP 723 single-file scripts. If shared data models and provider code become awkward, migrate deliberately to a package and `pyproject.toml`.

## 25. Report design

Each run should emit:

- `result.json`: canonical machine-readable result.
- `report.md`: concise human review.
- `manifest.yaml`: provenance and runtime configuration.
- Extractor text outputs.
- Optional raw provider responses.
- Optional comparison diff.

### 25.1 Report order

1. Outcome summary.
2. Hard failures.
3. Required criteria.
4. Preferred criteria.
5. Evidence quality.
6. Extraction and field mapping.
7. Judge disagreement.
8. Variant differences.
9. Caveats and untested boundaries.

### 25.2 Required report language

The report should say:

- Which layers were actually run.
- Which tools and providers were used.
- Which criteria came directly from the posting.
- Which conclusions are inferred.
- Which facts remain unknown.
- Whether cloud providers received visible text.
- Whether the result is a target-specific optimization or a general-role evaluation.

## 26. Test strategy

### 26.1 Unit tests

- Schema validation.
- URL/provider detection.
- Vendor field mapping.
- HTML cleaning.
- Required/preferred cue parsing.
- Date parsing.
- Alias normalization.
- Criterion-status logic.
- Evidence-strength rules.
- Composite profile arithmetic.
- Provider response validation.

### 26.2 Fixture tests

- Greenhouse sample.
- Lever sample.
- Ashby sample.
- Schema.org sample.
- Generic HTML sample.
- Missing fields.
- Multiple locations.
- Multiple compensation tiers.
- Malformed HTML.
- Posting with no explicit required section.
- Posting where preferred wording is ambiguous.
- LinkedIn copied-text fixture with only visible content.
- URL-only request whose page cannot be retrieved.
- URL plus copied text representing the same posting.
- Unknown-source text blob.
- Agent-produced canonical YAML.
- Source payload with unmapped vendor fields.
- Two syndicated sources for one logical posting.
- Two similar postings that must not be deduplicated.
- Conflicting compensation or location across sources.
- Source span outside artifact bounds.
- Populated canonical field without provenance.

### 26.3 Cross-source compatibility tests

Build logically equivalent fixtures in several forms:

- Greenhouse JSON.
- Lever JSON.
- Ashby JSON.
- LinkedIn-style copied text.
- Schema.org JSON-LD.
- Generic HTML.
- Plain text.

After normalization, assert semantic equivalence for fields the sources share:

- Title.
- Organization.
- Location.
- Employment and workplace type.
- Responsibilities.
- Required criteria.
- Preferred criteria.
- Compensation when present.

Do not require equivalence for metadata absent from a source. Assert `unknown` rather than a fabricated match.

Compatibility metrics should include:

- Shared-field exact agreement.
- Canonical criterion precision/recall against one reviewed oracle.
- Required/preferred classification agreement.
- Evidence-provenance completeness.
- Unmapped-field retention.
- False deduplication rate.

### 26.4 Resume parsing tests

Reuse the existing broken Typst fixtures and add structured expectations for:

- Company/title/date association.
- Skills extraction.
- Section segmentation.
- Evidence spans.

### 26.5 Matcher tests

- Exact skill match.
- Alias match.
- Acronym/full-form match.
- False-friend rejection, such as Java versus JavaScript.
- Required-any-of semantics.
- Required-all-of semantics.
- Minimum-years calculation.
- Missing versus unknown.
- Contradiction.
- Skill-list-only evidence.
- Strong production evidence.

### 26.6 Model evals

- Correct evidence selection.
- Required versus preferred preservation.
- Unknown-state preservation.
- No outside knowledge.
- No unsupported claim invention.
- Stable structured output.
- Pairwise order reversal.
- Negative controls.

### 26.7 End-to-end tests

Given a vendored job and compiled fixture resume:

1. Validate hashes.
2. Extract text.
3. Build profile.
4. Match criteria.
5. Generate report.
6. Assert expected result vector.
7. Exit nonzero on hard-gate failure.

## 27. Performance and cost controls

- Cache by content hash, parser version, model, and prompt version.
- Retrieve evidence locally before sending anything to an LLM.
- Send atomic criteria and bounded evidence rather than whole documents.
- Run deterministic graders first.
- Skip expensive judges when hard gates fail.
- Support local-only, cloud-only, and mixed profiles.
- Set explicit per-run provider budgets.
- Record token counts and latency where available.
- Use representative subsets for expensive cross-provider comparisons.

## 28. Failure handling

### 28.1 Extraction failure

Stop downstream scoring by default. Report the exact extractor and assertion failure.

### 28.2 Parser disagreement

Retain each parser result. Mark affected fields ambiguous. Do not choose the most favorable interpretation.

### 28.3 Job-normalization ambiguity

Mark criteria `unknown` or `needs_review`. Do not force required/preferred classification.

### 28.4 Model schema failure

Retry only under a bounded policy. If still invalid, record the failure and continue with other graders.

### 28.5 Model disagreement

Surface disagreement. Do not average categorical judgments into false certainty.

### 28.6 Unsupported generated claim

Reject the variant before matching and report the claim-ledger validation failure.

### 28.7 Cloud provider unavailable

Continue with deterministic and local providers when the run profile allows it. Never silently substitute another provider.

## 29. Implementation phases

### Phase 0: Contract and baseline

Deliverables:

- Approve this design.
- Define claim language and forbidden claims.
- Freeze current resume extraction baseline.
- Clarify tracked versus private job snapshots.
- Revise the extraction-only hypothesis boundary.

Completion bar:

- Existing extraction suite passes.
- Core terms and non-goals are agreed.
- No implementation ambiguity about layer boundaries.

### Phase 1: Job vendoring and canonical schema

Deliverables:

- JSON schemas.
- Greenhouse adapter.
- Lever adapter.
- Ashby adapter.
- LinkedIn copied-text adapter.
- Schema.org adapter.
- Generic plain-text and HTML adapters.
- Source-document envelope.
- Field-provenance sidecar.
- Agent-normalization handoff validation.
- Raw snapshot manifests.
- Three vendored postings.
- At least one pasted LinkedIn-style posting.
- Reviewed criteria oracles.

Completion bar:

- One command captures and normalizes each supported source.
- URL-only, text-only, and URL-plus-text inputs use the same canonical pipeline.
- Normalized output validates.
- Every criterion preserves source evidence.
- Every populated canonical field has valid provenance or an explicit reviewed exception.
- Equivalent vendor/text fixtures normalize to equivalent shared semantics.

### Phase 2: ResumeProfile and deterministic matching

Deliverables:

- Canonical resume schema.
- Structured parser.
- Canonical profile oracle.
- Exact and alias matching.
- Eligibility evaluator.
- Evidence-strength rules.
- JSON and Markdown reports.

Completion bar:

- Current resume evaluates against three postings.
- Results separate extraction, mapping, eligibility, and matching.
- Controlled fixtures fail in expected dimensions.

### Phase 3: Local semantic evaluation

Deliverables:

- Local embedding provider.
- Criterion-to-evidence retrieval.
- Optional local reranker.
- Retrieval metrics against reviewed evidence.

Completion bar:

- Semantic retrieval improves recall over exact matching without unacceptable false positives on negative controls.

### Phase 4: Model-provider adapters

Deliverables:

- Strict judge schemas.
- Local LLM adapter.
- OpenAI adapter.
- Pi sidecar.
- Prompt registry.
- Repeated-run and disagreement reporting.

Completion bar:

- Providers consume identical cases and emit the shared result schema.
- Cloud transmission is explicit.
- No provider silently falls back.

### Phase 5: Variant generation and comparison

Deliverables:

- Claim ledger.
- Variant manifests.
- Bounded mutation operations.
- Isolated compilation.
- Pairwise comparison.
- Pareto report.

Completion bar:

- At least three controlled variants can be generated, compiled, evaluated, and compared without modifying the canonical resume.
- Unsupported claims are rejected.

### Phase 6: Optimization loop

Deliverables:

- Target, holdout, negative, and mutation datasets.
- Candidate search strategy.
- Promotion gate.
- Cost and plateau controls.

Completion bar:

- A promoted variant improves a stated target metric without extraction regressions, unsupported claims, or unacceptable holdout degradation.

### Phase 7: Optional authorized ATS UAT

Deliverables depend on access:

- Authorized sandbox upload.
- Hand-reviewed ATS field output.
- Comparison with local `ResumeProfile`.
- Documented differences.

Completion bar:

- Claims remain limited to the tested vendor, configuration, and date.

## 30. Initial release scope

The smallest useful first release should include:

1. Three job postings from Greenhouse, Lever, or Ashby.
2. Canonical job schema and reviewed criteria.
3. Current resume plus three controlled broken variants.
4. Existing extraction gate.
5. Canonical resume profile.
6. Deterministic eligibility and lexical matching.
7. Evidence-backed JSON and Markdown report.
8. No LLM dependency.

Only after this deterministic slice works should the project add:

1. One local embedding model.
2. One local LLM judge.
3. One cloud judge.
4. Pairwise variant evaluation.

## 31. Completion definition for the framework

The framework is operational when:

> Given a resume PDF and a vendored job posting, one command produces a reproducible result that separately reports extraction integrity, structured field mapping, eligibility, criterion coverage, semantic evidence, and optional model judgment, with every conclusion tied to source evidence and every untested proprietary boundary stated explicitly.

The optimization system is operational when:

> Given a baseline resume, an approved claim ledger, and target plus held-out postings, the system can generate bounded variants, reject unsupported claims, compile and evaluate each variant, report tradeoffs on a Pareto frontier, and leave promotion to an explicit human decision.

## 32. Non-goals

- Claiming to clone Greenhouse, Workday, Lever, iCIMS, or another ATS.
- Predicting callbacks or offers.
- Producing a universal ATS percentage.
- Keyword stuffing.
- Hiding text or manipulating parsers deceptively.
- Automatically submitting applications.
- Scraping authenticated or private recruiting data.
- Replacing human review.
- Letting a model invent resume facts.
- Optimizing only against one job without held-out checks.
- Treating model agreement as ground truth.
- Treating extraction success as structured mapping or hiring success.

## 33. Risks and mitigations

### Proxy Goodharting

Risk: The optimizer learns the grader rather than improving the resume.

Mitigation:

- Multiple independent layers.
- Held-out jobs.
- Negative controls.
- Pairwise human review.
- Raw metrics.
- Prompt and model rotation for audits.

### Model bias and instability

Risk: Model judgments vary or encode inappropriate preferences.

Mitigation:

- Evidence-only prompts.
- Identity blinding where possible.
- Repeated trials.
- Order reversal.
- Multiple providers.
- Human adjudication.

### False confidence from normalization

Risk: Aliases or taxonomies overstate equivalence.

Mitigation:

- Versioned alias map.
- Directional relationships where needed.
- Exact source evidence.
- False-friend tests.

### Privacy leakage

Risk: Resume content or contact data is sent to cloud providers.

Mitigation:

- Local-first defaults.
- Field-level redaction.
- Atomic evidence transmission.
- Explicit run manifests.
- No secrets in artifacts.

### Overfitting to target postings

Risk: A highly tailored resume becomes brittle for nearby roles.

Mitigation:

- Role-family holdout.
- General baseline comparison.
- Pareto analysis.
- Explicit target-specific labeling.

### Unsupported claim generation

Risk: A model writes plausible but false achievements.

Mitigation:

- Claim ledger.
- Claim IDs on every mutation.
- Deterministic claim validation.
- Human diff review.
- Zero unsupported-claim hard gate.

## 34. Open decisions before implementation

1. Should raw public job snapshots be tracked or kept in a private/ignored directory?
2. When should the repository move from PEP 723 scripts to a `pyproject.toml` package?
3. Which local embedding model should establish the first semantic baseline?
4. Which local LLM endpoint and model should be the first judge?
5. Should the OpenAI integration use a direct Responses adapter first or begin with `openai-agents-python` for tracing?
6. Should Pi be integrated through SDK sidecar, RPC, or JSON CLI mode?
7. Which contact and identity fields should be redacted before cloud evaluation?
8. What constitutes an acceptable holdout regression for a target-specific variant?
9. Which claims in `work-experience/` are approved for public resume use?
10. Should the canonical resume remain one monolithic Typst file or move toward data-driven content selection?
11. Which job families define the first target and holdout sets?
12. Should an LLM-normalized posting require human review before any optimization run, or only before promotion/oracle use?
13. Should source extensions be stored inline or as a separate sidecar?
14. What confidence threshold should require manual reconciliation across syndicated sources?

The storage and schema-authority decision is resolved: Pydantic models are authoritative, YAML is the preferred human-reviewed representation, and JSON is the preferred generated or interchange representation. Both must validate through the same models.

## 35. Recommended decisions

Unless later evidence changes them:

1. Keep the framework core in Python.
2. Keep deterministic evaluators independent of agent SDKs.
3. Use Pydantic models as the schema authority, generate JSON Schema from them, use YAML for reviewed records, and use JSON for generated results.
4. Track schemas, normalizers, prompts, oracles, and small public fixtures.
5. Keep bulk/raw/private captures and run outputs ignored by default.
6. Start with Greenhouse, Lever, Ashby, and Schema.org.
7. Keep extraction as a hard gate outside weighted scoring.
8. Use criterion-level matching instead of document-level similarity.
9. Start with deterministic matching before embeddings or LLMs.
10. Use a Pi JSON sidecar only after the provider-neutral judge contract exists.
11. Use direct OpenAI scoring before adding a multi-agent workflow.
12. Add Agents SDK tracing and evals only when specialist workflows justify them.
13. Require claim-ledger provenance before generating resume variants.
14. Use pairwise comparisons and Pareto results instead of one master score.
15. Require an explicit human promotion decision.
16. Treat URL, pasted text, HTML, JSON, and canonical records as first-class ingestion modes.
17. Require field-level provenance, not only posting-level provenance.
18. Preserve unknown and conflicting values instead of selecting the most complete-looking source.
19. Treat LinkedIn copy/paste as the baseline LinkedIn path unless authorized partner data is supplied.
20. Validate Codex, Claude Code, Pi, and local-LLM normalization through the same schema and evidence checks.
21. Treat user-supplied job inputs as trusted and leave adversarial-input defenses outside the v1 scope.
22. Use lightweight run manifests and best-effort rerunnability; do not require hermetic or byte-identical reproduction.

## 36. References

- Schema.org JobPosting: <https://schema.org/JobPosting>
- Google JobPosting structured data: <https://developers.google.com/search/docs/appearance/structured-data/job-posting>
- Greenhouse Job Board API: <https://developer.greenhouse.io/job-board.html>
- Lever Postings API: <https://github.com/lever/postings-api>
- Ashby Job Postings API: <https://developers.ashbyhq.com/docs/public-job-posting-api>
- O*NET database: <https://www.onetcenter.org/database.html>
- ESCO downloads: <https://esco.ec.europa.eu/en/use-esco/download>
- Sentence Transformers semantic similarity: <https://sbert.net/docs/sentence_transformer/usage/semantic_textual_similarity.html>
- OpenAI Agents guidance: <https://developers.openai.com/api/docs/guides/agents>
- OpenAI agent evaluations: <https://developers.openai.com/api/docs/guides/agent-evals>
- OpenAI Agents SDK for Python: <https://github.com/openai/openai-agents-python>
- LinkedIn Job Posting API schema: <https://learn.microsoft.com/en-us/linkedin/talent/job-postings/api/job-posting-api-schema>
- LinkedIn Job Posting API overview: <https://learn.microsoft.com/en-us/linkedin/talent/job-postings/api/sync-job-postings>
