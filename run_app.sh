#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BOOTSTRAP_SCRIPT="${ROOT_DIR}/scripts/bootstrap_python.sh"
RUN_SCRIPT="${ROOT_DIR}/scripts/run_backend.sh"
PID_FILE="${ROOT_DIR}/.magnetar_api.pid"
LOG_FILE="${ROOT_DIR}/.magnetar_api.log"

MODE="run"
DAEMON=0
HOST="127.0.0.1"
PORT="8000"
FORWARD_ARGS=()

usage() {
    cat <<USAGE
Usage:
  bash run_app.sh [--workflow <path>] [--format summary|json]
  bash run_app.sh --api [--host <host>] [--port <port>]
  bash run_app.sh --api --daemon start [--host <host>] [--port <port>]
  bash run_app.sh --api --daemon stop
  bash run_app.sh --api --daemon status

Notes:
  - Default mode runs the one-shot workflow execution path.
  - Daemon mode is only supported with --api.
USAGE
}

is_pid_running() {
    local pid="$1"
    kill -0 "${pid}" 2>/dev/null
}

start_daemon() {
    if [ -f "${PID_FILE}" ]; then
        local existing_pid
        existing_pid="$(cat "${PID_FILE}")"
        if [ -n "${existing_pid}" ] && is_pid_running "${existing_pid}"; then
            echo "MagnetarPrometheus API daemon is already running with PID ${existing_pid}."
            echo "Logs: ${LOG_FILE}"
            return 0
        fi
        rm -f "${PID_FILE}"
    fi

    echo "Starting MagnetarPrometheus API daemon on http://${HOST}:${PORT} ..."
    nohup bash "${RUN_SCRIPT}" --api --host "${HOST}" --port "${PORT}" >"${LOG_FILE}" 2>&1 &
    local daemon_pid=$!
    echo "${daemon_pid}" > "${PID_FILE}"
    echo "MagnetarPrometheus API daemon started with PID ${daemon_pid}."
    echo "Stop it with: bash run_app.sh --api --daemon stop"
    echo "Logs: ${LOG_FILE}"
}

stop_daemon() {
    if [ ! -f "${PID_FILE}" ]; then
        echo "No PID file found at ${PID_FILE}. Daemon does not appear to be running."
        return 0
    fi

    local daemon_pid
    daemon_pid="$(cat "${PID_FILE}")"

    if [ -z "${daemon_pid}" ]; then
        echo "PID file is empty. Cleaning up stale PID file."
        rm -f "${PID_FILE}"
        return 0
    fi

    if ! is_pid_running "${daemon_pid}"; then
        echo "No running process found for PID ${daemon_pid}. Cleaning up stale PID file."
        rm -f "${PID_FILE}"
        return 0
    fi

    echo "Stopping MagnetarPrometheus API daemon PID ${daemon_pid} ..."
    kill "${daemon_pid}" 2>/dev/null || true

    for _ in {1..20}; do
        if ! is_pid_running "${daemon_pid}"; then
            break
        fi
        sleep 0.25
    done

    if is_pid_running "${daemon_pid}"; then
        echo "PID ${daemon_pid} did not stop with SIGTERM; sending SIGKILL."
        kill -9 "${daemon_pid}" 2>/dev/null || true
    fi

    rm -f "${PID_FILE}"
    echo "MagnetarPrometheus API daemon stopped."
}

daemon_status() {
    if [ ! -f "${PID_FILE}" ]; then
        echo "MagnetarPrometheus API daemon is not running."
        return 1
    fi

    local daemon_pid
    daemon_pid="$(cat "${PID_FILE}")"

    if [ -n "${daemon_pid}" ] && is_pid_running "${daemon_pid}"; then
        echo "MagnetarPrometheus API daemon is running with PID ${daemon_pid}."
        echo "Logs: ${LOG_FILE}"
        return 0
    fi

    echo "PID file exists but daemon is not running."
    return 1
}

while (($#)); do
    case "$1" in
        --api)
            MODE="api"
            FORWARD_ARGS+=("$1")
            shift
            ;;
        --daemon)
            DAEMON=1
            shift
            ;;
        start|stop|status)
            if [ "${DAEMON}" -eq 1 ]; then
                MODE="$1"
                shift
            else
                FORWARD_ARGS+=("$1")
                shift
            fi
            ;;
        --host)
            HOST="${2:-}"
            FORWARD_ARGS+=("$1" "${HOST}")
            shift 2
            ;;
        --port)
            PORT="${2:-}"
            FORWARD_ARGS+=("$1" "${PORT}")
            shift 2
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        *)
            FORWARD_ARGS+=("$1")
            shift
            ;;
    esac
done

echo "Starting MagnetarPrometheus..."

if [ ! -x "${BOOTSTRAP_SCRIPT}" ]; then
    echo "Bootstrap script not found at ${BOOTSTRAP_SCRIPT}."
    exit 1
fi

if [ ! -x "${RUN_SCRIPT}" ]; then
    echo "Backend run script not found at ${RUN_SCRIPT}."
    exit 1
fi

if ! { [ "${DAEMON}" -eq 1 ] && [[ "${MODE}" == "stop" || "${MODE}" == "status" ]]; }; then
    bash "${BOOTSTRAP_SCRIPT}"
fi

if [ "${DAEMON}" -eq 1 ] && [ "${MODE}" != "api" ] && [ "${MODE}" != "start" ] && [ "${MODE}" != "stop" ] && [ "${MODE}" != "status" ]; then
    echo "Daemon mode requires --api and one of: start, stop, status"
    exit 1
fi

if [ "${DAEMON}" -eq 1 ]; then
    if [[ "${MODE}" != "start" && "${MODE}" != "stop" && "${MODE}" != "status" ]]; then
        echo "Daemon mode requires one of: start, stop, status"
        exit 1
    fi

    case "${MODE}" in
        start)
            start_daemon
            ;;
        stop)
            stop_daemon
            ;;
        status)
            daemon_status
            ;;
    esac
    exit 0
fi

echo
if [ "${MODE}" = "api" ]; then
    echo "Launching backend API in foreground mode..."
else
    echo "Launching example workflow..."
fi
bash "${RUN_SCRIPT}" "${FORWARD_ARGS[@]}"
