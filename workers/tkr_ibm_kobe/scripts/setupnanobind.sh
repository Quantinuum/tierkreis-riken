#!/usr/bin/env bash

cmake -S . -B build -DPython_EXECUTABLE=./.venv/bin/python -DPYTHON_INCLUDE_DIR=$(python3.11 -c "import sysconfig; print(sysconfig.get_path('include'))")  \
    -DPYTHON_LIBRARY=$(python3.11 -c "import distutils.sysconfig as sysconfig; import os; print(os.path.join(sysconfig.get_config_var('LIBDIR'), sysconfig.get_config_var('LDLIBRARY')))") \
    -DPYTHON_EXECUTABLE:FILEPATH=`which python3.11`
cmake --build build