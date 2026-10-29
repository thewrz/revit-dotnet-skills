# Revit versions, builds and API drift

Verified 2026-10-29. Recheck Autodesk release notes before extending this table.

| Revit installation | Host runtime | Target for new matching builds |
|---|---|---|
| 2024 | .NET Framework 4.8 | `net48` |
| 2025 before 2025.5 | .NET 8 | `net8.0-windows` |
| 2026 before 2026.5 | .NET 8 | `net8.0-windows` |
| 2025.5 / 2026.5 and subsequent updates in those lines | .NET 10 | `net10.0-windows` |
| 2027 | .NET 10 | `net10.0-windows` |

For older years, retrieve that year's SDK requirements; do not extrapolate `net48` indefinitely. Autodesk's [current transition requirements](https://help.autodesk.com/view/RVT/2025/ENU/?caas=caas/sfdcarticles/sfdcarticles/Revit--Requirements-for-products-affected-by-the-Microsoft--NET-10-transition.html), [2026.5 release notes](https://help.autodesk.com/view/RVT/2026/ENU/?guid=RevitReleaseNotes_2026updates_2026_5_html), and [2027 migration](https://help.autodesk.com/cloudhelp/2027/ENU/Revit-WhatsNew/files/GUID-8D7A4715-EAF8-4BD1-BE78-061F900D0BCE.htm) establish the runtime transitions.

**Compatibility nuance:** Autodesk [says the 2025/2026 runtime update itself does not change the API](https://blog.autodesk.io/autodesk-desktop-products-2025-2026-net-10-updates/). Existing .NET 8 add-ins may continue working on those .NET 10 hosts; retargeting is needed when affected by runtime/dependency changes. Do not claim every existing add-in must be rebuilt. Prove any retained .NET 8 binary on both host runtime variants. A new .NET 10 binary cannot run on the earlier .NET 8 installation. Review Microsoft's [.NET 9](https://learn.microsoft.com/en-us/dotnet/core/compatibility/9.0) and [.NET 10](https://learn.microsoft.com/en-us/dotnet/core/compatibility/10.0) changes, including native dependencies and serialization.

## Build contract

- Distinguish SDK/compiler, language, TFM, API and host versions. Inspect assembly identity and framework references without loading Revit's native dependencies; a folder named `2026` cannot distinguish .NET 8 from 10. Check DB/UI assemblies individually and disclose mixed builds. A newer compiler does not add BCL APIs to `net48`.
- On Linux/macOS, set [`EnableWindowsTargeting=true`](https://learn.microsoft.com/en-us/dotnet/core/tools/sdk-errors/netsdk1100) for Windows/WPF builds; restore matching Windows Desktop and .NET Framework reference assemblies. This enables compilation, not Revit/WPF execution. Keep portable tests runnable on the available runtime.
- Separate year-specific adapters or explicit `RevitYear` + runtime configurations are valid. Use unique intermediate/output paths per combination; TFMs alone cannot distinguish same-runtime years. When customizing paths, exclude every target's generated files from source discovery, including WPF temporary projects ([MSBuild exclusions](https://learn.microsoft.com/en-us/dotnet/core/project-sdk/msbuild-props#defaultitemexcludes)). Verify target A → B → A in one checkout without cleaning.
- Pin API references to the actual minimum supported release/update. Use conditional package references or per-adapter project references; inspect restored assets. Build against the minimum API surface, then test later supported updates.
- Shared pure logic can target `netstandard2.0` when its APIs/packages fit; .NET Framework cannot consume `netstandard2.1`. Alternatively multi-target `net48;net8.0;net10.0`. Keep Windows UI and Autodesk types out of the portable contract. See [Microsoft framework compatibility](https://learn.microsoft.com/en-us/dotnet/standard/net-standard).
- For `net48`, verify modern syntax support separately from runtime features (`IsExternalInit`/required-member attributes, default interface implementations, `TimeProvider`, `ThrowIfNull`, `Parallel.ForEachAsync`). Prefer compatible implementations; do not install compatibility packages indiscriminately.

## API migration checklist

| API seam | Guidance |
|---|---|
| Element IDs | 2024 introduces 64-bit `ElementId.Value`; `IntegerValue` can throw for large IDs and is removed in [2026](https://help.autodesk.com/cloudhelp/2026/ENU/Revit-API-MainReference/files/html/44f3f7b1-3229-3404-93c9-dc5e70337dd6.htm). Use `Value`/`long` throughout 2024+ adapters, DTOs and serialization; test above Int32.MaxValue. Built-in category/parameter enums also widened. |
| Units/specs, 2021 onward | Migrate legacy `DisplayUnitType`/`UnitType` overloads to the release's `ForgeTypeId`, `UnitTypeId`, `SpecTypeId` and `UnitUtils` APIs. Do not confuse spec IDs with unit IDs or parameter IDs. |
| Parameters | Resolve by built-in identifier or shared-parameter GUID where available, rather than localized display name. Check storage type, read-only status and unit semantics before setting. |
| 2025 removals | [FamilyManager.AddParameter/ReplaceParameter overloads taking BuiltInParameterGroup were removed](https://blog.autodesk.io/whats-new-in-the-revit-2025-api/); use the release's ForgeTypeId overloads. |
| 2026 electrical deprecations | ElectricalSystem.[WireSizeString](https://help.autodesk.com/cloudhelp/2026/ENU/Revit-API-MainReference/files/html/51fad9c3-b6a4-a8b3-95b2-beafff72f994.htm) → CableSize; [WireType](https://help.autodesk.com/cloudhelp/2026/ENU/Revit-API-MainReference/files/html/d605965d-bbed-c3c9-14fa-2d040ec76dca.htm) → CableType. [VoltageDrop](https://help.autodesk.com/cloudhelp/2026/ENU/Revit-API-MainReference/files/html/2f7d179a-a6c3-375b-d184-cc796e918f5d.htm) has no replacement; do not invent one. |
| Year-specific methods/commands | Read that release's SDK API changes and obsolete-member replacement messages. Keep conditional compilation in adapters. Do not replace members based solely on the .NET version. |
| 2027 | Review removal/deprecation of FormIt AXM import, legacy rebar APIs, Mechanical.Zone and EnergyDataSettings members against the exact SDK. Do not copy old signatures as current examples. |

Sources: [Autodesk 2024 API changes](https://blog.autodesk.io/whats-new-in-the-revit-2024-api/), [2021 API changes](https://blog.autodesk.io/whats-new-in-the-revit-2021-api/), [2027 SDK changes](https://blog.autodesk.io/revit-2027-sdk-net-10-api-changes-and-additions/), [SDK downloads](https://aps.autodesk.com/developer/overview/revit-api). This is a migration checklist, not an exhaustive member-removal catalog. Compile each adapter with obsolete diagnostics visible; document a narrowly scoped exception only for a genuinely required older target.

## Packaging and loading

Revit supplies `RevitAPI.dll` and public `RevitAPIUI.dll` (not internal `RevitUIAPI.dll`). Set `<Private>false</Private>` on assembly references. `PrivateAssets="all"` controls transitive NuGet propagation, not DLL copying; inspect staged output.

For reference-only NuGet packages, use `ExcludeAssets="runtime"` together with `PrivateAssets="all"` on each API `PackageReference`, and verify the package's build targets do not copy the files separately. Add a deployment check that rejects staged `RevitAPI*.dll`; compile success alone does not verify packaging.

Deploy separate outputs/manifests per year/update contract. [2026 already supports opt-in load-context isolation](https://help.autodesk.com/cloudhelp/2026/ENU/Revit-API/files/Revit_API_Developers_Guide/Introduction/Add_In_Integration/Revit_API_Revit_API_Developers_Guide_Introduction_Add_In_Integration_Add_in_Dependency_Isolation_html.html) through `UseRevitContext=false`; defaults matter. [2027 changes machine-wide discovery to Program Files](https://blog.autodesk.io/revit-2027-sdk-net-10-api-changes-and-additions/); do not backport its path. Isolation does not grant API thread safety.

Do not publish the add-in as a self-contained app, trimmed assembly or Native AOT library. The host must discover and load managed entry points. Microsoft's [Native AOT limitations](https://learn.microsoft.com/en-us/dotnet/core/deploying/native-aot/) are relevant to separate executables, not a replacement Revit loading contract.
