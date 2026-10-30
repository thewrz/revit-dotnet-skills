# Revit plugin smoke experiment

The current Codex multi-version experiment uses [this outcome prompt](data-device-multiversion/prompt.txt); its [results](data-device-multiversion/RESULTS.md) report the full five-run sample against the final lean wording. The public copy substitutes `<REVIT_API_ROOT>` for the local reference path. Resolve it before freezing new runs; historical prompt hashes refer to the unchanged original inputs retained outside this repository.

## Original Claude Code smoke procedure

The initial spike tested the combined PR #2/#3/#4 content before later review recommendations. It is associated with existing issue #1. The test branch contains three explicit merges from the upstream base; before these evaluation files were added, its tree exactly matched PR #4.

The native Claude Code plugin evaluator runs the same natural-language add-in request in fresh contexts with and without the plugin. No conversation history, handoff, project instructions, scaffold, or extra system prompt is supplied. Run one sample per arm at high effort; this is a smoke experiment, not a reliability estimate. Do not revise the plugin or prompt midway to make the result pass.

The automated graders measure observable skill invocation, two reference reads, and artifact presence. They do not certify implementation correctness. Manually inspect both outputs for:

- A distinct ribbon tab/panel with one working push button and a matching application manifest.
- Data Device instances, filtered by built-in category; explicit whole-document versus view/linked-model scope.
- Valid Revit API context, no worker-thread API reads, no transactions/regeneration for this read-only query.
- Native filtering/counting without repeated model scans; separate presentation and plain result/domain types.
- Explicit supported Revit year/update and matching runtime/API references, with no false universal .NET mapping.
- WPF/native dialog ownership, usable layout, and no retained live document/element objects in UI data.
- Host API DLL exclusion, compatible dependencies, install instructions, and honest validation limits.

Stage only `.claude-plugin/plugin.json`, `skills/`, `agents/`, `LICENSE`, and `evals/` into the temporary plugin directory. Keep repository audit records and this conversation out of the child context. The evaluator hides the eval directory, including these criteria.

Run from the staged plugin:

```sh
CLAUDE_CODE_DISABLE_BUNDLED_SKILLS=1 CLAUDE_CODE_EFFORT_LEVEL=high claude plugin eval . \
  --model claude-fable-5-1 --runs 1 --ablation with-without --concurrency 2 \
  --allow-tools Bash Write Edit WebFetch WebSearch --disallow-tools Agent TaskStop \
  --no-scaffold --no-publish --trust-plugin --keep-temp \
  --output-dir /path/to/results --report /path/to/results/report.html
```

The run has a 1,200-second limit per arm and an outer 2,700-second process ceiling. Keep reports local. Preserve generated code and sanitized tool traces, then assess them without editing the outputs. Compile where this Linux environment permits; do not describe compilation as licensed Revit/WPF host execution.

Co-authored by Codex.
