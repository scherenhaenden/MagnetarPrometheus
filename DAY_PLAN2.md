# DAY_PLAN2: User-Centered Advance for MagnetarPrometheus

This document consolidates the planned steps to transition MagnetarPrometheus from a batch-style CLI tool into an interactive, user-facing application core.

## 1. High-Level Strategy
**Objective**: Enhance the user experience by providing visible, interactive interfaces (CLI and Web) and updating the project roadmap to reflect a user-centered direction.

### Proposed Changes
- **CLI UX**: Add ANSI colors, scannable summaries, and clearer progress reporting.
- **Web UI Shell**: Serve a modern `ui/index.html` from the API server with a "Run Example" button and result display.
- **API**: Extend the minimal server to serve static files from `ui/`.
- **Governance**: Add `ms-04: Visible Application Surface` to the project roadmap.

---

## 2. Intended PLAN.md Updates
The following changes are planned for the project baseline:

### New Milestone
| Milestone ID | Name | Target Date | Description | Completion Criteria |
| --- | --- | --- | --- | --- |
| `ms-04` | Visible Application Surface | 2026-05-10 | Transition from CLI PoC to an interactive application with a visible UI and improved CLI UX. | A web UI shell exists, can trigger workflows via API, and the CLI provides styled summaries. |

### New Tasks
| Task ID | Milestone | Title | Owner | State | Notes |
| --- | --- | --- | --- | --- | --- |
| `task-112` | `ms-04` | Enhance CLI with styled summaries and clearer progress | Edward + AI | `in_progress` | Improve user readability and scannability of the batch CLI output. |
| `task-113` | `ms-04` | Serve static Web UI shell from the API server | Edward + AI | `planned` | Update the minimal server to serve the `ui/` directory. |
| `task-114` | `ms-04` | Create interactive single-file Web UI MVP | Edward + AI | `planned` | Build the first visible product shell in `ui/index.html`. |
| `task-115` | `ms-04` | Update project status and governance for user-centeredness | Edward + AI | `in_progress` | Refactor PLAN.md, STATUS.md, and BITACORA.md to reflect the new direction. |

---

## 3. Intended STATUS.md Updates
The project status will be updated to reflect the new reality:

### Executive Summary Update
MagnetarPrometheus is transitioning from a backend proof of concept to an interactive, user-facing application.

**What is real today**:
- Minimal API server exists and can execute the example workflow.
- High-coverage backend core and SDK.

**What is being built right now**:
- A visible application surface (Web UI MVP) to make the product interactive.
- Improved CLI UX with styled summaries and clearer progress reporting.

---

## 4. Implementation Details

### CLI Refinement
- Add ANSI color support for scannable summaries.
- Update `_print_summary` in `cli.py` to be more robust and informative.

### Web UI & API
- **`ui/index.html`**: A clean, single-file UI using a CDN-based CSS framework.
- **`server.py`**:
    - Add a basic file server to `MagnetarAPIHandler.do_GET`.
    - Support serving the `ui/` directory at the root `/`.

---

## 5. Next Steps
1. Finalize the `ui/index.html` design.
2. Implement static file serving in the backend API.
3. Update the CLI rendering logic.
4. Verify end-to-end with `bash run_app.sh` and `bash run_app.sh --api`.
