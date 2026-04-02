# Architecture of MagnetarPrometheus

## High-Level Diagram

```text
                     +-----------------------------+
                     | Magnetar Canonical Model    |
                     | governance and project ops  |
                     +-------------+---------------+
                                   |
                                   v
+-------------------+    +---------+---------+    +----------------------+
| UI / Workflow     |<-->| SDK / Shared      |<-->| Backend Runtime      |
| Builder           |    | Schemas + Models  |    | Engine + Executors   |
+-------------------+    +-------------------+    +----------------------+
         |                           |                        |
         v                           v                        v
 visual graph editing         workflow contracts        execution, context,
 drag/drop nodes              serialization rules       logging, persistence
```

## What Exists Today Versus Later

Current implemented slice:

- CLI-triggered backend runtime
- workflow loader
- execution engine
- evaluator
- executor routing
- context accumulation
- shared SDK models and schema documents

Actively Planned (Next Slice):

- long-running backend service
- HTTP API
- persistent run storage
- user-facing web interface

Future / Unplanned:

- desktop application shell
- visual drag-and-drop workflow editor

This distinction is important because the current repository can execute workflows, but it does not yet expose a continuously running application surface.

## Component Descriptions

### Backend

Responsibility:

- workflow loading and validation
- orchestration engine
- executor routing
- runtime context management
- logging and persistence
- runtime bootstrap and dependency readiness checks
- CLI and script entrypoints for local execution
- future API/server entrypoints for repeated execution and inspection

Technologies:

- Python
- Pydantic
- YAML/JSON workflow definitions

Python is the primary implementation architecture for the first usable version. That matters beyond language choice. It means packaging, startup behavior, module discovery, dependency handling, and local execution flows should be designed coherently around Python first, while still preserving contract boundaries for future non-Python executors.

Current runtime shape:

- invoked from the shell
- loads one workflow
- executes it to completion
- prints structured JSON
- exits

That is a proof-of-concept execution path, not yet an always-on orchestration service.

### SDK

Responsibility:

- shared workflow schemas
- contract definitions between backend and UI
- serialization and validation helpers
- future client helpers for external integrations

Technologies:

- initially Python package plus language-neutral schema files

### UI

Responsibility:

- visual workflow creation
- drag-and-drop graph editing
- node configuration
- workflow validation feedback
- export/import using the shared schema

Technologies:

- intentionally undecided at this stage

Current status:

- no working UI implementation exists yet
- the nearest implemented artifact is the UI graph schema in `sdk/schemas/workflow-graph-schema.md`
- the repo reserves the UI surface architecturally, but the actual application layer still needs to be built

## Key Design Decisions

- The repo root remains the IDE project root.
- Python code starts under `backend/src/`.
- Shared contracts are not buried inside backend internals.
- The visual builder is treated as a first-class future subsystem, not a later add-on.
- The product follows the Magnetar canon for project administration but does not define the canon itself.
- The repository must expose explicit scripts for running the backend, tests, and bootstrap flows.
- The runtime should detect missing Python dependencies at startup and install or guide installation automatically when the chosen execution mode permits it.
- Release and build metadata should use a timestamp-oriented version stamp in the form `yyyy.MM.dd HH:mm:ss.SSS`.
- The repository should be pipeline-driven for test, validation, packaging, and release operations.

## Current Execution Flow

Today, the easiest execution path is:

```text
run_app.sh
  -> scripts/bootstrap_python.sh
  -> scripts/run_backend.sh
  -> python -m magnetar_prometheus.cli
  -> WorkflowLoader
  -> Engine
  -> PythonExecutor / registered handlers
  -> RunContext JSON printed to terminal
```

That means the current product slice is visible mainly through terminal output. There is no active UI rendering layer sitting on top of this runtime yet.

## Python Runtime Constraints

- The backend must have a clear Python entrypoint and script-based launch path.
- Missing libraries should be detected before execution reaches deep runtime code.
- Where allowed by execution policy, the startup flow should install missing dependencies dynamically and continue.
- If automatic installation is not permitted or fails, the error path must be explicit and actionable.
- Dependency auto-install behavior must be isolated so it does not contaminate domain logic or shared contracts.

## Versioning Strategy

The repository follows a strict separation between Python package semantic versions and the canonical version stamp:

- Python packages (`backend` and `sdk`) use standard PEP-440 versioning (e.g., `0.1.0`) for internal metadata and standard toolchain compatibility.
- The canonical release version stamp for MagnetarPrometheus follows the format `yyyy.MM.dd HH:mm:ss.SSS`. This stamp is generated during the delivery lifecycle and is meant for runtime reporting, release metadata, and external logging. It acts as the product-level identifier, while the package-level versions are used primarily for local dependency resolution.

## Delivery Automation Constraints

- CI pipelines should run the standard validation and test scripts.
- Release flows should produce an auditable version stamp based on the repository versioning rule.
- Pipeline design should keep backend, shared SDK contracts, and future UI delivery separable.

## Architectural Gap To Close Next

The biggest gap is not in the engine core anymore. It is in product surfacing.

The engine exists, but users still lack:

- a persistent entrypoint
- a submission model for runs/jobs
- a place to inspect executions without reading raw terminal JSON
- a first interactive UI or API layer

The newly established planning slice formally targets the persistent API and web UI to address this gap.
