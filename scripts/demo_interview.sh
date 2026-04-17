#!/usr/bin/env bash

set -euo pipefail

API_HOST="${API_HOST:-127.0.0.1}"
API_PORT="${API_PORT:-8000}"
DASHBOARD_PORT="${DASHBOARD_PORT:-8501}"

export PHANTOMSCOPE_OFFLINE_MODE="${PHANTOMSCOPE_OFFLINE_MODE:-true}"

cleanup() {
  if [[ -n "${API_PID:-}" ]]; then
    kill "${API_PID}" >/dev/null 2>&1 || true
  fi
  if [[ -n "${DASHBOARD_PID:-}" ]]; then
    kill "${DASHBOARD_PID}" >/dev/null 2>&1 || true
  fi
}

trap cleanup EXIT INT TERM

echo "Starting PhantomScope interview demo"
echo "Offline mode: ${PHANTOMSCOPE_OFFLINE_MODE}"

uvicorn phantomscope.api.main:app --host "${API_HOST}" --port "${API_PORT}" --reload &
API_PID=$!

streamlit run app/dashboard.py --server.port "${DASHBOARD_PORT}" &
DASHBOARD_PID=$!

echo
echo "API:        http://${API_HOST}:${API_PORT}/api/v1/health"
echo "Dashboard:  http://127.0.0.1:${DASHBOARD_PORT}"
echo
echo "Suggested live demo target: acme"
echo "Press Ctrl+C to stop both services."

wait
