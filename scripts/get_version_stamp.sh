#!/usr/bin/env bash
set -euo pipefail

# This script generates the canonical version stamp for MagnetarPrometheus.
# Format: yyyy.MM.dd HH:mm:sss
date -u '+%Y.%m.%d %H:%M:%S%3N'
