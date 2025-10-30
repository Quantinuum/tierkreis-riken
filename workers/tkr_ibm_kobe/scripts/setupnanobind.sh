#!/usr/bin/env bash

cmake -S . -B build -DPython_EXECUTABLE=./.venv/bin/python
cmake --build build -DPYTHON_ExECUTABLE=./.venv/bin/python