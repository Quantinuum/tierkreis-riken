#!/bin/bash
set -euo pipefail

. /vol0300/share/ra010014/jhpcq/x86/scripts/setenv-sqcsub.sh ibm-kobe-dacc

sqcsub --nqubits $input_nqubits_value \
    --nshots $input_nshots_value \
    --ifile $input_ifile_file \
    --iformat $input_iformat_value \
    --ofile $output_value_file \
    --oformat $input_oformat_value \
    --qpu $input_qpu_value