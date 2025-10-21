from pathlib import Path
from typing import NamedTuple
from uuid import UUID
from tierkreis import run_graph  # type: ignore
from tierkreis.builder import GraphBuilder
from tierkreis.consts import PACKAGE_PATH
from tierkreis.controller.data.models import TKR, OpaqueType
from tierkreis.pytket_worker import get_backend_info, compile_using_info
from tierkreis.executor import UvExecutor, MultipleExecutor, ShellExecutor
from tierkreis.storage import FileStorage

from workers.tkr_sqcsub_convert.stubs import SubmissionData, prepare_submission
from workers.tkr_sqcsub.stubs import submit

IBMQConfig = OpaqueType["quantinuum_schemas.models.backend_config.IBMQConfig"]
QuantinuumConfig = OpaqueType[
    "quantinuum_schemas.models.backend_config.QuantinuumConfig"
]
BackendInfo = OpaqueType["pytket.backends.backendinfo.BackendInfo"]
Circuit = OpaqueType["pytket._tket.circuit.Circuit"]


class SnapshotCompileRunInputs(NamedTuple):
    config: TKR[IBMQConfig | QuantinuumConfig]
    circuit: TKR[Circuit]


g = GraphBuilder(SnapshotCompileRunInputs, SubmissionData)
info = g.task(get_backend_info(g.inputs.config))
compiled_circuit = g.task(
    compile_using_info(
        g.inputs.circuit, info, g.inputs.config, g.const(2), g.const(100)
    )
)
data = g.task(prepare_submission(g.inputs.config, compiled_circuit))
# res = g.task(
#     submit(
#         g.const(2), g.const(100), data.qasm, g.const("qasm"), g.const("raw"), data.qpu
#     )
# )
g.outputs(data)

if __name__ == "__main__":
    import quantinuum_schemas as qs
    import pytket._tket.circuit as pt

    def ghz() -> pt.Circuit:
        circ1 = pt.Circuit(2)
        circ1.H(0)
        circ1.CX(0, 1)
        circ1.measure_all()
        return circ1

    config = qs.IBMQConfig(backend_name="ibm_pittsburgh", instance="default")
    # config = qs.QuantinuumConfig(device_name="reimei")
    storage = FileStorage(UUID(int=200), do_cleanup=True)
    tkr_exec = UvExecutor(PACKAGE_PATH / ".." / "tierkreis_workers", storage.logs_path)
    riken_exec = UvExecutor(Path(__file__).parent / ".." / "workers", storage.logs_path)
    shell_exec = ShellExecutor(
        Path(__file__).parent / ".." / "workers", storage.workflow_dir
    )
    executor = MultipleExecutor(
        tkr_exec,
        {"riken": riken_exec, "shell": shell_exec},
        {"tkr_sqcsub_convert": "riken", "tkr_sqcsub": "shell"},
    )
    run_graph(
        storage,
        executor,
        g,
        {"circuit": ghz(), "config": config},
        polling_interval_seconds=1,
    )
