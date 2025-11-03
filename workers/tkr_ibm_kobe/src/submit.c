// Copyright (C) 2025 RIKEN, Japan.

// Sample program using SQC C-API and a OpenQASM file.

#include "sqc_api.h"
#include "sqc_ecode.h"
#include <stdlib.h>
#include <string.h>

#define MAX_QASM_LEN (1024 * 1024)

int main(int argc, char *argv[])
{
  char *inputPath = argv[1];
  int nQubits = atoi(argv[2]);
  int nShots = atoi(argv[3]);
  char *outputPath = argv[4];

  printf("%s %d %d %s", inputPath, nQubits, nShots, outputPath);

  // Initialize C-API
  sqcInitOptions *init_options = sqcMallocInitOptions();
  init_options->use_qiskit = 0;
  sqcInitialize(init_options);

  // Read OpenQASM file
  sqcQC *qcir = sqcQuantumCircuit(nQubits);
  qcir->qasm = (char *)calloc(sizeof(char), MAX_QASM_LEN);
  sqcReadQasmFile(&(qcir->qasm), inputPath, MAX_QASM_LEN);

  // Set run option
  sqcRunOptions *run_options = (sqcRunOptions *)malloc(sizeof(sqcRunOptions));
  sqcInitializeRunOpt(run_options);
  run_options->nshots = nShots;
  run_options->qubits = nQubits;
  run_options->outFormat = SQC_OUT_RAW;

  // Run quantum circuit
  sqcOut *result_out;
  result_out = (sqcOut *)malloc(sizeof(sqcOut));
  int error_code = sqcQCRun(qcir, SQC_RPC_SCHED_QC_TYPE_QTM_SIM_GRPC, *run_options, result_out);

  // Show error_code
  printf("error_code:%d\n", error_code);

  // Write result to file
  if (error_code == SQC_RESULT_OK)
  {
    FILE *file;
    file = fopen(outputPath, "w");
    if (file == NULL)
    {
      printf("Error opening file.\n");
    }
    else
    {
      sqcPrintQCResult(file, result_out, run_options->outFormat);
      fclose(file);
    }
  }

  // End processing of C-API
  sqcFreeOut(result_out, run_options->outFormat);
  free(run_options);
  sqcDestroyQuantumCircuit(qcir);
  sqcFinalize(init_options);
  sqcFreeInitOptions(init_options);

  return 0;
}
