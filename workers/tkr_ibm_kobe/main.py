import json
from sys import argv
from typing import NamedTuple
from tierkreis import Worker

from qiskit_ibm_runtime.models.backend_properties import BackendProperties  # type: ignore
from qiskit_ibm_runtime.models.backend_configuration import QasmBackendConfiguration  # type: ignore

from pytket._tket.circuit import Circuit
from pytket.backends.backendresult import BackendResult
from pytket.extensions.qiskit.backends.ibm import IBMQBackend

from models_ctypes import c_tkr_sqcsub

worker = Worker("tkr_ibm_kobe")


class TranspileInformation(NamedTuple):
    config: QasmBackendConfiguration
    props: BackendProperties


@worker.task()
def get_backend_info() -> TranspileInformation:
    print("get_backend_info")
    res = c_tkr_sqcsub.get_transpile_info()
    print(res)
    print(json.loads(res.configuration))
    config = QasmBackendConfiguration.from_dict(json.loads(res.configuration))
    print(config.backend_name)
    print(json.loads(res.properties))
    props = BackendProperties.from_dict(json.loads(res.properties))  # type: ignore
    print(props.backend_name)
    return TranspileInformation(config, props)


@worker.task()
def compile_using_info(info: TranspileInformation, circuit: Circuit) -> Circuit:
    base_pass = IBMQBackend.default_compilation_pass_offline(info.config, info.props)
    base_pass.apply(circuit)
    return circuit


@worker.task()
def submit(circuit: Circuit) -> BackendResult: ...


if __name__ == "__main__":
    worker.app(argv)
