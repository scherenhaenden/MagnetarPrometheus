# MagnetarPrometheus UI (Angular)

This directory now contains the **first browser-visible Angular shell** for MagnetarPrometheus.

## Current State (2026-04-07)

- Workspace skeleton: ✅ implemented
- Routed shell/navigation: ✅ implemented
- Frontend data-contract seam + mock adapter: ✅ implemented
- Run history and run detail slice: ✅ implemented (mock-backed)
- Job submission slice: ✅ implemented (mock-backed)
- API-backed transport integration: 🚧 pending
- Desktop shell integration: 🚧 pending

Approximate completion for the `11 → 20` frontend packet stream: **65%**.

## Directory Intent

- `src/app/core/`: app frame and top-level shell structure
- `src/app/shared/models`: frontend contract interfaces decoupled from raw transport payloads
- `src/app/shared/services`: service boundary (`FrontendDataService`) + mock adapter
- `src/app/features/*`: isolated product slices (overview, runs, run detail, submission, workflow catalog, settings)

## Local Run Flow

From repository root:

```bash
cd ui
npm ci
npm run start
```

Open `http://localhost:4200`.

## Validation

```bash
cd ui
npm run build
npm run test:ci
```

## Boundary Clarification

The current UI defaults to **mock transport mode** via `MockFrontendDataService`.
That is intentional so feature work can move in parallel while backend HTTP persistence/API work is still landing.
