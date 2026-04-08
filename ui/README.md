# MagnetarPrometheus UI (Angular)

## Current State (2026-04-07)

- Packet 13 web shell: ✅ complete
- Packet 14 data contract boundary: ✅ complete (mock + API adapters + mappers)
- Packet 15 design system/layout primitives: ✅ complete
- Packet 16 run history/detail slice: ✅ complete
- Packet 17 job submission slice: ✅ complete
- Packet 18 desktop shell skeleton: ✅ complete (Electron skeleton in `../desktop`)
- Packet 19 testing/doc guardrails: ✅ complete (UI test tier + docs guard script integrated)
- Packet 20 local run flow docs: ✅ complete

Approximate completion for packets `11 → 20`: **100% in agreed scope**.

## Transport Modes

- **Mock mode** (`environment.development.ts`): `useMockDataService: true`
- **API mode** (`environment.api.ts` and production env): `useMockDataService: false`
- Strategy provider: `src/app/shared/services/frontend-data.provider.ts`

## Local Run Flow

```bash
cd ui
npm ci
npm run start:mock
```

API mode: 

```bash
cd ui
npm run start:api
```

## Validation

```bash
cd ui
npm run build
npm run test:ci
npm run check:docs
```

Root-level integration:

```bash
bash scripts/run_tests.sh ui
```
