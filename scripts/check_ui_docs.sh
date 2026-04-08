#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
UI_DIR="${ROOT_DIR}/ui/src/app"

required_files=()
while IFS= read -r file; do
  required_files+=("${file}")
done < <(find "${UI_DIR}" -type f -name "*.ts" | sort)

for file in "${required_files[@]}"; do
  if ! head -n 5 "${file}" | rg -q '^/\*\*'; then
    echo "Missing top-of-file intent comment in ${file}" >&2
    exit 1
  fi
done

echo "UI documentation guard passed."
