from pytket._tket.circuit import Circuit
from pytket.extensions.qiskit.backends.ibm import IBMQBackend
from tierkreis import Worker

from tkr_sqcsub import TranspileInfo, get_transpile_info_inner


worker = Worker("tkr_ibm_kobe")


@worker.task()
def get_transpile_info() -> TranspileInfo:
    return get_transpile_info_inner()


@worker.task()
def compile_using_info(info: TranspileInfo, circuit: Circuit) -> Circuit:
    base_pass = IBMQBackend.default_compilation_pass_offline(info.config, info.props)
    base_pass.apply(circuit)
    return circuit
