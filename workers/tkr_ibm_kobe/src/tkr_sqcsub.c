#include "sqc_api.h"
#include "sqc_ecode.h"
#include <stdlib.h>
#include <string.h>

#define MAX_QASM_LEN (1024 * 1024)

void get_transpile_info(char *props, char *config)
{
  sqcInitOptions *init_options = sqcMallocInitOptions();
  init_options->use_qiskit = 0;
  sqcInitialize(init_options);

  sqcQC *qcir = sqcQuantumCircuit(1);
  sqcIbmdTranspileInfo(qcir, SQC_RPC_SCHED_QC_TYPE_IBM_DACC);

  props = qcir->backend_config_json;
  config = qcir->backend_props_json;
  prinft("%s", props);
}

int main(int argc, char *argv[])
{
  get_transpile_info("", "");
  return 0;
}
