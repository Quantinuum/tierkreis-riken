#!/usr/bin/env bash
set -euo pipefail

source $(dirname "$0")/scripts/backend_setup.sh ibm-kobe-dacc

$(dirname "$0")/.venv/bin/python main.py $1