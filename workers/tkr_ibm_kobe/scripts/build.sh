#!/bin/bash
set -euo pipefail

source "$( dirname -- "${BASH_SOURCE[0]}" )"/backend_setup.sh ibm-kobe-dacc
mkdir -p build
gcc "$( dirname -- "${BASH_SOURCE[0]}" )"/../src/transpile_info.c -o build/transpile_info.o ${SQC_COMPILE_OPTIONS}

