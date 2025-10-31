from pathlib import Path
from sys import argv
from typing import NamedTuple
from uuid import UUID
from tierkreis import run_graph  # type: ignore
from tierkreis.builder import GraphBuilder
from tierkreis.controller.data.models import TKR, OpaqueType
from tierkreis.executor import UvExecutor
from tierkreis.storage import FileStorage

from workers.tkr_ibm_kobe.stubs import get_transpile_info, compile_using_info

IBMQConfig = OpaqueType["quantinuum_schemas.models.backend_config.IBMQConfig"]
QuantinuumConfig = OpaqueType[
    "quantinuum_schemas.models.backend_config.QuantinuumConfig"
]
BackendInfo = OpaqueType["pytket.backends.backendinfo.BackendInfo"]
Circuit = OpaqueType["pytket._tket.circuit.Circuit"]


class SnapshotCompileRunInputs(NamedTuple):
    circuit: TKR[Circuit]


g = GraphBuilder(SnapshotCompileRunInputs, TKR[Circuit])
info = g.task(get_transpile_info())
compiled_circuit = g.task(compile_using_info(info.config, info.props, g.inputs.circuit))
g.outputs(compiled_circuit)

if __name__ == "__main__":
    is_dev = len(argv) > 1 and argv[1] == "dev"

    print("ibm compile")
    import pytket._tket.circuit as pt

    def ghz() -> pt.Circuit:
        circ1 = pt.Circuit(2)
        circ1.H(0)
        circ1.CX(0, 1)
        circ1.measure_all()
        return circ1

    storage = FileStorage(UUID(int=200), do_cleanup=True)
    # tkr_exec = UvExecutor(PACKAGE_PATH / ".." / "tierkreis_workers", storage.logs_path)
    env = {"IS_DEV": "True"} if is_dev else {}
    exec = UvExecutor(
        Path(__file__).parent / ".." / "workers", storage.logs_path, env=env
    )

    # shell_exec = ShellExecutor(
    #     Path(__file__).parent / ".." / "workers", storage.workflow_dir
    # )
    # executor = MultipleExecutor(
    #     tkr_exec,
    #     {"riken": riken_exec, "shell": shell_exec},
    #     {"tkr_sqcsub_convert": "riken", "tkr_sqcsub": "shell"},
    # )
    print("running graph")
    run_graph(
        storage,
        exec,
        g,
        {"circuit": ghz()},
        polling_interval_seconds=1,
    )
    print("done")
