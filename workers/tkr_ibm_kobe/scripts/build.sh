#!/usr/bin/env bash
DIR=$( dirname "${BASH_SOURCE[0]}" )
source $DIR/backend_setup.sh ibm-kobe-dacc

gcc $DIR/../tkr_sqcsub.c ${SQC_COMPILE_OPTIONS}
# gcc -c -fPIC $DIR/../src/tkr_sqcsub.c -o $DIR/../build/tkr_sqcsub.o ${SQC_COMPILE_OPTIONS}
# gcc -shared -o $DIR/../build/tkr_sqcsub.so $DIR/../build/tkr_sqcsub.o ${SQC_COMPILE_OPTIONS}
