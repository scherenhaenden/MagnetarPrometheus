# MagnetarPrometheus Desktop Shell (Electron Skeleton)

This directory contains the desktop host shell that wraps the Angular UI.

## Scope

- Main process entrypoint (`src/main.js`)
- Preload secure bridge placeholder (`src/preload.js`)
- Dev mode by pointing `MP_UI_DEV_SERVER_URL` to `http://localhost:4200`
- Prod mode by loading Angular build output from `ui/dist/.../index.html`

## Non-goals in this packet

- No desktop-only business features
- No duplicated UI stack
- No direct backend coupling from Electron main process

## Run

```bash
cd desktop
npm ci
MP_UI_DEV_SERVER_URL=http://localhost:4200 npm run start
```
