---
name: revit-development
description: Use when developing, reviewing, testing, packaging, or migrating C# Revit add-ins, modeless tools, Revit API integrations, or multi-version Revit builds.
---

# Revit C# development

Revit owns the runtime, API context and model. Preserve upstream practices within those boundaries.

For project/build changes, load [project-structure](../project-structure/SKILL.md); for C#, load [csharp-coding-standards](../csharp-coding-standards/SKILL.md). Apply Revit host constraints.

Keep business logic in an independently buildable core:

```text
Core           plain .NET types and logic; no Autodesk/WPF references
RevitAdapter   → Core; API access, commands and presentation
```

Commands and UI delegate business decisions to Core. Build and test Core without Revit before integrating the adapter.

## Establish the target before coding

Read [versions and API migration](references/versions.md). Record **year/update, minimum supported update, API reference builds, runtime, TFM and deployment location**; label assumptions and check supplied references. Verify each supported host/API combination.

## Keep the API boundary small

Read [execution and performance](references/execution.md) for any model access, modeless UI, asynchronous work or transaction change.

- **Read-only:** query → detached snapshot → pure calculation → presentation. Filter in valid API context; extract only needed values.
- **Modification:** snapshot → pure computation → revalidate → apply. Include document/element identity and original values for later resolution or modification. Re-enter valid API context, verify current state, then apply changed values in bounded transactions.

Domain contracts contain detached values, never `Document`, `Element`, `Parameter`, `XYZ` or lazy API projections. Bounded CPU parallelism belongs in the domain.

API access requires Revit context, not just the main thread. WPF dispatch, workers and continuations after `await` do not establish it. Modeless work uses `ExternalEvent` (queued, not immediate). Never span `await`/callbacks with transactions/groups.

## Select dependencies deliberately

Read [packages and testing](references/ecosystem.md) before adding a wrapper, API package or test harness. Pin exact package versions per host; inspect their assets and transitive dependencies. Revit supplies its API DLLs; do not ship private copies. No trimmed/Native AOT/self-contained publishing for the in-process add-in. Separate companion executables have their own deployment choices.

## Required output when implementing

- Target record, thin host adapter and verification of the independent business logic.
- For writes/deferred work: stale-input, transaction/undo and cancellation policies.
- For performance claims: measurements on representative models.
- Build every requested target. Use compiler diagnostics to correct code, references and target settings, then rebuild. Report compilation, tests, host/UI execution and deployment separately as **passed, failed or unverified**. Deployment succeeds only after every required copy succeeds.

Use the exact release SDK/reference for member availability and The Building Coder for experience and rationale. Historical samples and dated source links require rechecking before claiming support for later releases.
