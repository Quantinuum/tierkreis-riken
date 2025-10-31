#!/bin/bash
set -xeuo pipefail

source $(dirname $0)/backend_setup.sh ibm-kobe-dacc
$(dirname $0)/../build/transpile_info.o $1 $2

