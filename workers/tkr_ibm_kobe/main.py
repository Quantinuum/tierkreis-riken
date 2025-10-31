from sys import argv
from pytket._tket.circuit import Circuit
from pytket.extensions.qiskit.backends.ibm import IBMQBackend
from tierkreis import Worker
from qiskit_ibm_runtime.models.backend_properties import BackendProperties  # type: ignore
from qiskit_ibm_runtime.models.backend_configuration import QasmBackendConfiguration  # type: ignore

from transpile_info import TranspileInfo, get_info


worker = Worker("tkr_ibm_kobe")


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


if __name__ == "__main__":
    worker.app(argv)
