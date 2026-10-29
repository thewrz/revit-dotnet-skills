# Revit skill wording implementation plan

> Execute inline; the user approved these edits and specified the benchmark model and sequence.

**Goal:** Apply concise behavior guidance and compare unchanged versus revised skills on the same task.
**Architecture:** Keep the Revit entry point as a conditional router with focused references; use isolated native Codex CLI plugin installs for evaluation.
**Spec:** `docs/superpowers/specs/2026-10-29-revit-wording-design.md`.

## Constraints and review focus

- Old revision: `01b11388986360b6340b75d3e064acf90502db89`; exact prompt body from its eval fixture.
- Both samples: `gpt-6-luna`, medium effort, fresh home/workspace, same tools and 1,200-second ceiling; old completes before new starts.
- No global instructions, prior outputs, evaluation criteria or review notes in child context.
- Preserve API context/thread safety, separated business logic, minimum API targeting and upstream preferences.
- Generated code is evidence; any diagnostic fixes use a separate copy.
- One pair is requested; it tests behavior, not reliability or cross-model improvement.

## Task 1: Concise wording changes

Files: `skills/revit-development/SKILL.md`, its `references/versions.md` and `references/ecosystem.md`, and descriptions in `skills/project-structure/SKILL.md` and `skills/csharp-coding-standards/SKILL.md`.

- [x] Preserve old package and start isolated baseline.
- [x] Replace wording using the approved six changes; keep the entry point approximately its current length.
- [x] Run manifest validators, existing six tests, index generation and diff checks; commit locally.

## Task 2: Same-prompt comparison

- [x] Finish old run, then launch new revision with identical prompt/model/effort/isolation.
- [x] Inspect skill reads, generated scope, pure business-logic boundary, target contract, transactions, packaging and verification honesty.
- [x] Compile/test generated artifacts where feasible, including sequential targets if claimed.
- [x] Save raw outputs, sanitized tool evidence and a comparison report. Report regressions as well as improvements.

Outcome: routing improved (both C# and project-structure read); both generated projects compile with reference warnings, while the revised output omits the old output's update-level runtime boundary. Same prompt SHA-256: `69930f6b0d60fd303e4a704b9d55daf88a80cd8da80a3e10ce2bc892206c43e6`. Tested skill commit: `08a2034`. Full evidence is in `/home/adam/github/revit-dotnet-skills-reviews/2026-10-28-luna-comparison/COMPARISON.md`. No generated source was corrected for scoring.
