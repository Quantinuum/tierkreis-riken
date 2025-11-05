"""Code generated from tkr_ibm_kobe namespace. Please do not edit."""

from typing import NamedTuple
from tierkreis.controller.data.models import TKR, OpaqueType


class TranspileInfo(NamedTuple):
    config: TKR[OpaqueType["qiskit_ibm_runtime.models.backend_configuration.QasmBackendConfiguration"]]  # noqa: F821 # fmt: skip
    props: TKR[OpaqueType["qiskit_ibm_runtime.models.backend_properties.BackendProperties"]]  # noqa: F821 # fmt: skip


class get_transpile_info(NamedTuple):
    @staticmethod
    def out() -> type[TranspileInfo]:  # noqa: F821 # fmt: skip
        return TranspileInfo  # noqa: F821 # fmt: skip

    @property
    def namespace(self) -> str:
        return "tkr_ibm_kobe"


class compile_using_info(NamedTuple):
    config: TKR[OpaqueType["qiskit_ibm_runtime.models.backend_configuration.QasmBackendConfiguration"]]  # noqa: F821 # fmt: skip
    props: TKR[OpaqueType["qiskit_ibm_runtime.models.backend_properties.BackendProperties"]]  # noqa: F821 # fmt: skip
    circuit: TKR[OpaqueType["pytket._tket.circuit.Circuit"]]  # noqa: F821 # fmt: skip

    @staticmethod
    def out() -> type[TKR[OpaqueType["pytket._tket.circuit.Circuit"]]]:  # noqa: F821 # fmt: skip
        return TKR[OpaqueType["pytket._tket.circuit.Circuit"]]  # noqa: F821 # fmt: skip

    @property
    def namespace(self) -> str:
        return "tkr_ibm_kobe"


class submit(NamedTuple):
    circuit: TKR[OpaqueType["pytket._tket.circuit.Circuit"]]  # noqa: F821 # fmt: skip
    n_shots: TKR[int]  # noqa: F821 # fmt: skip

    @staticmethod
    def out() -> type[TKR[OpaqueType["pytket.backends.backendresult.BackendResult"]]]:  # noqa: F821 # fmt: skip
        return TKR[OpaqueType["pytket.backends.backendresult.BackendResult"]]  # noqa: F821 # fmt: skip

    @property
    def namespace(self) -> str:
        return "tkr_ibm_kobe"
