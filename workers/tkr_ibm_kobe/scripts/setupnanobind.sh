#!/usr/bin/env bash

source $(dirname $0)/backend_setup.sh ibm-kobe-dacc

# rm -rf ./build
uv run cmake -S . -B build -DPython_EXECUTABLE=./.venv/bin/python
uv run cmake --build build -DCMAKE_CXX_FLAGS="'${SQC_COMPILE_OPTIONS}'"