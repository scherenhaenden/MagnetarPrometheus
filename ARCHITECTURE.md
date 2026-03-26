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

Technologies:

- Python
- Pydantic
- YAML/JSON workflow definitions

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

