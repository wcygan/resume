# Architecture second pass — 2026-08-10

## Question and method

**Question.** After the recent artifact, PDF-evidence, extraction-expectation,
validation-plan, and Golden-stress centralizations, is there a residual module
that should be deepened now?

**Method.** This is a source-and-history review at `d51e31b` using repository
files as primary evidence. I inspected the recent hot spots, their executable
adapters, and their focused tests. `CONTEXT.md` and `docs/adr/` were absent at
this revision; no domain term or recorded decision was therefore available to
constrain the scan. The recent history itself records the five completed
centralizations: artifact provenance (`e1cc369`), PDF evidence (`dba41dd`),
expectations (`aac7d40`), validation plans (`b6895ff`), and semantic Golden
stress cases (`be4c459`).

## Inspected scope

- Artifact construction and freshness: `resume_tools/artifact.py:50-307`,
  including the shared `CompileRequest`, single compiler policy, provenance,
  and freshness evaluation.
- PDF evidence and active extraction: `resume_tools/pdf_evidence.py:1-320` and
  `scripts/extraction_check.py:480-668`.
- Validation orchestration and its executable adapters:
  `resume_tools/validation.py:70-225`, `justfile:8-50`,
  `.github/workflows/compile-resume.yml:26-43`, and
  `.github/workflows/extraction-check.yml:72-87`.
- Golden evaluation and stress:
  `.agents/skills/resume-parsability/scripts/evaluate_golden_resume.py:55-705`,
  `.agents/skills/resume-parsability/scripts/evaluate_golden_stress_matrix.py:152-343`,
  `resume_tools/golden_stress.py:47-442`, and
  `tests/fixtures/golden-resume/golden-resume-stress-matrix.json:1-95`.
- Test surfaces: `tests/test_artifact.py:31-190`,
  `tests/test_validation.py:28-160`, `tests/conftest.py:51-89`,
  `tests/test_extraction_check.py:1-227`, and
  `tests/test_golden_resume_stress.py:20-339`.

## Findings

### Observation: the completed modules have real depth

`artifact` accepts a `CompileRequest` and owns the Typst command, dependency
evidence, provenance writing, and freshness checks; both the active resume and
Golden paths construct that same request shape. This is a deep module: deleting
it would reintroduce compiler policy, provenance, and freshness complexity in
the CLI, live-preview adapter, negative-fixture fixture, workflows, and stress
dispatcher. [artifact.py:50-137](../../resume_tools/artifact.py#L50-L137)
[artifact.py:165-292](../../resume_tools/artifact.py#L165-L292)
[dev.py:15-43](../../scripts/dev.py#L15-L43)
[conftest.py:51-73](https://github.com/wcygan/resume/blob/d51e31b737d4776328f104e0d56ba33f6ec65f79/tests/conftest.py#L51-L73)

`pdf_evidence` deliberately owns discovery and process mechanics while callers
choose their evidence policy. The active extraction module accepts whichever
extractors are present, whereas the Golden evaluator requires the fuller tool
set. This is an intentional seam with two adapters, not duplicate policy.
[pdf_evidence.py:1-7](../../resume_tools/pdf_evidence.py#L1-L7)
[pdf_evidence.py:83-165](../../resume_tools/pdf_evidence.py#L83-L165)
[extraction_check.py:72-87](https://github.com/wcygan/resume/blob/d51e31b737d4776328f104e0d56ba33f6ec65f79/scripts/extraction_check.py#L72-L87)
[evaluate_golden_resume.py:87-104](https://github.com/wcygan/resume/blob/d51e31b737d4776328f104e0d56ba33f6ec65f79/.agents/skills/resume-parsability/scripts/evaluate_golden_resume.py#L87-L104)

`validation` owns ordered check membership and evidence locations. The justfile
and GitHub workflow adapters invoke the module rather than reconstructing its
plan, and focused tests pin that delegation. This concentrates plan changes in
one module and gives callers leverage through a small interface.
[validation.py:1-8](../../resume_tools/validation.py#L1-L8)
[validation.py:70-149](../../resume_tools/validation.py#L70-L149)
[justfile:28-50](../../justfile#L28-L50)
[extraction-check.yml:78-87](../../.github/workflows/extraction-check.yml#L78-L87)
[test_validation.py:124-138](../../tests/test_validation.py#L124-L138)

### Candidate ledger

| Candidate | Evidence | Deletion test | Strength | Recommendation |
| --- | --- | --- | --- | --- |
| Deepen Golden evaluation behind a repository-owned module, leaving both skill files as adapters | The evaluator owns tool policy, text checks, geometry checks, evidence-file interpretation, report assembly, and process orchestration. The direct Golden path returns only an exit status plus a written report; the stress adapter invokes it by subprocess and reaches into nested report fields and generated render paths. [evaluate_golden_resume.py:513-705](https://github.com/wcygan/resume/blob/d51e31b737d4776328f104e0d56ba33f6ec65f79/.agents/skills/resume-parsability/scripts/evaluate_golden_resume.py#L513-L705) [evaluate_golden_stress_matrix.py:245-310](https://github.com/wcygan/resume/blob/d51e31b737d4776328f104e0d56ba33f6ec65f79/.agents/skills/resume-parsability/scripts/evaluate_golden_stress_matrix.py#L245-L310) [pdf_evidence.py:260-316](../../resume_tools/pdf_evidence.py#L260-L316) | Deleting a repository module would reintroduce evaluator invocation, report-schema knowledge, and evidence-path knowledge in the direct Golden adapter and stress adapter. Complexity would reappear across two production callers. | Strong | Deepen now: one repository module should own Golden evaluation, evidence paths, and a structured result; retain the skill executables as thin adapters. Do not change the reviewed oracle or Golden policy in the same change. |
| Add a Golden-case artifact helper | The stress adapter constructs a detailed `CompileRequest` and separately checks dependency inputs; ordinary artifact requests own the standard source/output/provenance layout. [evaluate_golden_stress_matrix.py:201-243](https://github.com/wcygan/resume/blob/d51e31b737d4776328f104e0d56ba33f6ec65f79/.agents/skills/resume-parsability/scripts/evaluate_golden_stress_matrix.py#L201-L243) [artifact.py:50-60](../../resume_tools/artifact.py#L50-L60) [artifact.py:97-114](../../resume_tools/artifact.py#L97-L114) | Only the stress adapter currently needs this variant. Deleting a helper would not spread complexity across multiple callers. | Speculative | Defer until another fixture-variant adapter needs the same construction policy. |
| Move Golden stress semantic target mapping into data | Semantic subjects map to a deliberately limited registry; the manifest has concise semantic mutations and the module rejects unsupported targets before materialization. [golden_stress.py:47-99](https://github.com/wcygan/resume/blob/d51e31b737d4776328f104e0d56ba33f6ec65f79/resume_tools/golden_stress.py#L47-L99) [golden_stress.py:102-191](https://github.com/wcygan/resume/blob/d51e31b737d4776328f104e0d56ba33f6ec65f79/resume_tools/golden_stress.py#L102-L191) [golden-resume-stress-matrix.json:16-95](../../tests/fixtures/golden-resume/golden-resume-stress-matrix.json#L16-L95) | Deleting the registry would move target validation and reviewed-oracle synchronization into the manifest, dispatcher, or tests. Complexity would spread. | Speculative | Keep the registry. A second fixture schema or another independently shaped mutation adapter would make a data-driven seam real; one adapter does not justify it today. |

## Explicit non-candidates

- **Artifact construction.** Not a shallow module: callers share the compiler
  policy and provenance implementation through `CompileRequest`; the test
  surface exercises the policy rather than rebuilding command flags.
  [artifact.py:97-137](../../resume_tools/artifact.py#L97-L137)
  [test_artifact.py:160-176](../../tests/test_artifact.py#L160-L176)
- **PDF evidence.** Do not merge caller policy into this module. Its current
  interface supports two adapters with intentionally different tool
  requirements, so centralizing policy would reduce locality.
  [pdf_evidence.py:109-129](../../resume_tools/pdf_evidence.py#L109-L129)
- **Validation-plan adapters.** Do not add another planning module. The
  justfile and workflows already delegate to one implementation, and the
  full plan is tested for ordering and fail-fast behavior.
  [validation.py:123-149](../../resume_tools/validation.py#L123-L149)
  [test_validation.py:53-99](../../tests/test_validation.py#L53-L99)
- **Active extraction checks.** Its in-process test fixture calls the same
  `load_fixtures` and `evaluate_pdf` interface as its executable path, while
  the Golden evaluator intentionally uses a distinct reviewed oracle and PDF
  geometry checks. A shared abstraction now would enlarge the interface
  without a second implementation need.
  [conftest.py:76-89](https://github.com/wcygan/resume/blob/d51e31b737d4776328f104e0d56ba33f6ec65f79/tests/conftest.py#L76-L89)
  [extraction_check.py:480-549](https://github.com/wcygan/resume/blob/d51e31b737d4776328f104e0d56ba33f6ec65f79/scripts/extraction_check.py#L480-L549)
  [evaluate_golden_resume.py:252-457](https://github.com/wcygan/resume/blob/d51e31b737d4776328f104e0d56ba33f6ec65f79/.agents/skills/resume-parsability/scripts/evaluate_golden_resume.py#L252-L457)
- **Three extraction-check adapters.** `detect_tika`, `build_extractors`, and
  `run_extractor` are shallow pass-through modules over `pdf_evidence`; their
  deletion would concentrate no complexity because the `evaluate_pdf` caller
  can use the existing `pdf_evidence` interface directly. This is a small
  cleanup, not a deepening opportunity. [extraction_check.py:72-87](https://github.com/wcygan/resume/blob/d51e31b737d4776328f104e0d56ba33f6ec65f79/scripts/extraction_check.py#L72-L87)
- **Private Golden-stress test reach-through.** One test calls
  `_record_for` directly, past the module's intended `materialize_case`
  interface. Replace that assertion with the materialized data result only
  when changing the test area; it is test-surface cleanup, not a reason to
  widen the module interface. [golden_stress.py:230-237](https://github.com/wcygan/resume/blob/d51e31b737d4776328f104e0d56ba33f6ec65f79/resume_tools/golden_stress.py#L230-L237)
  [golden_stress.py:419-442](https://github.com/wcygan/resume/blob/d51e31b737d4776328f104e0d56ba33f6ec65f79/resume_tools/golden_stress.py#L419-L442)
  [test_golden_resume_stress.py:319-339](https://github.com/wcygan/resume/blob/d51e31b737d4776328f104e0d56ba33f6ec65f79/tests/test_golden_resume_stress.py#L319-L339)

## Recommendation

At reviewed revision `d51e31b`, one **Strong** candidate remained: deepen Golden
evaluation into a repository module, while retaining the two skill files as
adapters. The direct Golden adapter and stress adapter demonstrated a real seam;
both needed one structured result rather than a subprocess/report-file
protocol. The Golden-case helper remained deferred.

## Implementation follow-up

The current worktree implements the Strong candidate. `resume_tools.golden_evaluation`
now owns evaluation policy, evidence paths, reports, and the structured result;
its only public operation is `evaluate`. The direct and stress executables
delegate through that interface, and the stress adapter no longer parses a
subprocess report. The two cleanup findings were also resolved: extraction uses
`pdf_evidence` directly, and Golden-stress tests observe materialized data
without calling `_record_for`.
[golden_evaluation.py:50-86](../../resume_tools/golden_evaluation.py#L50-L86)
[golden_evaluation.py:532-742](../../resume_tools/golden_evaluation.py#L532-L742)
[evaluate_golden_resume.py:18-73](../../.agents/skills/resume-parsability/scripts/evaluate_golden_resume.py#L18-L73)
[evaluate_golden_stress_matrix.py:215-306](../../.agents/skills/resume-parsability/scripts/evaluate_golden_stress_matrix.py#L215-L306)

## Uncertainty

This review establishes source-level structure and focused test surfaces; it
does not prove the future rate of Golden evaluator change or external ATS
behavior. The latter remains explicitly untested in the evaluator's report.
[evaluate_golden_resume.py:691-704](https://github.com/wcygan/resume/blob/d51e31b737d4776328f104e0d56ba33f6ec65f79/.agents/skills/resume-parsability/scripts/evaluate_golden_resume.py#L691-L704)
