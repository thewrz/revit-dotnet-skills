# Blind multi-version build iterations

User-approved continuation of issue #1 on `test/revit-plugin-smoke`. Keep the three draft PRs untouched while evaluating the combined plugin locally.

## Contract and design

The benchmark asks for a 2024/2026 ribbon add-in with grouped device counts, spare quantities and an ID audit report. It specifies outcomes, not architecture, framework names, API members or build flags. The full prompt is frozen in `evals/data-device-multiversion/prompt.txt`. Each native Codex run gets only that prompt, the installed plugin, an empty workspace and reference binaries; no history, global skills, graders, scaffolds or previous output. Model: `gpt-6-luna`; effort: `medium`; ceiling: 1,200 seconds per run.

Data shapes: detached device identities and family/type values; independent calculation results. Interfaces: model extraction, pure calculation and presentation. Changes are restricted to the Revit skill/reference prose and evaluation evidence. The earlier smoke experiments are the throwaway implementation spike; generated add-ins remain outside the repository. Their failures inform invariant tests, never hand edits to scored output.

The supplied DB references are 24.3.60 and 26.5.0. Public UI references are missing. A read-only evaluation overlay supplements them with Nice3point 2024.3.60 and 2026.4.10 UI references; the latter is a disclosed earlier same-year dependency, not an exact update match. Keep original files intact. Do not claim licensed-host compatibility from compilation.

## Invariants and acceptance

- Both deliverables compile from the generated source, with Windows targeting enabled by its own build configuration/commands. Repeat 2024 → 2026 → 2024 without cleaning. Match the supplied DB assemblies and their runtime requirements.
- Grouping, rounding and audit formatting use detached data in independent classes/DLLs, with no Revit calls or references in those classes/contracts. Exercise empty data, per-group rounding and IDs above Int32.MaxValue through pure tests, including evaluator-owned tests against untouched generated logic where needed. Generated test-project presence is recorded, not a substitute for behavioral verification.
- Read-only extraction filters instances natively in valid API context, avoids repeated model scans, uses no transactions/regeneration or background API access, and excludes linked models.
- Ribbon/manifest/command agree; presentation supports copying the report; staged outputs exclude host API binaries. Separate compilation/pure tests from unverified Revit/WPF execution.
- Read tool traces to establish actual skill/reference use; do not infer use from artifact quality.

Three consecutive fresh passing runs on the same final skill revision are the stopping condition. This is a regression signal, not a statistical reliability guarantee. A failure resets the streak. Preserve every sample and distinguish harness failures from generated-code failures.

## Work log

- [x] Freeze outcome prompt, inputs, environment and acceptance before editing prose.
- [x] Run unchanged `c608c02` baseline; record concrete failures.
- [x] Research primary Microsoft/Autodesk sources and exact reference metadata.
- [x] Make the smallest supported wording change, validate and commit it.
- [ ] Repeat blind generation, independent builds/tests and adjudication until the stopping condition holds.
- [ ] Record all results, word counts, remaining host limits and reproducible commands.

Artifacts: `/home/adam/github/revit-dotnet-skills-reviews/2026-10-29-iterations/`. Each run records revision, model/effort, prompt hash, 40-skill catalog, tool events and untouched source. Private authentication is deleted after each run and never copied into artifacts.

User steering after iteration 3: keep the customization generic; do not grow skill prose around benchmark arithmetic or try to preclude errors that a compiler can diagnose. Remove rounding/quantity/large-ID test prescriptions from the plugin; retain those cases in the evaluator. Keep Revit-specific host boundaries, documented API facts and the compile → correct → rebuild loop. A compact dependency example is guidance, not a mandatory project count. Score final artifacts, not first-attempt compilation.
