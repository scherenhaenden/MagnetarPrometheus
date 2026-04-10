#!/usr/bin/env bash
set -euo pipefail
set -m

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BOOTSTRAP_SCRIPT="${ROOT_DIR}/scripts/bootstrap_python.sh"
BACKEND_SCRIPT="${ROOT_DIR}/scripts/run_backend.sh"
UI_DIR="${ROOT_DIR}/ui"
API_PORT="${API_PORT:-8000}"
API_HOST="${API_HOST:-127.0.0.1}"
UI_PORT="${UI_PORT:-4200}"
UI_NPM_SCRIPT="${UI_NPM_SCRIPT:-start:api}"

BACKEND_PID=""
UI_PID=""
SHUTTING_DOWN=0

cleanup() {
    local exit_code="${1:-0}"

    if [ "${SHUTTING_DOWN}" -eq 1 ]; then
        return
    fi
    SHUTTING_DOWN=1

    echo
    echo "Stopping MagnetarPrometheus local stack..."

    if [ -n "${UI_PID}" ] && kill -0 "${UI_PID}" 2>/dev/null; then
        # Send SIGTERM to the whole process group
        kill -TERM -"${UI_PID}" 2>/dev/null || kill "${UI_PID}" 2>/dev/null || true
        wait "${UI_PID}" 2>/dev/null || true
    fi

    if [ -n "${BACKEND_PID}" ] && kill -0 "${BACKEND_PID}" 2>/dev/null; then
        # Send SIGTERM to the whole process group
        kill -TERM -"${BACKEND_PID}" 2>/dev/null || kill "${BACKEND_PID}" 2>/dev/null || true
        wait "${BACKEND_PID}" 2>/dev/null || true
    fi

    exit "${exit_code}"
}

trap 'cleanup 130' INT TERM
trap 'cleanup $?' EXIT

if [ ! -x "${BOOTSTRAP_SCRIPT}" ]; then
    echo "Bootstrap script not found at ${BOOTSTRAP_SCRIPT}."
    exit 1
fi

if [ ! -x "${BACKEND_SCRIPT}" ]; then
    echo "Backend run script not found at ${BACKEND_SCRIPT}."
    exit 1
fi

if [ ! -d "${UI_DIR}" ]; then
    echo "UI directory not found at ${UI_DIR}."
    exit 1
fi

echo "Bootstrapping MagnetarPrometheus Python runtime..."
bash "${BOOTSTRAP_SCRIPT}"

echo "Ensuring UI dependencies exist..."
if [ ! -x "${UI_DIR}/node_modules/.bin/ng" ]; then
    (
        cd "${UI_DIR}"
        npm ci
    )
fi

echo "Starting backend API on http://${API_HOST}:${API_PORT} ..."
bash "${BACKEND_SCRIPT}" --api --host "${API_HOST}" --port "${API_PORT}" &
BACKEND_PID=$!

echo "Starting Angular UI with npm run ${UI_NPM_SCRIPT} ..."
(
    cd "${UI_DIR}"
    CI=1 NG_CLI_ANALYTICS=false npm run "${UI_NPM_SCRIPT}"
) &
UI_PID=$!

echo
echo "MagnetarPrometheus local stack is starting."
echo "UI:      http://localhost:${UI_PORT}"
echo "Backend: http://${API_HOST}:${API_PORT}/api"
echo "Press Ctrl+C to stop both processes."
echo

wait "${BACKEND_PID}" "${UI_PID}"
