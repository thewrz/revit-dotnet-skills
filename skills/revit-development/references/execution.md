# Execution, transactions and performance

## Boundaries before optimization

Use `IExternalCommand.Execute`, an appropriate Revit callback, or `IExternalEventHandler.Execute` for model access. Each callback has restrictions: being in API context does not mean the document is writable (for example, `DocumentChanged` is read-only). Do not start transactions in read-only callbacks or nest `Transaction` objects.

The Building Coder's [thread-safety discussion](https://jeremytammik.github.io/tbc/a/1244_no_multithreading.htm) includes Autodesk API lead Arnošt Löbel's explanation: even reads may expand internal element state. Its addendum explicitly exempts `ExternalEvent.Raise`. Therefore copying a list of `Element` wrappers does not make parameter reads safe on workers. Copy numeric/string/domain values in the callback instead.

## Snapshot → compute → present/apply

Recommended assembly responsibilities:

| Assembly | Inputs/outputs | Dependencies |
|---|---|---|
| Domain | Immutable snapshots → summaries, reports or proposed changes | Plain .NET; no Autodesk/UI types |
| Revit adapter per API target | Model → snapshots; validated changes → model | Matching Revit API, Domain |
| UI/orchestration | User intent, progress, cancellation, results | Domain contracts and dispatch abstraction |

Test business behavior through detached inputs and outputs without loading Revit/WPF. Command handlers and windows coordinate this work; the independent domain owns its rules.

An interface hiding a `Document` behind a method called by background business logic is still an API call. Snapshot the needed data first. Convert `XYZ`, transforms, geometry and units to domain-owned values where needed; never enumerate a collector/lazy projection after leaving API context. Preserve `long` IDs with document identity; IDs alone are not globally unique, and saved/cross-session workflows need an appropriate persistent identity such as `UniqueId` resolved inside the adapter.

Revalidate before applying: intended document remains open, identity matches, elements still exist, relevant values match the snapshot, parameters are writable and worksharing permits edits. Reject/recompute stale changes rather than silently applying results to a different active model. If snapshotting across callbacks, detect intervening changes; multiple chunks are not an atomic snapshot.

## Modeless and asynchronous work

Create the external event in valid API context. UI/background code enqueues detached intent and raises it. Handle the raise result and coalescing/pending requests; repeated raises do not guarantee one callback per request. Define a bounded FIFO or latest-request policy, single consumer and cancellation semantics. Stop/dispose subscriptions and handlers with the add-in/UI lifetime.

Keep each callback synchronous and bounded. A Task-based wrapper is a dispatcher, not an API worker thread. No `.Wait()`/`.Result` blocking on dispatch from Revit's thread; no `async void` API handler that loses its callback context. After asynchronous I/O or CPU computation, explicitly dispatch the apply phase again. WPF Dispatcher marshaling is only UI marshaling.

Check cancellation before dispatch and between batches. Cancellation cannot preempt arbitrary native API work. Stop scheduling, roll back the active uncommitted batch where appropriate, and report already committed batches accurately. Throttle progress; neither a progress event nor a timer may query the model outside context.

Sources: Autodesk [External Events](https://help.autodesk.com/cloudhelp/2025/ENU/Revit-API/files/Revit_API_Developers_Guide/Introduction/Add_In_Integration/External_Events_html.html); Tammik [API context and polling](https://jeremytammik.github.io/tbc/a/1383_external_event_10_year.html). Queue, stale-input and cancellation policies above are this fork's engineering guidance inferred from deferred execution, not built-in ExternalEvent guarantees.

## Transactions and regeneration

- Read-only extraction normally needs no transaction. Compute and remote I/O outside transactions.
- Apply changed values only, with as few transactions as undo, failure isolation and responsiveness permit. Avoid a transaction and `Regenerate()` per element. There is no universal batch size: measure representative projects, including workshared models.
- A `TransactionGroup` may group completed transactions into one undo item via `Assimilate`, but does not remove their commit/regeneration cost. Keep groups within a single valid callback. For work spanning callbacks, close all transactions/groups before yielding; explain partial completion/undo semantics instead of promising atomicity.
- Check `Start`, `Commit` and rollback status. `Committed`, `RolledBack` and `Pending` are different outcomes. Do not report success or start another transaction while failure processing is pending; follow the release's failure-handling contract. Never blanket-delete all warnings to force success.
- Regenerate explicitly only when subsequent operations require updated derived state before commit. A regeneration failure requires aborting the operation/transaction; do not catch and keep reading or writing the damaged document state.

Sources: Autodesk [Transactions](https://help.autodesk.com/cloudhelp/2024/ENU/Revit-API/files/Revit_API_Developers_Guide/Basic_Interaction_with_Revit_Elements/Revit_API_Revit_API_Developers_Guide_Basic_Interaction_with_Revit_Elements_Transactions_html.html), [Regenerate](https://help.autodesk.com/cloudhelp/2026/ENU/Revit-API-MainReference/files/html/22468e2c-9772-8478-0816-c9759aa43428.htm).

## Measure API cost separately

Filter natively by category/class/type/view and bounding box as applicable before managed predicates. Use `FilteredElementCollector` quick filters to reduce element expansion; materialize required values once. Avoid repeated full-document collectors, parameter lookups, geometry extraction and element-by-element UI refresh. A bounding-box match is only a broad-phase candidate, not proof of geometric intersection.

Record candidate count, expanded elements, extraction time, pure compute time, apply/commit/regeneration time, changed count, transactions and cancellation latency. BenchmarkDotNet fits pure computation; measure host operations in the actual Revit build with representative models. Do not transfer historical timing numbers into universal thresholds. See Autodesk's [collector documentation](https://help.autodesk.com/cloudhelp/2026/ENU/Revit-API-MainReference/files/html/263cf06b-98be-6f91-c4da-fb47d01688f3.htm).
