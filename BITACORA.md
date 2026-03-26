# Logbook of MagnetarPrometheus

This document is the project logbook. It records decisions, state changes, discoveries, and exceptions in reverse chronological order.

## Entry Format

Each entry should use:

- Timestamp: `YYYY-MM-DD HH:MM Z`
- Author: person or AI agent name
- Entry: concise event description

## Entries

---
**Timestamp:** 2026-03-26 10:58 UTC
**Author:** Codex
**Entry:** GitHub tracking initialized. Created issues `#1` runtime domain models and schema contracts, `#2` CI pipelines, `#3` timestamp-based versioning, `#4` 100 percent coverage enforcement, `#5` dependency detection and auto-install flow, `#6` runnable scripts, and `#7` UI graph model. Discussion creation is currently blocked because the repository has no discussion categories configured.

---
**Timestamp:** 2026-03-26 10:49 UTC
**Author:** Codex
**Entry:** Decision: canonical versioning now requires the timestamp format `yyyy.MM.dd HH:mm:sss`. CI/CD expectations were expanded so the repository must gain pipelines for testing, validation, and release flows in addition to local scripts.

---
**Timestamp:** 2026-03-26 10:42 UTC
**Author:** Codex
**Entry:** Decision: planning, architecture, requirements, and testing were tightened to require runnable scripts, Python-first runtime structure, startup-time dependency detection with dynamic installation when permitted, and a strict 100 percent automated coverage target.

---
**Timestamp:** 2026-03-26 10:28 UTC
**Author:** Codex
**Entry:** Decision: agile operating guidance expanded so daily updates must include user-visible progress. GitHub issues are designated for actionable work items and GitHub discussions for broader product, architecture, and governance conversations.

---
**Timestamp:** 2026-03-26 10:20 UTC
**Author:** Codex
**Entry:** Decision: repository structure established around `backend/`, `sdk/`, and `ui/` to keep the Python runtime, shared contracts, and future drag-and-drop workflow builder decoupled while preserving a single IDE project root.

---
**Timestamp:** 2026-03-26 10:18 UTC
**Author:** Codex
**Entry:** `task-102`: state changed from `planned` to `done`. Modular repository layout created to support PyCharm as the initial IDE without nesting the entire project under an additional top-level directory.

---
**Timestamp:** 2026-03-26 10:16 UTC
**Author:** Codex
**Entry:** `task-101`: state changed from `planned` to `done`. Canonical governance documents initialized. Clarified that MagnetarPrometheus follows the Magnetar canonical model but is not itself the canonical model repository.

## Immutability

This logbook should not be rewritten retroactively. Corrections must be made by adding a new entry that clarifies an earlier one.
