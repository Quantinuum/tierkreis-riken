#!/usr/bin/env bash

uv run g++ -O3 -Wall -shared -std=c++11 -fPIC $(python -m pybind11 --includes) tkr_sqcsub.cpp -o example$(python -m pybind11 --extension-suffix) ${SQC_COMPILE_OPTIONS}