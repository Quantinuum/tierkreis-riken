from pathlib import Path
from sys import argv, modules
from unittest.mock import Mock

import qnexus as qnx
from impl import parse_qsubmit, run_sqcsub
from pytket._tket.circuit import Circuit
from pytket.backends.backendinfo import BackendInfo
from pytket.backends.backendresult import BackendResult
from pytket.passes import BasePass
from tierkreis import Worker
from tierkreis.exceptions import TierkreisError

worker = Worker("tkr_reimei")
BATCH_FILE = Path("_scr/batches/batch_file.txt")


@worker.task()
def qnx_login() -> int:
    # cannot return None
    try:
        qnx.login_with_credentials()
        return 0
    except Exception as e:
        print(f"Error logging in to QNX: {e}")
        return 1


@worker.task()
def get_backend_info(device_name: str = "reimei") -> BackendInfo:
    devices = list(
        filter(lambda d: d.device_name == device_name, qnx.devices.get_all())
    )
    if len(devices) != 1:
        raise TierkreisError(f"Could not find device '{device_name}'")
    return devices[0].backend_info


@worker.task()
def pass_from_info(backend_info: BackendInfo, optimisation_level: int) -> BasePass:
    mock = Mock()
    modules["pyqir"] = mock  # pyqir is not installed on fugaku
    from pytket.extensions.quantinuum.backends.quantinuum import QuantinuumBackend

    compilation_pass = QuantinuumBackend.pass_from_info(
        backend_info, optimisation_level=optimisation_level
    )
    return compilation_pass


@worker.task()
def compile(circuit: Circuit, optimisation_level: int) -> Circuit:
    mock = Mock()
    modules["pyqir"] = mock  # pyqir is not installed on fugaku
    from pytket.extensions.quantinuum.backends.quantinuum import QuantinuumBackend

    devices = list(filter(lambda d: d.device_name == "reimei", qnx.devices.get_all()))
    if len(devices) != 1:
        raise TierkreisError("Could not find device 'reimei'")
    compilation_pass = QuantinuumBackend.pass_from_info(
        devices[0].backend_info, optimisation_level=optimisation_level
    )
    compilation_pass.apply(circuit)
    return circuit


@worker.task()
def sqcsub_submit_circuits(
    circuits: list[Circuit], n_shots: int
) -> list[BackendResult]:
    results = []
    for circuit in circuits:
        result_file = run_sqcsub(circuit, n_shots)
        with open(result_file, "r") as f:
            result = parse_qsubmit(f.read())
        results.append(result)
    return results


@worker.task()
def sqcsub_submit_circuit(circuit: Circuit, n_shots: int) -> BackendResult:
    result_file = run_sqcsub(circuit, n_shots)
    with open(result_file, "r") as f:
        result = parse_qsubmit(f.read())
    return result


@worker.task()
def sqcsub_submit_batched(
    circuit: Circuit, n_shots: int, batch_size: int = 100
) -> BackendResult:
    if not BATCH_FILE.exists():
        BATCH_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(BATCH_FILE, "w+") as fh:
            fh.write("0\n")  # Use the first line to store the number of shots
        start = 0
    else:
        with open(BATCH_FILE, "r") as fh:
            start = int(fh.readline())  # First line is the number of shots
    for batch in range(start, n_shots, batch_size):
        result_file = run_sqcsub(circuit, batch_size)
        with open(BATCH_FILE, "r") as fh:
            lines = fh.readlines()
        lines[0] = f"{batch + batch_size}\n"
        with open(result_file, "r") as rf:
            lines += rf.readlines()
        with open(BATCH_FILE, "w") as fh:
            fh.writelines(lines)

    with open(BATCH_FILE, "r") as fh:
        fh.readline()  # First line is the number of shots
        return parse_qsubmit(fh.read())


@worker.task()
def parse_sqcsub_output(sqcsub_output: bytes) -> BackendResult:
    return parse_qsubmit(sqcsub_output.decode())


if __name__ == "__main__":
    worker.app(argv)
