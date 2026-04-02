# WIP Guidelines for MagnetarPrometheus

## Default WIP Limit

No individual contributor or AI collaborator should hold more than 2 tasks in `in_progress` simultaneously.

## Exceptions

Exceptions require:

- explicit justification
- a note in [BITACORA.md](/home/edward/Development/MagnetarPrometheus/BITACORA.md)
- acknowledgment in planning if it affects delivery

## Practical Guidance

- finish or review current work before starting additional tasks
- split oversized tasks before violating WIP limits
- prefer moving tasks to `ready` rather than starting too many in parallel
- parallel work must be divided by disjoint write ownership so contributors do not collide in the same surface
- each round should preferably leave one more thing runnable, visible, or inspectable; prefer work packets that each unlock a small user-visible or user-testable increment instead of only internal progress

## Disjoint Write Ownership

Disjoint write ownership means parallel contributors should own different writable surfaces so they are not editing the same files or tightly coupled implementation area at the same time.

Example:

- one contributor updates governance documents such as `RULES.md` and `CONTRIBUTING.md`
- another contributor updates runtime code under `backend/src/`

That split reduces merge collisions and makes review responsibility clearer.
