---
name: revit-development
description: Use when developing, reviewing, testing, packaging, or migrating C# Revit add-ins, modeless tools, Revit API integrations, or multi-version Revit builds.
---

# Revit C# development

Revit owns the runtime, API context and model. Preserve upstream practices within those boundaries.

When creating/changing projects or build settings, load [project-structure](../project-structure/SKILL.md); when implementing C#, load [csharp-coding-standards](../csharp-coding-standards/SKILL.md). Revit host constraints govern their application.

Build the smallest requested end-to-end feature first. Additional breakdowns, dependencies and supported targets require an explicit requirement.

## Establish the target before coding

Read [versions and API migration](references/versions.md). Record: **Revit year/update, minimum supported update, exact API reference build, host runtime, TFM, deployment location and verification status**. Label assumed values. Revit 2025.5/2026.5 use .NET 10; earlier updates use .NET 8. Select references by API build, not TFM; verify each supported host/API combination.

## Keep the API boundary small

Read [execution and performance](references/execution.md) for any model access, modeless UI, asynchronous work or transaction change.

- **Read-only:** query → detached result → presentation. Filter in valid API context; extract only values the result needs.
- **Modification:** snapshot → pure computation → revalidate → apply. Include document/element identity and original values for later resolution or modification. Re-enter valid API context, verify current state, then apply changed values in bounded transactions.

Business logic belongs in independent classes/DLLs with no Revit references or live API objects (`Document`, `Element`, `Parameter`, `XYZ`, collectors/lazy projections). Pass detached values; bounded CPU parallelism belongs here.

Main-thread execution alone is insufficient: WPF Dispatcher callbacks and continuations after `await` do not establish Revit API context. Modeless requests use `ExternalEvent`; raising it is a dispatch request, not immediate execution. API reads are not safe in `Task.Run`, actors, timers or `Parallel.ForEach`. Do not keep a transaction or group open across `await` or callbacks.

## Select dependencies deliberately

Read [packages and testing](references/ecosystem.md) before adding a wrapper, API package or test harness. Pin exact package versions per host; inspect their assets and transitive dependencies. Revit supplies its API DLLs; do not ship private copies. No trimmed/Native AOT/self-contained publishing for the in-process add-in. Separate companion executables have their own deployment choices.

## Required output when implementing

- Target record, thin host adapter and pure business-logic tests.
- For writes/deferred work: stale-input, transaction/undo and cancellation policies.
- For performance claims: measurements on representative models.
- Per target, report compilation, tests, host loading, UI execution and deployment separately as **passed, failed or unverified**. Deployment succeeds only after every required copy succeeds.

Use the exact release SDK/reference for member availability and The Building Coder for experience and rationale. Historical samples and dated source links require rechecking before claiming support for later releases.
