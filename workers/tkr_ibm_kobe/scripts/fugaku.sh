#!/usr/bin/env bash
set -x
set -eou pipefail

source $(dirname $0)/backend_setup.sh ibm-kobe-dacc
uv run g++ -O3 -Wall -shared -std=c++11 -fPIC $(uv run python -m pybind11 --includes) tkr_sqcsub.cpp -o tkr_sqcsub$(uv run python -m pybind11 --extension-suffix) ${SQC_COMPILE_OPTIONS}