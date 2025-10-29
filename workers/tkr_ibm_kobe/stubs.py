"""Code generated from tkr_ibm_kobe namespace. Please do not edit."""

from typing import NamedTuple, Protocol
from tierkreis.controller.data.models import TKR, OpaqueType
from tierkreis.controller.data.types import Struct


class TranspileInformation(Struct, Protocol):
    config: OpaqueType["qiskit_ibm_runtime.models.backend_configuration.QasmBackendConfiguration"]  # noqa: F821 # fmt: skip
    props: OpaqueType["qiskit_ibm_runtime.models.backend_properties.BackendProperties"]  # noqa: F821 # fmt: skip


class get_backend_info(NamedTuple):
    @staticmethod
    def out() -> type[TKR[TranspileInformation]]:  # noqa: F821 # fmt: skip
        return TKR[TranspileInformation]  # noqa: F821 # fmt: skip

    @property
    def namespace(self) -> str:
        return "tkr_ibm_kobe"


class compile_using_info(NamedTuple):
    info: TKR[TranspileInformation]  # noqa: F821 # fmt: skip
    circuit: TKR[OpaqueType["pytket._tket.circuit.Circuit"]]  # noqa: F821 # fmt: skip

    @staticmethod
    def out() -> type[TKR[OpaqueType["pytket._tket.circuit.Circuit"]]]:  # noqa: F821 # fmt: skip
        return TKR[OpaqueType["pytket._tket.circuit.Circuit"]]  # noqa: F821 # fmt: skip

    @property
    def namespace(self) -> str:
        return "tkr_ibm_kobe"


class submit(NamedTuple):
    circuit: TKR[OpaqueType["pytket._tket.circuit.Circuit"]]  # noqa: F821 # fmt: skip

    @staticmethod
    def out() -> type[TKR[OpaqueType["pytket.backends.backendresult.BackendResult"]]]:  # noqa: F821 # fmt: skip
        return TKR[OpaqueType["pytket.backends.backendresult.BackendResult"]]  # noqa: F821 # fmt: skip

    @property
    def namespace(self) -> str:
        return "tkr_ibm_kobe"
