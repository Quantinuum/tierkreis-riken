import ctypes
import json
from sys import argv
from typing import NamedTuple
from tierkreis import Worker
from pathlib import Path
from qiskit_ibm_runtime.models.backend_properties import BackendProperties  # type: ignore
from qiskit_ibm_runtime.models.backend_configuration import QasmBackendConfiguration  # type: ignore

from pytket._tket.circuit import Circuit
from pytket.backends.backendresult import BackendResult
from pytket.extensions.qiskit.backends.ibm import IBMQBackend


worker = Worker("tkr_ibm_kobe")
c_tkr_sqcsub = ctypes.CDLL(Path(__file__).parent / "build" / "tkr_sqcsub.so")


class TranspileInformation(NamedTuple):
    config: QasmBackendConfiguration
    props: BackendProperties


# @worker.task()
def get_backend_info() -> TranspileInformation:
    print("get_backend_info")
    config_json = ctypes.c_char_p()
    props_json = ctypes.c_char_p()
    c_tkr_sqcsub.get_transpile_info(ctypes.byref(config_json), ctypes.byref(props_json))

    print(config_json.value)
    print(props_json.value)

    print("config")
    config = QasmBackendConfiguration.from_dict(json.loads(config_json.value))
    print(config.backend_name)
    print("props")
    props = BackendProperties.from_dict(json.loads(props_json.value))
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
    # worker.app(argv)
    print("start")
    get_backend_info()
    print("done")
    raise SystemExit()
