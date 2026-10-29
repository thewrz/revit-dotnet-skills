---
name: revit-development
description: Use when developing, reviewing, testing, packaging, or migrating C# Revit add-ins, modeless tools, Revit API integrations, or multi-version Revit builds.
---

# Revit C# development

Revit owns the runtime, API context and model. Preserve upstream practices within those boundaries.

For project/build changes, load [project-structure](../project-structure/SKILL.md); for C#, load [csharp-coding-standards](../csharp-coding-standards/SKILL.md). Apply Revit host constraints.

For features with calculations, first build a portable domain project and runnable tests; then add the Revit/UI adapter. Keep the requested scope.

## Establish the target before coding

Read [versions and API migration](references/versions.md). Inspect assemblies before choosing targets; folder years/package labels are insufficient. Record **year/update, minimum supported update, each API reference build, runtime, TFM and deployment location**; label assumptions. Revit 2025.5/2026.5 use .NET 10; earlier updates use .NET 8. Verify each supported host/API combination.

## Keep the API boundary small

Read [execution and performance](references/execution.md) for any model access, modeless UI, asynchronous work or transaction change.

- **Read-only:** query → detached snapshot → pure calculation → presentation. Filter in valid API context; extract only needed values.
- **Modification:** snapshot → pure computation → revalidate → apply. Include document/element identity and original values for later resolution or modification. Re-enter valid API context, verify current state, then apply changed values in bounded transactions.

The domain owns calculations and report formatting; commands/windows delegate to it. Contracts contain detached values, never `Document`, `Element`, `Parameter`, `XYZ` or lazy API projections. Bounded CPU parallelism belongs here.

Main-thread execution alone is insufficient: WPF Dispatcher callbacks and continuations after `await` do not establish Revit API context. Modeless requests use `ExternalEvent`; raising it is a dispatch request, not immediate execution. API reads are not safe in `Task.Run`, actors, timers or `Parallel.ForEach`. Do not keep a transaction or group open across `await` or callbacks.

## Select dependencies deliberately

Read [packages and testing](references/ecosystem.md) before adding a wrapper, API package or test harness. Pin exact package versions per host; inspect their assets and transitive dependencies. Revit supplies its API DLLs; do not ship private copies. No trimmed/Native AOT/self-contained publishing for the in-process add-in. Separate companion executables have their own deployment choices.

## Required output when implementing

- Target record, thin host adapter and executed pure tests covering calculation boundaries and identity preservation.
- For writes/deferred work: stale-input, transaction/undo and cancellation policies.
- For performance claims: measurements on representative models.
- Build every requested target; fix errors and rerun affected checks. Report compilation, tests, host/UI execution and deployment separately as **passed, failed or unverified**. Deployment succeeds only after every required copy succeeds.

Use the exact release SDK/reference for member availability and The Building Coder for experience and rationale. Historical samples and dated source links require rechecking before claiming support for later releases.
