from pathlib import Path
from sys import argv
from typing import NamedTuple
from uuid import UUID
from tierkreis import run_graph  # type: ignore
from tierkreis.builder import GraphBuilder
from tierkreis.controller.data.models import TKR, OpaqueType
from tierkreis.executor import UvExecutor
from tierkreis.storage import FileStorage, read_outputs  # type: ignore
from pytket.qasm.qasm import circuit_from_qasm

from data import RIKEN_WORKERS_DIR
from workers.tkr_ibm_kobe.stubs import get_transpile_info, compile_using_info, submit
from workers.tkr_reimei.stubs import (
    compile_offline,
    sqcsub_submit_circuit as submit_reimei,
)

Circuit = OpaqueType["pytket._tket.circuit.Circuit"]
BackendResult = OpaqueType["pytket.backends.backendresult.BackendResult"]


class Input(NamedTuple):
    circuit: TKR[Circuit]
    order: TKR[str]


class Output(NamedTuple):
    result: TKR[dict[str, list[str]]]
    order: TKR[str]


def ibm_graph() -> GraphBuilder[Input, Output]:
    g = GraphBuilder(Input, Output)
    info = g.task(get_transpile_info())
    compiled_circuit = g.task(
        compile_using_info(info.config, info.props, g.inputs.circuit)
    )
    res = g.task(submit(compiled_circuit, g.const(10)))
    g.outputs(Output(res, g.inputs.order))
    return g


def reimei_simulator_graph() -> GraphBuilder[Input, Output]:
    g = GraphBuilder(Input, Output)
    compiled_circuit = g.task(compile_offline(g.inputs.circuit))
    res = g.task(
        submit_reimei(compiled_circuit, g.const(10), g.const(True))
    )  # simulate=TRUE
    g.outputs(Output(res, g.inputs.order))
    return g


class FullOutput(NamedTuple):
    reimei: TKR[dict[str, list[str]]]
    ibm: TKR[dict[str, list[str]]]


def full_graph() -> GraphBuilder[TKR[Circuit], FullOutput]:
    g = GraphBuilder(TKR[Circuit], FullOutput)
    output_ibm = g.eval(ibm_graph(), Input(g.inputs, g.const("")))
    output_reimei = g.eval(reimei_simulator_graph(), Input(g.inputs, output_ibm.order))
    g.outputs(FullOutput(output_ibm.result, output_reimei.result))
    return g


if __name__ == "__main__":
    circuit = circuit_from_qasm(Path(__file__).parent / "data" / "simple.qasm")

    storage = FileStorage(UUID(int=201), do_cleanup=True)
    env = {"IS_DEV": "True"} if len(argv) > 1 and argv[1] == "dev" else {}
    exec = UvExecutor(RIKEN_WORKERS_DIR, storage.logs_path, env=env)
    graph = full_graph()
    run_graph(storage, exec, graph, circuit, polling_interval_seconds=1)
    output = read_outputs(graph, storage)
    print(output)
