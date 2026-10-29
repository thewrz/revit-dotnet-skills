# Execution, transactions and performance

## Boundaries before optimization

Declare each external command's [transaction mode](https://help.autodesk.com/cloudhelp/2026/ENU/Revit-API/files/Revit_API_Developers_Guide/Introduction/Add_In_Integration/Revit_API_Revit_API_Developers_Guide_Introduction_Add_In_Integration_Attributes_html.html); it has no default. Use `IExternalCommand.Execute`, `IExternalEventHandler.Execute` or another supported callback for model access. Match writes to the callback's permissions: `DocumentChanged` is read-only. Keep `Transaction` objects non-nested.

The Building Coder's [thread-safety discussion](https://jeremytammik.github.io/tbc/a/1244_no_multithreading.htm) includes Autodesk API lead Arnošt Löbel's explanation: even reads may expand internal element state. Its addendum explicitly exempts `ExternalEvent.Raise`. Therefore copying a list of `Element` wrappers does not make parameter reads safe on workers. Copy numeric/string/domain values in the callback instead.

## Snapshot → compute → present/apply

Component responsibilities (not a required assembly layout):

| Component | Inputs/outputs | Dependencies |
|---|---|---|
| Domain | Immutable snapshots → summaries, reports or proposed changes | Plain .NET; no Autodesk/UI types |
| Revit adapter per API target | Model → snapshots; validated changes → model | Matching Revit API, Domain |
| UI/orchestration | User intent, progress, cancellation, results | Domain contracts and dispatch abstraction |

Test business behavior through detached inputs and outputs without loading Revit/WPF. Command handlers and windows coordinate this work; the independent domain owns its rules.

An interface hiding a `Document` behind a method called by background business logic is still an API call. Snapshot the needed data first. Convert `XYZ`, transforms, geometry and units to domain-owned values where needed; never enumerate a collector/lazy projection after leaving API context. Preserve `long` IDs with document identity; IDs alone are not globally unique, and saved/cross-session workflows need an appropriate persistent identity such as `UniqueId` resolved inside the adapter.

Before applying, re-evaluate every input and eligibility predicate behind the proposal, including document/element identity, original values, writability and worksharing permissions. Reject/recompute stale proposals. Bind previews, queued work and cancellation to their owning document/lifetime; invalidate them together. Snapshot chunks across callbacks are not atomic.

## Modeless and asynchronous work

Create the external event in valid API context. UI/background callbacks submit detached requests; handlers resolve documents and validate model state. Give every request a terminal outcome, including superseded, rejected or cancelled work. Handle `Raise` results with a bounded FIFO or latest-request policy; repeated raises can coalesce. Consume requests once and release subscriptions/handlers with their owner.

Keep each callback synchronous and bounded. A Task-based wrapper is a dispatcher, not an API worker thread. No `.Wait()`/`.Result` blocking on dispatch from Revit's thread; no `async void` API handler that loses its callback context. After asynchronous I/O or CPU computation, explicitly dispatch the apply phase again. WPF Dispatcher marshaling is only UI marshaling.

Check cancellation before dispatch and between batches. Cancellation cannot preempt arbitrary native API work. Stop scheduling, roll back the active uncommitted batch where appropriate, and report already committed batches accurately. Throttle progress; neither a progress event nor a timer may query the model outside context.

Sources: Autodesk [ExternalEvent.Raise](https://help.autodesk.com/cloudhelp/2026/ENU/Revit-API-MainReference/files/html/13bf4411-c400-dcd2-458c-7f09357d9ecb.htm); Tammik [API context and polling](https://jeremytammik.github.io/tbc/a/1383_external_event_10_year.html). Queue, stale-input and cancellation policies above are this fork's engineering guidance inferred from deferred execution, not built-in ExternalEvent guarantees.

## Transactions and regeneration

- Read-only extraction normally needs no transaction. Compute and remote I/O outside transactions.
- Apply changed values only, with as few transactions as undo, failure isolation and responsiveness permit. Avoid a transaction and `Regenerate()` per element. There is no universal batch size: measure representative projects, including workshared models.
- A `TransactionGroup` may group completed transactions into one undo item via `Assimilate`, but does not remove their commit/regeneration cost. Keep groups within a single valid callback. For work spanning callbacks, close all transactions/groups before yielding; explain partial completion/undo semantics instead of promising atomicity.
- Check [mutation results](https://help.autodesk.com/cloudhelp/2026/ENU/Revit-API-MainReference/files/html/956a1e23-cfe5-a60b-1ff9-0e8e33812774.htm) and `Start`/`Commit`/rollback status before reporting applied changes. Treat `Pending` as unresolved failure processing; wait for its final outcome before further writes. Preserve actionable failures and warnings rather than suppressing them to force success.
- Regenerate explicitly only when subsequent operations require updated derived state before commit. A regeneration failure requires aborting the operation/transaction; do not catch and keep reading or writing the damaged document state.

Sources: Autodesk [Transactions](https://help.autodesk.com/cloudhelp/2024/ENU/Revit-API/files/Revit_API_Developers_Guide/Basic_Interaction_with_Revit_Elements/Revit_API_Revit_API_Developers_Guide_Basic_Interaction_with_Revit_Elements_Transactions_html.html), [Regenerate](https://help.autodesk.com/cloudhelp/2026/ENU/Revit-API-MainReference/files/html/22468e2c-9772-8478-0816-c9759aa43428.htm).

## Measure API cost separately

Filter natively by category/class/type/view and bounding box as applicable before managed predicates. Use `FilteredElementCollector` quick filters to reduce element expansion; materialize required values once. Avoid repeated full-document collectors, parameter lookups, geometry extraction and element-by-element UI refresh. A bounding-box match is only a broad-phase candidate, not proof of geometric intersection.

Record candidate count, expanded elements, extraction time, pure compute time, apply/commit/regeneration time, changed count, transactions and cancellation latency. BenchmarkDotNet fits pure computation; measure host operations in the actual Revit build with representative models. Do not transfer historical timing numbers into universal thresholds. See Autodesk's [collector documentation](https://help.autodesk.com/cloudhelp/2026/ENU/Revit-API-MainReference/files/html/263cf06b-98be-6f91-c4da-fb47d01688f3.htm).
