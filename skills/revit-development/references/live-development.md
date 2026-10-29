# Live development and Hot Reload

Research checked: 2026-10-29. Use the [target record](versions.md): Revit update, runtime, compiler and debugger versions determine capability. Keep development hooks out of release deployment.

## Choose the mechanism

| Need | Starting point | Boundary |
|---|---|---|
| Edit running business/command methods | Visual Studio Hot Reload / Edit and Continue | Patches supported edits; existing state is retained. |
| Refresh existing UI or caches after an edit | Explicit refresh; optionally `MetadataUpdateHandler` | Requires re-execution and verified notification delivery. |
| Replace a rebuilt implementation and dependencies | Optional development loader | Separate lifecycle; unload and dependency identity must be proven. |

Start with a small debugger probe before adding infrastructure. Use a supported Debug configuration, matching loaded DLL/PDB/source, managed-only debugging and enabled Hot Reload. Check evaluated settings for custom configurations; a `Debug` prefix is not proof. Launching Revit under the debugger and attaching later are different scenarios. Follow [Microsoft's setup/support guidance](https://learn.microsoft.com/en-us/visualstudio/debugger/hot-reload) and inspect the Hot Reload output. `dotnet watch` does not automatically patch an arbitrary running Revit process.

[The Building Coder](https://jeremytammik.github.io/tbc/a/1920_apply_code_changes.html) reports successful C# edits; its [2024 follow-up](https://blog.autodesk.io/net-core-c4r-views-and-interactive-hot-reload/) highlights interactive Revit/Dynamo demonstrations. These establish useful techniques, not support for every host/update or XAML workflow.

## Make changed behavior reachable

Put evolving behavior in methods invoked by commands or refresh actions. Applying an edit does not rerun startup, constructors or completed work. Reopen a dialog or invoke a repeatable presentation method; preserve user input and detach replaced subscriptions. Keep ribbon/bootstrap registration once per host lifetime.

Let compiler/debugger diagnostics determine supported edits. Check [Roslyn's edit matrix](https://github.com/dotnet/roslyn/blob/main/docs/wiki/EnC-Supported-Edits.md) for the toolchain; do not freeze an old rule that all type/signature edits require restart. .NET Framework has a smaller edit set; modern collectible `AssemblyLoadContext` is unavailable on `net48`.

On supporting modern targets, an assembly-level [MetadataUpdateHandler](https://learn.microsoft.com/en-us/dotnet/api/system.reflection.metadata.metadataupdatehandlerattribute?view=net-10.0) identifies static `ClearCache(Type[]? updatedTypes)` and/or `UpdateApplication(Type[]? updatedTypes)` methods. All cache callbacks precede application callbacks; `null` types means any type may have changed. Verify these callbacks independently: [Microsoft's native-host investigation](https://github.com/dotnet/runtime/issues/113452) demonstrates applied edits without notifications. The attribute alone does not enable Hot Reload.

Callbacks do not establish Revit API context. Dispatch presentation to WPF; queue model work through the existing `ExternalEvent` boundary with cancellation/stale-input handling. Never automatically replay model writes after a code edit.

## If a custom replacement loader is justified

Keep the host/contract stable; share the actual host API assemblies. Stage each payload with its private dependencies, symbols and dependency metadata. Exercise the same business implementation as production. Dependency isolation is not unloadability.

[Unloading is cooperative](https://learn.microsoft.com/en-us/dotnet/standard/assembly/unloadability). Quiesce work and release subscriptions, UI callbacks, tasks and retained objects before checking a weak context reference from outside payload frames. Retained exceptions/types can also root a generation: preserve failure diagnostics as detached host-owned data before probing. Distinguish a recoverable busy/rejected attempt from a failed shutdown or proven unreleased context; a busy window alone should not poison later retries. Bound dispatch waits and complete failed requests; see [execution](execution.md).

## Deliver and verify the loop

For a hot-reload request, configure the chosen development workflow and implement its required refresh/cleanup path. Deliver exact edit → apply → invoke steps and a restart fallback for unsupported edits. Reuse established tooling; introduce a custom loader only for a demonstrated gap.

Verify changed behavior in Revit: Core edits, repeated updates, UI refresh, failure recovery and clean shutdown. For replacement, record artifact identity and collection; for Hot Reload, record applied-edit diagnostics and observed behavior—disk hashes alone do not prove an in-memory patch. Finish with a cold-start production-path check. Report builds, standalone tests and host execution separately; label host checks unverified when Revit is unavailable.
