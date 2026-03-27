#!/usr/bin/env bash
set -euo pipefail

# This script generates the canonical version stamp for MagnetarPrometheus.
# Format: yyyy.MM.dd HH:mm:ss.SSS
PYTHON_BIN="${PYTHON_BIN:-python3}"

"${PYTHON_BIN}" - <<'PY'
from datetime import datetime, timezone

now = datetime.now(timezone.utc)
print(now.strftime("%Y.%m.%d %H:%M:%S.") + f"{now.microsecond // 1000:03d}")
PY
