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
