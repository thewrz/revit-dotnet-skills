# Revit packaging and loading

Research checked: 2026-10-29. Apply the [year/update contract](versions.md); a small, complete deployment matters more than DLL count.

## Code boundaries and runtime assets

Pure classes can share source with portable tests or live in a separate core project. Test the production logic and target-specific branches. Ordinary project/assembly references retain dependencies; they do not merge implementations. [Microsoft's library guidance](https://learn.microsoft.com/en-us/dotnet/standard/library-guidance/dependencies) supports reviewing unnecessary dependencies and using shared source for small internal components.

Inspect the resolved dependency graph and staged files. Include required managed/native dependencies and resources; exclude build-only tools and verified host/runtime-provided assets. A `Microsoft.*` name alone proves neither category. Remove unnecessary package references at their source, rather than deleting required DLLs from output.

Revit supplies `RevitAPI.dll` and public `RevitAPIUI.dll` (not internal `RevitUIAPI.dll`). Set `<Private>false</Private>` on assembly references. For reference-only API packages, use `ExcludeAssets="runtime"` with `PrivateAssets="all"`. [PrivateAssets controls propagation, not copying](https://learn.microsoft.com/en-us/nuget/consume-packages/package-references-in-project-files#controlling-dependency-assets); package build targets can copy files separately. Reject staged Revit API DLLs.

## Single-file choices

Keep the Revit entry assembly a managed class library. [`PublishSingleFile` requires an executable](https://learn.microsoft.com/en-us/dotnet/core/tools/sdk-errors/) (NETSDK1099); it does not merge add-in libraries. No self-contained runtime, trimming or Native AOT for the in-process entry assembly. Companion executables have separate deployment choices.

[ILRepack](https://github.com/gluck/il-repack) merges managed assemblies; [Costura](https://github.com/Fody/Costura) embeds dependencies and adds runtime resolution. Use either only for a justified deployment benefit. Validate the chosen transformation's initialization, resources, assembly identities and loading on every target; fewer files do not prove fewer dependencies.

## Registration and bundles

Two discovery chains:

```text
Yearly Addins folder → .addin → Assembly + FullClassName
ApplicationPlugins/App.bundle → PackageContents.xml → ModuleName (.addin) → Assembly + FullClassName
```

In [`.addin` XML](https://help.autodesk.com/cloudhelp/2026/ENU/Revit-API/files/Revit_API_Developers_Guide/Introduction/Add_In_Integration/Revit_API_Revit_API_Developers_Guide_Introduction_Add_In_Integration_Add_in_Registration_html.html), `RevitAddIns` contains `AddIn` entries. `Type="Application"` identifies an `IExternalApplication`; `Type="Command"` an `IExternalCommand`. Supply `Assembly`, `FullClassName`, a stable `AddInId` unique among registrations in that Revit session, and vendor identity; applications also need `Name`. Ribbon construction belongs in application code; `Text` describes externally registered command buttons. Use documented `AddInId` in new manifests; older `ClientId` also appears in Autodesk samples.

Use a resolved absolute `Assembly` path or a relative path verified from the installed manifest's location. [Tammik explains](https://blog.autodesk.io/addin-file-learning-python-and-ifcjs/) that manifest paths support relative navigation, not environment-variable expansion; expand installer variables before writing XML.

A `.bundle` suffix alone is just a folder name. For ApplicationPlugins discovery, put `PackageContents.xml` at the bundle root. Its Revit `ComponentEntry.ModuleName` points to a `.addin`, which selects the DLL/class. Autodesk's [bundle guide](https://damassets.autodesk.net/content/dam/autodesk/www/developer-network/app-store/revit/pdf/3%20Autodesk%20Exchange%20Publish%20Revit%20Apps%20-%20Preparing%20Apps%20for%20the%20Store_Guidelines.pdf) illustrates this layout. Give each year a separate `Components` element containing sibling `RuntimeRequirements` and `ComponentEntry` elements. [Autodesk's 2025 guidance](https://blog.autodesk.io/revit-api-understanding-the-role-of-seriesmin-and-seriesmax-in-plugin-deployment/) says Revit matches `SeriesMin` and ignores `SeriesMax`. Verify selection in each host; install one discovery route.

For 2024–2026, place yearly manifests directly in `%AppData%\Autodesk\Revit\Addins\<year>` or `%ProgramData%\Autodesk\Revit\Addins\<year>` ([registration paths](https://help.autodesk.com/cloudhelp/2025/ENU/Revit-API/files/Revit_API_Developers_Guide/Introduction/Getting_Started/Using_the_Autodesk_Revit_API/Revit_API_Revit_API_Developers_Guide_Introduction_Getting_Started_Using_the_Autodesk_Revit_API_Registration_of_add_ins_html.html)); bundles use the corresponding `Autodesk\ApplicationPlugins` roots. [2027 moves both machine-wide roots to Program Files](https://blog.autodesk.io/revit-2027-sdk-net-10-api-changes-and-additions/), retaining per-user discovery. Do not backport that change.

## Validate the installed package

[2026 opt-in isolation](https://help.autodesk.com/cloudhelp/2026/ENU/Revit-API/files/Revit_API_Developers_Guide/Introduction/Add_In_Integration/Revit_API_Revit_API_Developers_Guide_Introduction_Add_In_Integration_Add_in_Dependency_Isolation_html.html) uses `ManifestSettings/UseRevitContext=false` (default true). Dependencies must resolve in the chosen context; incidental copies loaded by other add-ins are insufficient. Isolation grants no API thread safety.

From clean staging, validate the installed discovery chain, XML structure, target selection, GUIDs, paths, command attributes and runtime assets. Test loading and UI on each supported Windows/Revit update using the installed files. Report builds, pure tests, staging checks and host execution separately; compiler success does not establish deployment success.
