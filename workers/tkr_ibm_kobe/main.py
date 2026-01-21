from sys import argv
from pathlib import Path
from pytket._tket.circuit import Circuit
from pytket.extensions.qiskit.backends.ibm import IBMQBackend

from qiskit_ibm_runtime.models.backend_properties import BackendProperties  # type: ignore
from qiskit_ibm_runtime.models.backend_configuration import QasmBackendConfiguration  # type: ignore

from tierkreis import Worker

from submit import parse_results, submit_circuit
from transpile_info import TranspileInfo, get_info
from token_impl import set_up_token


worker = Worker("tkr_ibm_kobe")
TOKEN_DIR = Path.home() / ".tkr_tokens"


@worker.task()
def get_transpile_info() -> TranspileInfo:
    return get_info()


@worker.task()
def compile_using_info(
    config: QasmBackendConfiguration, props: BackendProperties, circuit: Circuit
) -> Circuit:
    base_pass = IBMQBackend.default_compilation_pass_offline(config, props)
    base_pass.apply(circuit)
    return circuit


@worker.task()
def submit(circuit: Circuit, n_shots: int) -> dict[str, list[str]]:
    """Run the given circuit with the specified number of shots on IBM Kobe.

    The keys of the returned dictionary are the classical register names.
    The values of the returned dictionary are lists of shots.
    Each shot is a string of 0s and 1s with the lower bits appearing first."""
    _ = set_up_token(TOKEN_DIR, "ibm-kobe-dacc")
    res = submit_circuit(circuit, n_shots)
    return parse_results(res)


if __name__ == "__main__":
    worker.app(argv)
