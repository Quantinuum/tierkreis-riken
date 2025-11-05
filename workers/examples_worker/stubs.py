"""Code generated from examples_worker namespace. Please do not edit."""

from typing import NamedTuple
from tierkreis.controller.data.models import TKR, OpaqueType


class example_circuit_list(NamedTuple):
    @staticmethod
    def out() -> type[TKR[list[OpaqueType["pytket._tket.circuit.Circuit"]]]]:  # noqa: F821 # fmt: skip
        return TKR[list[OpaqueType["pytket._tket.circuit.Circuit"]]]  # noqa: F821 # fmt: skip

    @property
    def namespace(self) -> str:
        return "examples_worker"
