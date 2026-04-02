#!/usr/bin/env bash
set -euo pipefail

# This script generates the canonical version stamp for MagnetarPrometheus.
# Format: yyyy.MM.dd HH:mm:ss.SSS
python3 -c 'import datetime; now = datetime.datetime.now(datetime.timezone.utc); print(now.strftime("%Y.%m.%d %H:%M:%S.") + f"{now.microsecond // 1000:03d}")'
