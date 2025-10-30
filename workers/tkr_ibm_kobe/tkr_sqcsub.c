#include "sqc_api.h"
#include "sqc_ecode.h"

#include <stdio.h>
#include <stdlib.h>

#define MAX_QASM_LEN (1024 * 1024)

void get_transpile_info()
{
    sqcInitOptions *init_options = sqcMallocInitOptions();
    init_options->use_qiskit = 0;
    sqcInitialize(init_options);

    sqcQC *qcir = sqcQuantumCircuit(1);
    sqcIbmdTranspileInfo(qcir, SQC_RPC_SCHED_QC_TYPE_IBM_DACC);

    // File *outputFile = fopen("output", "a");
    printf("%s\n", qcir->backend_config_json);

    // File *outputFile = fopen("output", "a");
    printf("%s\n", qcir->backend_props_json);
}

int main(int argc, char *argv[])
{
    get_transpile_info();

    return 0;
}
