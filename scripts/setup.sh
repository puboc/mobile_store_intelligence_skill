#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd -- "${SCRIPT_DIR}/.." && pwd)"
VENV_DIR="${ROOT_DIR}/.venv"
PY_TARGET_DIR="${ROOT_DIR}/.python-packages"
APPLE_VENDOR_DIR="${ROOT_DIR}/vendor/app-store-scraper"
GOOGLE_VENDOR_DIR="${ROOT_DIR}/vendor/google-play-scraper"

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 is required" >&2
  exit 1
fi

if ! command -v npm >/dev/null 2>&1; then
  echo "npm is required" >&2
  exit 1
fi

if [[ ! -f "${APPLE_VENDOR_DIR}/package.json" ]]; then
  echo "Missing vendored app-store-scraper source: ${APPLE_VENDOR_DIR}" >&2
  exit 1
fi

if [[ ! -f "${GOOGLE_VENDOR_DIR}/pyproject.toml" ]]; then
  echo "Missing vendored google-play-scraper source: ${GOOGLE_VENDOR_DIR}" >&2
  exit 1
fi

if [[ ! -x "${VENV_DIR}/bin/pip" ]]; then
  if python3 -m venv "${VENV_DIR}" >/dev/null 2>&1; then
    :
  else
    rm -rf "${VENV_DIR}"
  fi
fi

if [[ -x "${VENV_DIR}/bin/pip" ]]; then
  "${VENV_DIR}/bin/pip" install --upgrade pip >/dev/null
  "${VENV_DIR}/bin/pip" install -r "${ROOT_DIR}/requirements.txt"
else
  python3 -m pip install --break-system-packages --upgrade pip >/dev/null
  python3 -m pip install --break-system-packages --target "${PY_TARGET_DIR}" -r "${ROOT_DIR}/requirements.txt"
fi

npm --prefix "${ROOT_DIR}" install

echo "mobile_store_intelligence skill dependencies ready (from vendored source)"
