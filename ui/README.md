# MagnetarPrometheus UI

This directory contains the user interface for MagnetarPrometheus.

## Current Status: MVP Shell (Proof of Concept)

The current state of the UI is an **MVP Shell**. It provides a first visible application surface to demonstrate the intended product direction (Dashboard, Workflows, Runs), but **it is currently disconnected from the backend runtime and operates on mocked data**.

This shell was created to make the product feel less invisible and provide a clear visual target for future API integration.

### How to Run

Because this is a static shell, there is no build step or dev server required.

Simply open `ui/index.html` in any modern web browser.

```bash
# MacOS
open ui/index.html

# Linux
xdg-open ui/index.html

# Windows
start ui/index.html
```

### What You Can Do

*   **Navigate:** Switch between Dashboard, Workflows, and Runs views.
*   **View Run Console:** Select different mock runs in the Runs view to see simulated execution logs.
*   **Run Example (Mock):** Click the "Run Example Workflow" button in the top right to see a simulated modal execution sequence.

## Future Goals

As the backend API matures, this UI will be updated to:

- connect to the real backend service to fetch real workflows and run history
- submit real workflow executions via HTTP API
- implement the visual graph editor:
  - create complete workflows through click, drag, and drop interactions
  - edit node configuration and branching rules visually
  - serialize workflows against the shared schema in `sdk/schemas/`
- remain decoupled from backend internals
