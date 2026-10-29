# Multi-version benchmark outcome

2026-10-29; final skill revision `ddd0352`; five fresh native Codex `gpt-6-luna` runs at medium effort. Each used the same outcome prompt, empty workspace and locally installed plugin, without prior conversation or evaluator hints.

The Revit entry point is **424 words**, versus 433 before this experiment. It keeps general host/core boundaries and compiler-driven correction. Benchmark-specific arithmetic advice was removed after user steering.

| Measured outcome | Final sample |
|---|---|
| Both targets compile; repeated 2024 → 2026 → 2024 without cleaning | 5/5 |
| Windows targeting enabled; correct final net48/net10 target pair | 5/5 |
| One model query; no transactions, regeneration or worker API access | 5/5 |
| Business logic independent of Revit/UI types | 2/5 |
| Independent behavior checks pass | 1/5 overall; 1/2 independently testable outputs |
| Agent authored executable pure tests | 0/5 |

The successful sample (`repeat2`) kept business logic in a plain C# class within the add-in project. Its unchanged source compiled without Revit/WPF and passed six evaluator-owned checks. Another sample generated a separate Core DLL but failed two numerical checks. Three retained calculations in a window, command or Document-dependent utility. No generated source was repaired for scoring.

All five read the relevant Revit, version, execution, project-structure and C# skill files. Compiler correction was consistent; architectural compliance was not. These small samples do not establish a reliability improvement or justify adding task-specific rules to the skill. The initial passing-streak plan was replaced with a fixed sample after user steering; every failure is retained.

The supplied 2026 DB reference is 26.5 and requires .NET 10. Missing public UI references were supplemented in a read-only overlay with Nice3point 2024.3.60 and 2026.4.10; the latter is an earlier same-year build. Compilation produced zero errors, with one or two reference-conflict warnings for 2026. Licensed-host loading, UI and deployment remain unverified.

Full outputs, hashes, exact commands, checks, earlier exploratory trials and input provenance: [/home/adam/github/revit-dotnet-skills-reviews/2026-10-29-iterations/RESULTS.md](/home/adam/github/revit-dotnet-skills-reviews/2026-10-29-iterations/RESULTS.md).
