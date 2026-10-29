# Revit NuGet ecosystem and tests

Research snapshot: 2026-10-28. These are candidates, not a mandatory dependency stack. Inspect the chosen package version's TFMs, API year/update, license, dependencies and release notes. A NuGet compatible-framework badge does not prove that Revit can load an add-in.

| Project / package family | Useful role | Adoption boundary |
|---|---|---|
| [Nice3point Revit API packages](https://github.com/Nice3point/revit-api) (`Nice3point.Revit.Api.RevitAPI`, `Nice3point.Revit.Api.RevitAPIUI`) | Build-time references for specific Revit releases | Pin exact versions per adapter; do not infer the year from the TFM or deploy Revit DLLs. Wrapper repository licensing does not relicense Autodesk binaries. Inspect package license and Autodesk terms. |
| [Nice3point.Revit.Toolkit](https://github.com/Nice3point/RevitToolkit) | Command/application conveniences and ExternalEvent helpers | MIT helper code; verify selected release supports the intended runtime/API. Context helpers do not permit worker-thread API calls. |
| [Nice3point Revit templates](https://github.com/Nice3point/RevitTemplates) | Starting build/configuration conventions | Read generated targets/deployment side effects. Adapt year/update matrix rather than accepting template defaults blindly. |
| [Revit.Async](https://github.com/KennanChan/Revit.Async) | Awaitable ExternalEvent request/response | MIT; Task-based dispatch, not multithreaded API execution. Inspect current package's initialization, exception, queue and cancellation behavior; implement missing lifecycle policies explicitly. |
| [ricaun.RevitTest](https://github.com/ricaun-io/RevitTest) | NUnit-based tests executed inside installed Revit | MIT harness; requires configured Revit installation/session/licensing. Version-specific integration checks, not a replacement for ordinary unit tests. |
| [RevitLookup](https://github.com/lookup-foundation/RevitLookup) | Interactive investigation of actual elements and API values | MIT tool; use a compatible release during diagnosis, not as a production business-logic dependency. |
| [Dynamo RevitTestFramework](https://github.com/DynamoDS/RevitTestFramework) | Historical journal-driven Revit testing ecosystem | Distinct from ricaun.RevitTest. Verify current maintenance, license and supported hosts before adopting. |

Do not add Toolkit and Revit.Async together by default; choose a dispatch abstraction from project needs and supported versions. No helper bypasses Autodesk's API context rules. If a package lacks the needed update/runtime assets, reference the installed SDK assemblies explicitly instead of selecting an unrelated newest package.

## Dependency review

1. Verify package identity against publisher repository and NuGet metadata; pin exact versions/lock restore.
2. Inspect transitive dependencies, native assets, WPF support and assemblies already loaded by Revit. Keep host-provided API references out of deployment.
3. Run the installed SDK's NuGet vulnerability audit for each target (use its documented CLI syntax), and inspect package licenses. Do not equate a clean audit with host compatibility.
4. Test installation and assembly loading on each supported host/update combination, including other required add-ins. Do not change Revit's process-wide binding/runtime configuration to hide a conflict.

Microsoft sources: [Central Package Management](https://learn.microsoft.com/en-us/nuget/consume-packages/central-package-management), [NuGet auditing](https://learn.microsoft.com/en-us/nuget/concepts/auditing-packages), [package compatibility](https://learn.microsoft.com/en-us/dotnet/standard/library-guidance/nuget-package-compatibility-rules).

## Verification layers

- **Pure tests:** calculations, units at contract boundaries, tolerances, validation, unchanged-value elimination, idempotent plans and cancellation on detached DTOs. Run without loading Revit.
- **Build matrix:** each supported API/runtime configuration, including both sides of supported runtime transitions. Switch targets without cleaning; inspect obsolete diagnostics and staged files.
- **Host tests:** command registration and UI behavior; for implemented writes/modeless work, test commit/rollback, failure handling, document switch/close, stale snapshots, worksharing, cancellation and undo.
- **Performance:** small and large representative models, with separate extraction/compute/apply timings and transaction counts. Test partial completion honestly; no brittle universal millisecond threshold.

A CI restore/build on Linux validates neither Revit loading nor transactions. Host integration needs Windows and a properly licensed supported Revit environment. Testcontainers is useful for separate data services, not a containerized substitute for the Revit UI host.
