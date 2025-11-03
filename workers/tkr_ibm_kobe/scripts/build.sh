#!/bin/bash
set -xeuo pipefail

source $(dirname $0)/backend_setup.sh ibm-kobe-dacc
gcc $(dirname $0)/../src/transpile_info.c -o build/transpile_info.o ${SQC_COMPILE_OPTIONS}
gcc $(dirname $0)/../src/submit.c -o build/submit.o ${SQC_COMPILE_OPTIONS} 

