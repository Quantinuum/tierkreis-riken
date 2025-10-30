#!/usr/bin/env bash

source $(dirname $0)/backend_setup.sh ibm-kobe-dacc
uv run g++ -O3 -Wall -shared -std=c++11 -fPIC tkr_sqcsub.cpp -o tkr_sqcsub$(uv run python -m pybind11 --extension-suffix) $(uv run python -m pybind11 --includes) ${SQC_COMPILE_OPTIONS}