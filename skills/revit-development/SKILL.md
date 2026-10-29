---
name: revit-development
description: Use when developing, reviewing, testing, packaging, or migrating C# Revit add-ins, modeless tools, Revit API integrations, or multi-version Revit builds.
---

# Revit C# development

Revit owns the runtime, API context and model. Apply general .NET practices within those boundaries. Keep upstream institutional advice unless a factual error or host constraint makes it inapplicable.

## Establish the target before coding

Read [versions and API migration](references/versions.md). Record **Revit year AND update/build**, host runtime, target framework, exact API reference version, minimum supported update, and deployment location. Revit 2025.5 and 2026.5 use .NET 10; earlier updates use .NET 8. Never select an API reference from the TFM alone. Compile and test each supported host/API combination; do not assume one DLL works across years.

## Keep the API boundary small

Read [execution and performance](references/execution.md) for any model access, modeless UI, asynchronous work or transaction change.

1. **Snapshot:** in valid Revit API context, filter once and extract only needed values into detached DTOs, including document identity, element identity, units and relevant original values.
2. **Compute:** independent classes/DLLs operate on those DTOs. They reference neither RevitAPI nor RevitAPIUI and accept no `Document`, `Element`, `Parameter`, `XYZ`, collectors or lazy API-backed enumerables. CPU work may use bounded parallelism here.
3. **Apply:** re-enter a valid API callback, verify the intended document and current values, resolve elements afresh, then apply only changed values in bounded, deliberate transactions.

Main-thread execution alone is insufficient: WPF Dispatcher callbacks and continuations after `await` do not establish Revit API context. Modeless requests use `ExternalEvent`; raising it is a dispatch request, not immediate execution. API reads are not safe in `Task.Run`, actors, timers or `Parallel.ForEach`. Do not keep a transaction or group open across `await` or callbacks.

## Select dependencies deliberately

Read [packages and testing](references/ecosystem.md) before adding a wrapper, API package or test harness. Pin exact package versions per host; inspect their assets and transitive dependencies. Revit supplies its API DLLs; do not ship private copies. No trimmed/Native AOT/self-contained publishing for the in-process add-in. Separate companion executables have their own deployment choices.

## Required output when implementing

- Target matrix with evidence and minimum update requirements.
- Thin host adapter and pure computation boundary, including stale-input policy.
- Transaction/undo/cancellation behavior and representative-model performance measurements.
- Pure-logic tests plus per-host build/load/integration evidence. State unavailable host checks explicitly; structural validation is not a Revit execution test.

Historical blog samples are explanations, not current API contracts. Prefer the exact release SDK/reference for member availability; use The Building Coder for experience and rationale. The dated source links in the references are the research starting point, not permission to guess future releases.
