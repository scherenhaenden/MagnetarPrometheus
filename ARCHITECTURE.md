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

Technologies:

- Python
- Pydantic
- YAML/JSON workflow definitions

Python is the primary implementation architecture for the first usable version. That matters beyond language choice. It means packaging, startup behavior, module discovery, dependency handling, and local execution flows should be designed coherently around Python first, while still preserving contract boundaries for future non-Python executors.

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

## Key Design Decisions

- The repo root remains the IDE project root.
- Python code starts under `backend/src/`.
- Shared contracts are not buried inside backend internals.
- The visual builder is treated as a first-class future subsystem, not a later add-on.
- The product follows the Magnetar canon for project administration but does not define the canon itself.
- The repository must expose explicit scripts for running the backend, tests, and bootstrap flows.
- The runtime should detect missing Python dependencies at startup and install or guide installation automatically when the chosen execution mode permits it.

## Python Runtime Constraints

- The backend must have a clear Python entrypoint and script-based launch path.
- Missing libraries should be detected before execution reaches deep runtime code.
- Where allowed by execution policy, the startup flow should install missing dependencies dynamically and continue.
- If automatic installation is not permitted or fails, the error path must be explicit and actionable.
- Dependency auto-install behavior must be isolated so it does not contaminate domain logic or shared contracts.
