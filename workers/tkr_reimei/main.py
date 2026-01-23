from pathlib import Path
from sys import argv

from pytket._tket.circuit import Circuit
from pytket.backends.backendinfo import BackendInfo
from pytket.architecture import FullyConnected
from pytket.passes import BasePass
from tierkreis import Worker

from sqcsub_impl import parse_qsubmit_to_dict, run_sqcsub
from qnexus_impl import qnexus_quantinuum_device_by_name, REIMEI_OPS
from token_impl import (
    set_up_token,
)
from pyqir import mock_pyqir

worker = Worker("tkr_reimei")
BATCH_FILE = Path("_scr/batches/batch_file.txt")
TOKEN_DIR = Path.home() / ".tkr_tokens"


@worker.task()
def get_backend_info(device_name: str = "reimei") -> BackendInfo:
    device = qnexus_quantinuum_device_by_name(device_name)
    return device.backend_info


@worker.task()
def pass_from_info(backend_info: BackendInfo, optimisation_level: int) -> BasePass:
    mock_pyqir()
    from pytket.extensions.quantinuum.backends.quantinuum import QuantinuumBackend

    compilation_pass = QuantinuumBackend.pass_from_info(
        backend_info, optimisation_level=optimisation_level
    )
    return compilation_pass


@worker.task()
def compile(circuit: Circuit, optimisation_level: int) -> Circuit:
    mock_pyqir()
    from pytket.extensions.quantinuum.backends.quantinuum import QuantinuumBackend

    device = qnexus_quantinuum_device_by_name("reimei")
    compilation_pass = QuantinuumBackend.pass_from_info(
        device.backend_info, optimisation_level=optimisation_level
    )
    compilation_pass.apply(circuit)
    return circuit


@worker.task()
def compile_offline(
    circuit: Circuit,
    optimisation_level: int = 2,
) -> Circuit:
    """Gets a compiled circuit for reimei using MAGIC values for backend config.

    :param circuit: The original circuit to compile.
    :type circuit: Circuit
    :param optimisation_level: The optimization level for the compilation, defaults to 2
    :type optimisation_level: int, optional
    :return: The compiled circuit.
    :rtype: Circuit
    """
    mock_pyqir()

    from pytket.extensions.quantinuum.backends.quantinuum import QuantinuumBackend

    compilation_pass = QuantinuumBackend.pass_from_info(
        BackendInfo(
            name="EmulatorEnabledQuantinuumBackend",
            device_name="reimei",
            architecture=FullyConnected(20),
            version="0.54.0",
            gate_set=REIMEI_OPS,
        ),
        optimisation_level=optimisation_level,
    )
    compilation_pass.apply(circuit)
    return circuit


@worker.task()
def sqcsub_submit_circuits(
    circuits: list[Circuit], n_shots: int, simulate: bool = False
) -> list[dict[str, list[str]]]:
    results = []
    _ = set_up_token(TOKEN_DIR, "reimei-simulator" if simulate else "reimei")
    for circuit in circuits:
        result_file = run_sqcsub(circuit, n_shots, simulate)
        with open(result_file, "r") as f:
            result = parse_qsubmit_to_dict(f.read())
        results.append(result)
    return results


@worker.task()
def sqcsub_submit_circuit(
    circuit: Circuit, n_shots: int, simulate: bool = False
) -> dict[str, list[str]]:
    _ = set_up_token(TOKEN_DIR, "reimei-simulator" if simulate else "reimei")
    result_file = run_sqcsub(circuit, n_shots, simulate)
    with open(result_file, "r") as f:
        result = parse_qsubmit_to_dict(f.read())
    return result


@worker.task()
def sqcsub_submit_batched(
    circuit: Circuit, n_shots: int, batch_size: int = 100, simulate: bool = False
) -> dict[str, list[str]]:
    _ = set_up_token(TOKEN_DIR, "reimei-simulator" if simulate else "reimei")
    if not BATCH_FILE.exists():
        BATCH_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(BATCH_FILE, "w+") as fh:
            fh.write("0\n")  # Use the first line to store the number of shots
        start = 0
    else:
        with open(BATCH_FILE, "r") as fh:
            start = int(fh.readline())  # First line is the number of shots
    for batch in range(start, n_shots, batch_size):
        result_file = run_sqcsub(circuit, batch_size, simulate)
        with open(BATCH_FILE, "r") as fh:
            lines = fh.readlines()
        lines[0] = f"{batch + batch_size}\n"
        with open(result_file, "r") as rf:
            lines += rf.readlines()
        with open(BATCH_FILE, "w") as fh:
            fh.writelines(lines)

    with open(BATCH_FILE, "r") as fh:
        fh.readline()  # First line is the number of shots
        return parse_qsubmit_to_dict(fh.read())


@worker.task()
def parse_sqcsub_output(sqcsub_output: bytes) -> dict[str, list[str]]:
    return parse_qsubmit_to_dict(sqcsub_output.decode())


if __name__ == "__main__":
    worker.app(argv)
