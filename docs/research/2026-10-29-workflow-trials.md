# Blind Revit workflow trials

## Method and scope

Fresh native Codex sessions used `gpt-6-luna` at medium effort, the installed 40-skill plugin, a frozen outcome prompt, public API references and an empty workspace. They received no conversation history, earlier implementations or grading criteria. Each generation had a 1,200-second ceiling. Evaluators preserved generated source and exercised production code or exact extracted loader bodies; test adapters were identified separately from host execution.

Baseline and candidates 1–3 each have five samples for modeless editing, multi-runtime packaging and live development. Candidate 4 changes only the live-development reference and has five additional live samples. Eight counter/migration holdouts and four paired inherited-guidance checks bring the total to **77 evaluable generations**. These small cohorts show observed outcomes, not a reliability guarantee or a statistically established causal effect.

Reference pairs cover Revit 2024.3.60, 2025.4.60 and 2027.3.0, using SDK 10.0.111. The counter holdout deliberately retains a mixed 2026 API/UI pair and requires disclosure. Compilation, portable execution, filesystem installation simulation and source review are distinct evidence classes. **Windows/Revit and Visual Studio execution remain unverified throughout.**

Three initial CLI parser failures never reached the model. A later temporary-storage failure truncated one live transcript; that attempt remains preserved as an infrastructure exception and was replaced with a fresh run using identical inputs. Interrupted evaluator checks were rerun after storage recovery. No generated source was repaired to improve a score. Manifest/hash checks verified model, effort, revision, prompts, references and source preservation; rebuilt binaries are distinguished from the original exported artifacts.

## Revisions and size

| Revision | Change | Revit entry / total words |
|---|---|---:|
| `76a500a` | Frozen baseline | 443 / 3,564 |
| `3814174` | Explicit command, callback, packaging and workflow contracts | 439 / 3,511 |
| `6a2da52` | Proposal inputs, resource ownership and current-state activation | 434 / 3,527 |
| `3337a26` | Proposal/request structure, binary-retention policy and attach prerequisite | 438 / 3,540 |
| `8523d97` | Explicit supported Visual Studio minimum for .NET 10 | 438 / 3,548 |

The inherited consistency corrections at `ca08312` precede the last two revisions. Modeless and packaging results below belong to `3337a26`; live results belong to `8523d97`. Unchanged scenarios were not represented as newly tested at the last revision.

## Observed outcomes

Each count is out of five runs for that scenario. Passes apply only to the named evidence boundary. Criteria are not combined into an overall score.

| Criterion | Baseline | Latest tested cohort |
|---|---|---|
| Modeless command metadata | 1 pass, 4 failures | 5 passes |
| Modeless API-context boundaries, source review | 4 passes, 1 failure | 5 passes |
| Modeless confirmed stale-model/value failures | 2 failures | 0 failures; all 5 retain proposal-field/UI ambiguities |
| Modeless request/lifetime outcomes | 2 failures, 3 partial | 1 failure, 3 partial, 1 pass |
| Modeless mutation/Undo handling, source review | 3 passes, 2 partial | 4 passes, 1 unchanged-write failure |
| Packaging command metadata | 2 passes, 3 failures | 5 passes |
| Packaging bundle structure/year selection | 3 passes, 2 failures | 5 passes |
| Packaging advertised all-target output | 4 passes, 1 failure | 5 passes |
| Packaging relocated per-user manifest paths | 5 passes | 4 passes, 1 failure |
| Live command metadata/API boundary | 3 passes, 2 gaps | 5 passes |
| Debugger setup completeness, source review | 1 pass, 1 partial, 3 gaps | 4 passes, 1 gap |
| Live current-selection activation recovery | 4 identified gaps | 2 identified gaps |
| Live cold-start/discovery path | 3 supported, 2 gaps | 3 supported, 2 gaps |
| Prior-generation collection observed portably | 3 observed, 2 unproven | 1 observed, 4 unproven |
| Live request/completion findings | 2 primary findings | 4 primary findings |

Portable modeless domain checks and individual packaging target builds passed across the compared cohorts. All five latest live loaders demonstrated changed business behavior portably. Improvement is **mixed**: metadata, bundle construction and debugger instructions improved; timeout handling, collection evidence and deployment remain inconsistent. Later samples still contain a stranded request, no-op write rollback, stale absolute manifest paths, malformed deployment XML or a missing production payload. Successful compilation and self-authored checks missed several of these defects.

## Holdouts and inherited guidance

The migration holdout improved from three of five gates to five of five. The final answer distinguishes validated retention of an existing .NET 8 binary from retargeting, adds the separate 2027 API target and uses the current machine-wide discovery location. This is advice review, not an executed migration.

The extended counter remains a failed regression check: three candidate samples use floating-point arithmetic that returns 56 instead of 55 for a 50-item group with 10% spares. The baseline calculates that boundary correctly. Several samples also leave aggregation coupled to the command. These findings concern the expanded calculation task; they do not invalidate the separately user-tested simple counter. The skill retains generic domain separation and testing guidance rather than adding a counting-specific recipe.

The [independent inherited-guidance audit](2026-10-29-inherited-guidance-audit.md) covered 95 files and led to five narrow corrections. Both package-update and bare-provider startup checks pass before and after those corrections: preserved behavior, not measured improvement. CPM, shared versions, explicit configuration and other intentional institutional practices remain intact.

## Sources and review adjudication

- [Autodesk command attributes](https://help.autodesk.com/cloudhelp/2026/ENU/Revit-API/files/Revit_API_Developers_Guide/Introduction/Add_In_Integration/Revit_API_Revit_API_Developers_Guide_Introduction_Add_In_Integration_Attributes_html.html) require a transaction mode. A UI-opening command may validly use ReadOnly; Manual is not universal.
- [External Events](https://help.autodesk.com/cloudhelp/2026/ENU/Revit-API/files/Revit_API_Developers_Guide/Advanced_Topics/Revit_API_Revit_API_Developers_Guide_Advanced_Topics_External_Events_html.html) motivate callback-owned model access. Proposal-state, cancellation and completion policies are this fork's engineering guidance.
- [Revit bundle selection](https://blog.autodesk.io/revit-api-understanding-the-role-of-seriesmin-and-seriesmax-in-plugin-deployment/) uses exact `SeriesMin` and ignores `SeriesMax`. Missing `SeriesMax` was not treated as a desktop Revit failure. [Relative manifest paths](https://blog.autodesk.io/addin-file-learning-python-and-ifcjs/) are valid when they resolve in the installed layout.
- [Microsoft debugger prerequisites](https://learn.microsoft.com/en-us/visualstudio/debugger/supported-code-changes-csharp#unsupported-scenarios), [IDE/SDK compatibility](https://learn.microsoft.com/en-us/dotnet/core/install/windows#net-versions-and-visual-studio) and [cooperative unloading](https://learn.microsoft.com/en-us/dotnet/standard/assembly/unloadability) support checking setup and actual lifecycle behavior separately.
- [Autodesk's runtime transition](https://blog.autodesk.io/autodesk-desktop-products-2025-2026-net-10-updates/) and [2027 SDK guidance](https://blog.autodesk.io/revit-2027-sdk-net-10-api-changes-and-additions/) support update-aware compatibility and deployment decisions.

Reviewers' unsupported wrapper-identity assumptions, universal Pending-finalizer demands and an incorrectly invoked PowerShell array argument were rejected or qualified. Applying the visible preview was distinguished from writing an undisplayed stale proposal. Same-current-selection recovery was distinguished from guaranteeing every future input. Source references and exact invocation semantics were checked before accepting findings.

## Remaining host validation

Use disposable models to exercise document switching, queued cancellation, reopening and Undo; load relocated packages on each declared host/update; and perform repeated terminal replacements and Visual Studio edits with visible changed behavior, failure recovery and a clean production restart. Portable builds and loader probes cannot establish those Windows/Revit outcomes.
