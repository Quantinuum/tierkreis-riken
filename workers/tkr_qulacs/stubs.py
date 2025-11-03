"""Code generated from tkr_qulacs namespace. Please do not edit."""

from typing import Literal, NamedTuple, Sequence, TypeVar, Generic, Protocol
from types import NoneType
from tierkreis.controller.data.models import TKR, OpaqueType
from tierkreis.controller.data.types import PType, Struct



class compile(NamedTuple):
    circuits: TKR[Sequence[OpaqueType["pytket._tket.circuit.Circuit"]]]  # noqa: F821 # fmt: skip
    optimisation_level: TKR[int]  # noqa: F821 # fmt: skip

    @staticmethod
    def out() -> type[TKR[list[OpaqueType["pytket._tket.circuit.Circuit"]]]]: # noqa: F821 # fmt: skip
        return TKR[list[OpaqueType["pytket._tket.circuit.Circuit"]]] # noqa: F821 # fmt: skip

    @property
    def namespace(self) -> str:
        return "tkr_qulacs" 

class submit(NamedTuple):
    circuits: TKR[Sequence[OpaqueType["pytket._tket.circuit.Circuit"]]]  # noqa: F821 # fmt: skip
    n_shots: TKR[int]  # noqa: F821 # fmt: skip

    @staticmethod
    def out() -> type[TKR[list[OpaqueType["pytket.backends.backendresult.BackendResult"]]]]: # noqa: F821 # fmt: skip
        return TKR[list[OpaqueType["pytket.backends.backendresult.BackendResult"]]] # noqa: F821 # fmt: skip

    @property
    def namespace(self) -> str:
        return "tkr_qulacs" 
    