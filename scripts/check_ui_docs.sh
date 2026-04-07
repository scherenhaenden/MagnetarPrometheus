#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
UI_DIR="${ROOT_DIR}/ui/src/app"

required_files=(
  "${UI_DIR}/app.routes.ts"
  "${UI_DIR}/shared/models/frontend-contracts.ts"
  "${UI_DIR}/shared/services/frontend-data.service.ts"
  "${UI_DIR}/shared/services/mock-frontend-data.service.ts"
)

for file in "${required_files[@]}"; do
  if ! head -n 5 "${file}" | rg -q '^/\*\*'; then
    echo "Missing top-of-file intent comment in ${file}" >&2
    exit 1
  fi
done

echo "UI documentation guard passed."
