---
name: revit-development
description: Use when planning, implementing or reviewing Revit C# add-ins, including API/runtime compatibility, installation, modeless UI, performance and hot-reload workflows.
---

# Revit C# development

Revit owns the runtime, API context and model. Preserve upstream practices within those boundaries.

For project/build changes, load [project-structure](../project-structure/SKILL.md); for C#, load [csharp-coding-standards](../csharp-coding-standards/SKILL.md). Apply Revit host constraints.

Keep business logic independent of the host:

```text
Core           plain .NET types and logic; no Autodesk/WPF references
RevitAdapter   → Core; API access, commands and presentation
```

Commands and UI delegate business decisions to Core. Test production logic without Revit/UI; a separate project or shared source can enforce this boundary without requiring another deployed DLL.

## Establish the target before coding

Read [versions and API migration](references/versions.md). Record **year/update, minimum supported update, API reference builds, runtime, TFM and deployment location**; label assumptions and check supplied references. Verify each supported host/API combination.

## Keep the API boundary small

Read [execution and performance](references/execution.md) for any model access, modeless UI, asynchronous work or transaction change.

- **Read-only:** query → detached snapshot → pure calculation → presentation. Filter in valid API context; extract only needed values.
- **Modification:** snapshot → pure computation → revalidate → apply. Preserve document/element identity and every input behind the proposal. Re-enter valid API context, recheck its preconditions, then apply changed values in bounded transactions.

Domain contracts contain detached values, never `Document`, `Element`, `Parameter`, `XYZ` or lazy API projections. Bounded CPU parallelism belongs in the domain.

Modeless callbacks enqueue detached intent through `ExternalEvent`. Resolve and validate Revit objects inside API callbacks; WPF dispatch, workers and `await` continuations supply no API context. Keep transactions/groups within one callback.

For debugging or implementing hot-reload capability, read [live development](references/live-development.md), including its implementation and verification requirements.

## Select dependencies deliberately

Read [packages and testing](references/ecosystem.md) before adding dependencies. Minimize and justify runtime dependencies without imposing a DLL count. For manifests, bundles or distribution, read [packaging and loading](references/packaging.md). Exclude verified host-provided and build-only assets; retain required runtime dependencies. No trimmed/Native AOT/self-contained publishing for the in-process add-in.

## Required output when implementing

- Target record, declared command transaction modes and verified independent business logic.
- For writes/deferred work: stale-input, transaction/undo and cancellation policies.
- For performance claims: measurements on representative models.
- Build every requested target. Use compiler diagnostics to correct code, references and target settings, then rebuild. Report compilation, tests, host/UI execution and deployment separately as **passed, failed or unverified**. Deployment succeeds only after every required copy succeeds.

Use the exact release SDK/reference for member availability and The Building Coder for experience and rationale. Historical samples and dated source links require rechecking before claiming support for later releases.
