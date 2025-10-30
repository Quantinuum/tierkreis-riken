#!/usr/bin/env bash

rm -rf ./build
uv run cmake -S . -B build -DPython_EXECUTABLE=./.venv/bin/python
uv run cmake --build build