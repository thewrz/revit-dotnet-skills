# Revit skills implementation plan and evidence ledger

Goal: retain useful upstream .NET expertise while making this fork safe and discoverable for Revit C# work.
Architecture: one Revit entry skill with focused version/API, architecture, and ecosystem references; contextual guards on inherited skills and agents. Preserve all 39 upstream skills and MIT attribution. Retain a fork because most content remains shared.
Spec: user's 2026-10-28 request; no further questions. Research precedes edits; no merge or release tag authorized.

## Decisions and contracts

- Structs: compatibility records identify Revit year, update, runtime, TFM, API assembly/package and deployment target; domain snapshots contain no Autodesk types.
- Interfaces: host adapter snapshots inputs, domain computes a change plan, adapter revalidates and applies it in valid API context.
- Change map: manifests/README/index; new `revit-development` skill; inherited scope notes and verified factual corrections; research ledger and packaging tests.
- Spike: baseline agent applied upstream skills to a 100k-element/modeless/multi-year task. It knew basic threading limits but could not resolve the runtime matrix and missed .5 transitions. No product spike retained.
- Invariants: every installed skill is registered/indexed; fork names agree; references resolve; year+update select runtime; no API types cross worker boundaries; transactions close before yielding; examples label source/version limits.
- Institutional choices (mapping, composition, CQRS, channels, Akka, fail-fast policies) remain intact even where Microsoft makes different recommendations.
- Scope: source audit, structural checks, behavioral scenarios; not execution of every inherited .NET example or licensed Revit host integration.

## Work

- [x] Clone upstream; fork to thewrz; preserve upstream SHA 5ca5db8cf25566f19d2a5dc53204d4af22b23a0d; issue #1.
- [x] Research Microsoft/Autodesk/TBC/package sources and run no-Revit-skill baseline.
- [x] Add failing packaging regression checks, brand fork and register Revit guidance; validate.
- [x] Write release-aware Revit skill/references; run fresh behavioral scenarios against baseline gaps.
- [x] Correct substantiated inherited errors, preserve opinions, publish complete skill inventory with source/verification limits.
- [x] Run validators, shell lint, regression checks, index drift check and final review; publish draft PRs.

## Review focus

Point releases changing runtime within a year; identical TFM across different API years; API-context lifetime after await; rollback/cancellation with pending transactions; installation losing reference files.
