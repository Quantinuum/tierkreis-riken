"""Code generated from examples_worker namespace. Please do not edit."""

from typing import Literal, NamedTuple, Sequence, TypeVar, Generic, Protocol
from types import NoneType
from tierkreis.controller.data.models import TKR, OpaqueType
from tierkreis.controller.data.types import PType, Struct



class example_circuit_list(NamedTuple):
    

    @staticmethod
    def out() -> type[TKR[list[OpaqueType["pytket._tket.circuit.Circuit"]]]]: # noqa: F821 # fmt: skip
        return TKR[list[OpaqueType["pytket._tket.circuit.Circuit"]]] # noqa: F821 # fmt: skip

    @property
    def namespace(self) -> str:
        return "examples_worker" 
    