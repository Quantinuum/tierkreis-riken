// Copyright (C) 2025 RIKEN, Japan.

#include "sqc_api.h"
#include "sqc_ecode.h"
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

int main(int argc, char *argv[])
{
  // Initialize C-API
  sqcInitOptions *init_options = sqcMallocInitOptions();
  init_options->use_qiskit = 0;
  sqcInitialize(init_options);

  // Construct circuit
  sqcQC *qcir = sqcQuantumCircuit(1);
  // Populate config and props
  sqcIbmdTranspileInfo(qcir, SQC_RPC_SCHED_QC_TYPE_IBM_DACC);

  FILE *config_file = fopen(argv[1], "w");
  fprintf(config_file, qcir->backend_config_json);

  FILE *props_file = fopen(argv[2], "w");
  fprintf(props_file, qcir->backend_props_json);

  // End processing of C-API
  sqcDestroyQuantumCircuit(qcir);
  sqcFinalize(init_options);
  sqcFreeInitOptions(init_options);

  return 0;
}
