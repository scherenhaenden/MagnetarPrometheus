# MagnetarPrometheus

MagnetarPrometheus is a workflow automation and orchestration platform in the same broad space as tools like n8n: a system for defining flows as data, executing them through a controlled runtime, exposing them through an API, and evolving toward a visual builder UI.

The repository currently contains:

- a Python backend runtime and local API server
- an Angular web UI with mock and API transport modes
- a desktop shell skeleton
- shared contracts, tests, and validation scripts

The core product idea is simple: workflows should be modeled, executed, observed, and eventually edited visually without hardwiring every process into application code.

## What You Can Do Today

Right now you can:

- run the backend workflow engine locally
- start the local API server
- open the Angular UI in mock mode or API mode
- exercise the current UI slices for run history, run detail, job submission, settings, and workflow catalog

Current limitations:

- the product is still a proof-of-concept baseline, not a finished n8n-style platform
- the UI exists and is usable, but the full visual workflow-builder experience is not implemented yet
- some runtime and API surfaces are still intentionally minimal

## Quick Start

### Full Stack

From the repository root:

```bash
./run_full_stack.sh
```

That command:

- bootstraps the Python environment if needed
- installs UI dependencies if needed
- starts the backend API on `127.0.0.1:8000`
- starts the Angular UI on `http://localhost:4200`
- stops both when you press `Ctrl+C`

### Backend Only

Run the example workflow:

```bash
bash run_app.sh
```

Start the local API server:

```bash
bash scripts/run_backend.sh --api --host 127.0.0.1 --port 8000
```

Manage the local API server through the repo-root launcher:

```bash
bash run_app.sh --api --daemon start
bash run_app.sh --api --daemon status
bash run_app.sh --api --daemon stop
```

Daemon mode stores host/port-specific PID and log files in the repo root by default.
You can override those paths with `MAGNETAR_API_PID_FILE` and `MAGNETAR_API_LOG_FILE`.

### UI Only

Mock mode:

```bash
cd ui
npm ci
npm run start:mock
```

API mode:

```bash
cd ui
npm ci
npm run start:api
```

## Product Overview

MagnetarPrometheus is meant to become a workflow platform with four clear layers:

1. Workflow runtime
2. API surface
3. Web UI
4. Future visual workflow builder and richer operator experience

Today, the most mature layer is still the runtime. The UI and API are already real enough to run locally, but they are still growing toward the broader product vision.

## Repository Structure

```text
MagnetarPrometheus/
  backend/                # Python orchestration engine and local API server
  sdk/                    # Shared contracts and schemas
  ui/                     # Angular frontend
  desktop/                # Electron shell skeleton
  scripts/                # Bootstrap, validation, and helper scripts
  run_app.sh              # Run the backend workflow path
  run_full_stack.sh       # Run backend API + Angular UI together
```

## Technology Choices

The stack matters because it defines the current implementation shape, but it is not the product story.

- Python powers the workflow runtime and local API layer
- Angular powers the current web UI
- Electron is present as a lightweight desktop host skeleton

These are implementation choices for delivering the workflow product. They are not the main point of the repository.

## Current Status

Implemented baseline:

- backend workflow execution
- local HTTP API mode
- Angular UI shell and feature slices
- mock/API transport switching
- validation scripts for backend and UI tiers

Not implemented yet:

- a full drag-and-drop workflow builder
- a complete production-grade API surface
- the broader editor/product ergonomics you would expect from a mature n8n-class platform

## Development And Validation

Repository-level validation:

```bash
bash scripts/run_tests.sh
```

UI-only validation:

```bash
bash scripts/run_tests.sh ui
```

Backend-only validation:

```bash
bash scripts/run_tests.sh backend
```

## Project Docs

The repository also carries governance and planning documents, but those are supporting project-management artifacts, not the product itself.

- [ARCHITECTURE.md](/Users/edwardflores/Projects/Development/MagnetarPrometheus/ARCHITECTURE.md)
- [REQUIREMENTS.md](/Users/edwardflores/Projects/Development/MagnetarPrometheus/REQUIREMENTS.md)
- [PLAN.md](/Users/edwardflores/Projects/Development/MagnetarPrometheus/PLAN.md)
- [STATUS.md](/Users/edwardflores/Projects/Development/MagnetarPrometheus/STATUS.md)
- [BITACORA.md](/Users/edwardflores/Projects/Development/MagnetarPrometheus/BITACORA.md)
- [TESTING.md](/Users/edwardflores/Projects/Development/MagnetarPrometheus/TESTING.md)
- [RULES.md](/Users/edwardflores/Projects/Development/MagnetarPrometheus/RULES.md)

If you are trying to understand the product, start with this README and the runnable commands above. If you are trying to understand repository governance, then move into the planning and rules documents.


## Plugin-Ready Runtime (New)

MagnetarPrometheus now includes a generic backend plugin layer for step capability extension.

What this enables today:

- bundled example capabilities are loaded through a plugin manager instead of hard-coded wiring
- plugin contracts are typed (manifest + runtime handlers) and API-version checked
- the runtime rejects conflicting step ownership early for deterministic startup

What remains intentionally future-scoped:

- plugin signing and trust policy controls
- remote plugin distribution/catalog flows
- richer UI/plugin capability metadata surfaces

This preserves the current local developer experience while opening a clear path for adding new capabilities without repeatedly modifying core engine wiring.
