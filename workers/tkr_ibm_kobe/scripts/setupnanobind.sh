#!/usr/bin/env bash

cmake -S . -B build -DPython_EXECUTABLE=./.venv/bin/python -DPYTHON_INCLUDE_DIR=$(python3.11 -c "import sysconfig; print(sysconfig.get_path('include'))")  \
    -DPYTHON_LIBRARY=$(python3.11 -c "import sysconfig; print(sysconfig.get_config_var('LIBDIR'))")
cmake --build build