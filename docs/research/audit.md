# Revit .NET skills audit

Research date: 2026-10-28. Upstream: Aaronontheweb/dotnet-skills at `5ca5db8cf25566f19d2a5dc53204d4af22b23a0d` (MIT). The fork retains all 39 upstream skills and six agents and adds `revit-development`.

## Assessment

The package offers substantial institutional knowledge in composition, concurrency, API contracts, testing, and distributed systems. It is useful as a reference library, not an automatically safe Revit architecture. Generic server/actor concurrency, modern-only BCL APIs, publishing, dependency injection lifetimes and benchmark advice need host-specific scope. Its structural validators do not compile its examples or check semantic truth. Some examples and links are stale; strong preferences must be distinguished from platform guarantees.

The Revit overlay implements snapshot → pure compute → revalidate/apply, with explicit API context, transaction lifetime and release/update selection. Research found that the simple 2024/net48, 2025–26/net8, 2027/net10 mapping is incomplete: 2025.5 and 2026.5 also run .NET 10. Existing .NET 8 add-ins are not automatically invalid on those updates; test dependency/runtime compatibility before requiring a rebuild.

## Evidence and limitations

All inherited skill directories and their supporting Markdown references were assigned to source review. Microsoft Learn is the authority for Microsoft product/API behavior; Autodesk for Revit host contracts; package maintainers for third-party libraries. Opinions such as explicit mapping, composition, CQRS, actor patterns and value-object preferences are preserved even when they differ from Microsoft recommendations.

Source review is not execution certification. The detailed audit records version-sensitive/unverified third-party, distro and performance claims explicitly. No claim is made that every illustrative snippet compiles, every external link is permanent, or every package works in every Revit build. Revit host tests require licensed Windows installations and have not been executed in this Linux workspace.

The skill references provide the primary Microsoft, Autodesk, The Building Coder and package sources. The detailed inherited audit and behavior evidence are maintained alongside this summary as the audit is integrated.

## Deliverables

- [All 39 inherited skills and six agents: source ledger](skill-inventory.md)
- [Baseline and five behavior scenarios](behavior.md)
- [Revit runtime/API matrix](../../skills/revit-development/references/versions.md)
- [Execution and performance boundaries](../../skills/revit-development/references/execution.md)
- [NuGet ecosystem and host test strategy](../../skills/revit-development/references/ecosystem.md)

The second regression run extracts actual Markdown C# examples: upstream fails with three CS0111 duplicate-constructor errors and a CS8602 nullable-flow error. Corrected examples compile under .NET 8 with warnings treated as errors. Package identity/registration and these two compiler checks make five automated tests; they do not validate all illustrative snippets.

## Additional TBC and NuGet findings

Tammik's [quick/slow/LINQ comparison](https://jeremytammik.github.io/tbc/a/1382_filter_shortcuts.html) and [profiling discussion](https://jeremytammik.github.io/tbc/a/0332_performance_profiling.htm) reinforce reducing native element expansion before managed filtering and measuring actual costs. These historical explanations inform the architecture; their timing numbers and API samples are not current compatibility guarantees. Use the [original-author archive](https://jeremytammik.github.io/tbc/a/index.html) rather than relying on retired Typepad links.

The [NuGet API package listing](https://www.nuget.org/packages/Nice3point.Revit.Api.RevitAPI) currently includes 2027.3.0 and older-year package lines; its publisher advertises .NET 10 for the newest version. This is concrete evidence against blindly selecting “latest” for all years. [ricaun.RevitTest.TestAdapter](https://www.nuget.org/packages/ricaun.RevitTest.TestAdapter) is a separate testing package, not the API runtime. Package catalog data is dated evidence, not a recommended floating dependency.
