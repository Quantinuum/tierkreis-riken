# Quantum submissions using sqcsub

We can use the `sqcsub` worker to run tasks on a QPU.

## Example graph

```python
from typing import NamedTuple
from uuid import UUID
from tierkreis import run_graph
from tierkreis.builder import GraphBuilder
from tierkreis.executor import ShellExecutor
from tierkreis.models import TKR
from tierkreis.storage import FileStorage, read_outputs
from workers.tkr_sqcsub.stubs import submit

from workers.consts import WORKERS_DIR


class SqcsubInput(NamedTuple):
    nqubits: TKR[int]
    nshots: TKR[int]
    iformat: TKR[str]
    oformat: TKR[str]
    input: TKR[bytes]
    qpu: TKR[str]


g = GraphBuilder(SqcsubInput, TKR[bytes])
res = g.task(
    submit(
        g.inputs.nqubits,
        g.inputs.nshots,
        g.inputs.input,
        g.inputs.iformat,
        g.inputs.oformat,
        g.inputs.qpu,
    )
)
g.outputs(res)


storage = FileStorage(UUID(int=106), do_cleanup=True)
executor = ShellExecutor(WORKERS_DIR, storage.workflow_dir)
TEST_QASM = """
OPENQASM 2.0;
include "hqslib1.inc";

qreg q[2];
creg c[2];
U1q(0.20000000000000012*pi,0.0*pi) q[0];
U1q(0.5*pi,0.5*pi) q[1];
RZZ(0.5*pi) q[0],q[1];
measure q[0] -> c[0];
U1q(0.5*pi,0.0*pi) q[1];
measure q[1] -> c[1];
"""

run_graph(
    storage,
    executor,
    g.get_data(),
    {
        "nqubits": 10,
        "nshots": 30,
        "iformat": "qasm",
        "input": TEST_QASM,
        "oformat": "raw",
        "qpu": "reimei-simulator",
    },
)
read_outputs(g.get_data(), storage)

```
