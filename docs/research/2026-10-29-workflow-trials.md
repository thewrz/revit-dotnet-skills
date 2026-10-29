# Blind workflow trials

## Method

Baseline: `76a500a`. Model: `gpt-6-luna`, medium effort. Each fresh native Codex session receives the installed plugin catalog, an empty workspace, public API references and one frozen outcome prompt. Conversation history, previous outputs and grading criteria are withheld. Each scenario has five samples per revision and a 1,200-second generation ceiling; failures remain in the record.

The scenarios implement a modeless editing tool, a relocatable multi-runtime package, and terminal plus Visual Studio live development. Matching public API/UI reference pairs cover Revit 2024.3.60, 2025.4.60 and 2027.3.0. The original counter and same-year runtime migration are holdouts. Generation outputs are preserved unchanged; evaluators may compile unchanged production source into independent probes.

Linux builds, portable runtime tests, installed-tree checks and source inspection are separate evidence categories. Actual Windows/Revit and Visual Studio behavior remains unverified. A working portable replacement loader does not establish debugger Hot Reload. Initial CLI parser failures occurred before model execution and are excluded from generated-sample denominators.

## First candidate: explicit contracts, fewer words

Initial generated samples compiled and tested pure calculations while omitting required command attributes, accessing model state from modeless click handlers, or retaining previews across document/lifetime changes. Other samples emitted unsupported bundle XML structure or documented a debugger attach workflow without its startup prerequisites. These are reasons to test host integration contracts beyond successful compilation.

The candidate replaces existing prose with imperative guidance for command metadata, callback-owned validation, request outcomes, installed discovery and executable reload lifecycle checks. The Revit entry point decreases from 443 to 439 words; all Revit guidance decreases from 3,564 to 3,511 words. Its behavioral improvement is **not yet established**; the fixed sample comparison remains in progress.

## Evidence and adjudication

- [Autodesk command attributes](https://help.autodesk.com/cloudhelp/2026/ENU/Revit-API/files/Revit_API_Developers_Guide/Introduction/Add_In_Integration/Revit_API_Revit_API_Developers_Guide_Introduction_Add_In_Integration_Attributes_html.html) require a declared transaction mode. Choose the mode for the command's work; a UI-opening command need not be Manual solely because a later external event performs writes.
- [Autodesk External Events](https://help.autodesk.com/cloudhelp/2026/ENU/Revit-API/files/Revit_API_Developers_Guide/Advanced_Topics/Revit_API_Revit_API_Developers_Guide_Advanced_Topics_External_Events_html.html) establish deferred callback execution. Document/lifetime binding and request completion policies are engineering guidance inferred from that boundary.
- [Autodesk's bundle example](https://blog.autodesk.io/revit-api-understanding-the-role-of-seriesmin-and-seriesmax-in-plugin-deployment/) places per-year runtime requirements beside the component entry. [Tammik's manifest guidance](https://blog.autodesk.io/addin-file-learning-python-and-ifcjs/) confirms relative and colocated DLL paths: a reviewer recommendation to require absolute paths was rejected.
- [Microsoft's debugger prerequisites](https://learn.microsoft.com/en-us/visualstudio/debugger/supported-code-changes-csharp#unsupported-scenarios) distinguish attach from debugger launch. [Cooperative unload guidance](https://learn.microsoft.com/en-us/dotnet/standard/assembly/unloadability) motivates testing the actual loader, collection and recovery separately from business calculations.

Review findings about simultaneous installation of explicitly alternative routes and future unused dependencies are not treated as failures of the requested implementation. One evaluator used a different SDK environment; its build failure was reproduced and corrected with the frozen SDK, rather than changing generated code or suppressing the SDK check.

## Second candidate: validate state and delivered behavior

The first candidate's five modeless and five packaging samples all declare command transaction attributes; the corresponding baseline counts were one and two out of five. This is compiled-metadata evidence, not host execution. Other failures remain: an exact resource-reader probe misses an adjacent file when loaded by a separate host, one bundle shortens the release identifier, and a replacement loader publishes a candidate before testing the state currently displayed. The first candidate's live-development series is still in progress; its full comparison remains pending.

The second candidate clarifies proposal preconditions, resource ownership, full bundle series identifiers and activation against current state. It asks agents to exercise documented commands from clean outputs and to compare binary retention with retargeting when advising on runtime migration. These replace existing passages; there is no benchmark-specific application or rule in the skill. It requires the same fixed five-sample comparison before an improvement claim.

[Microsoft's application base-directory documentation](https://learn.microsoft.com/en-us/dotnet/api/system.appdomain.basedirectory) and [assembly-location contract](https://learn.microsoft.com/en-us/dotnet/api/system.reflection.assembly.location) support separating host and library resource paths; a loader must supply the resource root when an assembly has no file location. Current-state activation and rollback are engineering guidance derived from the requested recovery contract, rather than built-in guarantees of an assembly load context.

## Third candidate: explicit proposal and startup contracts

The second candidate's five packaging implementations pass the core portable artifact checks; one supplies malformed README command examples. Modeless callback-context checks improve to five of five, but stale-proposal checks are less consistent than the first candidate, and one implementation attempts unchanged writes. These results do not establish uniform improvement. The third candidate states the proposal's required data and the comparison performed at Apply, replaces generic completion language with request states, and names Microsoft's documented prelaunch attach setting. The compatibility table now distinguishes existing-binary retention directly from new matching targets.

The Revit entry point is 438 words and all Revit guidance is 3,540 words, both below baseline. Five fresh samples per core scenario and the frozen holdouts will assess this combined revision; prior failures remain in the comparison. The separate inherited-guidance corrections are documented in [the consistency audit](2026-10-29-inherited-guidance-audit.md).
