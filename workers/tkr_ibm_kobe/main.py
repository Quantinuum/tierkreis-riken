import ctypes
import ctypes.util
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


class TranspileInformation(NamedTuple):
    config: QasmBackendConfiguration
    props: BackendProperties


# @worker.task()
def get_backend_info() -> TranspileInformation:
    c_tkr_sqcsub = ctypes.CDLL(Path(__file__).parent / "build" / "tkr_sqcsub.so")
    del c_tkr_sqcsub
    #c_tkr_sqcsub.get_transpile_info.restype = None
    #libc = ctypes.CDLL(ctypes.util.find_library('c'))

    #config_json = ctypes.c_char_p()
    #props_json = ctypes.c_char_p()
    #c_tkr_sqcsub.get_transpile_info(ctypes.byref(config_json), ctypes.byref(props_json))

    #config = QasmBackendConfiguration.from_dict(json.loads(config_json.value))
    #props = BackendProperties.from_dict(json.loads(props_json.value))

    #libc.free(config_json)
    #libc.free(props_json)

    #del libc
    #del c_tkr_sqcsub
    
    return TranspileInformation("", "")


@worker.task()
def compile_using_info(info: TranspileInformation, circuit: Circuit) -> Circuit:
    base_pass = IBMQBackend.default_compilation_pass_offline(info.config, info.props)
    base_pass.apply(circuit)
    return circuit


@worker.task()
def submit(circuit: Circuit) -> BackendResult: ...


#if __name__ == "__main__":
    # worker.app(argv)
print("start")
info = get_backend_info()
print(info)
print("done")

import threading
print(threading.enumerate())

