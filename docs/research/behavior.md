# Behavioral evidence

2026-10-28, fresh-context agent scenarios; these are qualitative checks, not statistical reliability claims.

Before the Revit skill existed, the control read upstream project/concurrency/performance/package skills and answered the 100k-element/modeless/multi-year scenario. It correctly rejected worker API reads and AOT, but described the year/runtime map as only a hypothesis and omitted 2025.5/2026.5 transitions. This is a retrieval/reference gap, not evidence the agent always violates threading rules.

After reading the new skill and its references, a fresh agent correctly:

1. Selected year AND update/runtime-specific adapters, rejected latest-package assumptions, and separated snapshot/compute/apply for 100k elements.
2. Rejected a net10 binary on 2025.4, while allowing tested existing net8 binaries on 2025.5 rather than demanding universal recompilation.
3. Rejected Dispatcher-after-await as API context, transactions in DocumentChanged, and queued work against closed documents.
4. Rejected an open group across callbacks and a promise of atomic rollback after committed batches; described partial completion.
5. Rejected a domain interface wrapping Document as a pure boundary and required detached DTO tests.

Packaging regression ran before changes: five subtest failures for four old manifest identities and missing Revit registration. All three test methods passed after branding/registration/index changes. Existing marketplace and Codex validators also passed. No Revit host execution is implied.

## Final-review regression

The independent review found that using only MessagePack's generated resolver removed built-in formatter fallback. With pinned MessagePack 3.1.12, `SKILL_TEST_REF=ceaf331 python -m unittest discover -s tests -p test_examples.py -v` reproduced `FormatterNotRegisteredException` for a nested Guid. The final skill uses Standard options (which retain generated and built-in/collection resolution); the same test now round-trips Guid and List<Guid> successfully. This is a managed-runtime test, not Native AOT certification.

The suite now has **six** automated tests. The new fixture uses a committed NuGet lock file with locked restore. MessagePack and its test dependencies have MIT licenses; `dotnet list Repro.csproj package --vulnerable --include-transitive` found no vulnerable packages in the verification fixture. These are test dependencies only, not a prescribed Revit dependency stack.
