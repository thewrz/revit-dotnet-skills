# Live development and Hot Reload

Research checked: 2026-10-29. Use the [target record](versions.md): Revit update, runtime, compiler and debugger versions determine capability. Keep development hooks out of release deployment.

## Choose the mechanism

| Need | Starting point | Boundary |
|---|---|---|
| Edit running business/command methods | Visual Studio Hot Reload / Edit and Continue | Patches supported edits; existing state is retained. |
| Refresh existing UI or caches after an edit | Explicit refresh; optionally `MetadataUpdateHandler` | Requires re-execution and verified notification delivery. |
| Terminal build and reload without a debugger | Development assembly replacement | Stage a complete generation; verify activation and collection. |

For debugger edits, provide a Debug launch configuration, matching loaded DLL/PDB/source, managed-only debugging and enabled Hot Reload. Check evaluated settings and [Microsoft's support guidance](https://learn.microsoft.com/en-us/visualstudio/debugger/hot-reload). For Attach to Process, set `COMPLUS_ForceENC=1` before launching Revit and verify the [toolchain prerequisites](https://learn.microsoft.com/en-us/visualstudio/debugger/supported-code-changes-csharp#unsupported-scenarios). For terminal builds, implement activation of staged output; `dotnet build`/`watch` alone does not patch an arbitrary running Revit process.

[The Building Coder's C# experiment](https://jeremytammik.github.io/tbc/a/1920_apply_code_changes.html) and [Revit/Dynamo demonstrations](https://blog.autodesk.io/net-core-c4r-views-and-interactive-hot-reload/) motivate small capability probes. Verify the actual host/update and XAML workflow separately.

## Make changed behavior reachable

Put evolving behavior in methods invoked by commands or refresh actions. Applying an edit does not rerun startup, constructors or completed work. Reopen a dialog or invoke a repeatable presentation method; preserve user input and detach replaced subscriptions. Keep ribbon/bootstrap registration once per host lifetime.

Let compiler/debugger diagnostics determine supported edits. Check [Roslyn's edit matrix](https://github.com/dotnet/roslyn/blob/main/docs/wiki/EnC-Supported-Edits.md) for the toolchain; do not freeze an old rule that all type/signature edits require restart. .NET Framework has a smaller edit set; modern collectible `AssemblyLoadContext` is unavailable on `net48`.

On supporting modern targets, an assembly-level [MetadataUpdateHandler](https://learn.microsoft.com/en-us/dotnet/api/system.reflection.metadata.metadataupdatehandlerattribute?view=net-10.0) identifies static `ClearCache(Type[]? updatedTypes)` and/or `UpdateApplication(Type[]? updatedTypes)` methods. All cache callbacks precede application callbacks; `null` types means any type may have changed. Verify these callbacks independently: [Microsoft's native-host investigation](https://github.com/dotnet/runtime/issues/113452) demonstrates applied edits without notifications. The attribute alone does not enable Hot Reload.

Callbacks do not establish Revit API context. Dispatch presentation to WPF; queue model work through the existing `ExternalEvent` boundary with cancellation/stale-input handling. Never automatically replay model writes after a code edit.

## If a custom replacement loader is justified

Keep the host/contract stable; share the actual host API assemblies. Stage each payload with its private dependencies, symbols and dependency metadata. Exercise the production business implementation against current detached state before activation; retain the working generation if activation fails. Dependency isolation is not unloadability.

[Unloading is cooperative](https://learn.microsoft.com/en-us/dotnet/standard/assembly/unloadability). Quiesce work and release subscriptions, UI callbacks, tasks and retained objects before checking a weak context reference outside payload frames. Retained exceptions/types also root generations: detach failure diagnostics before probing. Separate recoverable busy/rejected attempts from failed shutdown/unload. Expire unstarted requests; report already-started work accurately. Bound waits and expose a definitive result through [the dispatch contract](execution.md).

## Deliver and verify the loop

Exercise the documented commands from clean outputs: terminal build → stage → activate, or debugger launch → edit/apply → refresh. Verify the running generation uses the newly built production implementation. Reuse established tooling; state restart boundaries.

For replacement, run portable lifecycle tests against the production loader and payload: changed behavior, collection and failure recovery. In Revit, verify repeated edits, UI refresh, shutdown and a cold production start. For debugger Hot Reload, record applied-edit diagnostics and changed behavior; disk hashes prove only disk changes. Report builds, standalone tests and host execution separately; label unavailable host checks unverified.
