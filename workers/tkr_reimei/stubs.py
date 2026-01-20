"""Code generated from tkr_reimei namespace. Please do not edit."""

from typing import NamedTuple
from tierkreis.controller.data.models import TKR, OpaqueType


class get_backend_info(NamedTuple):
    device_name: TKR[str] | None = None  # noqa: F821 # fmt: skip

    @staticmethod
    def out() -> type[TKR[OpaqueType["pytket.backends.backendinfo.BackendInfo"]]]:  # noqa: F821 # fmt: skip
        return TKR[OpaqueType["pytket.backends.backendinfo.BackendInfo"]]  # noqa: F821 # fmt: skip

    @property
    def namespace(self) -> str:
        return "tkr_reimei"


class pass_from_info(NamedTuple):
    backend_info: TKR[OpaqueType["pytket.backends.backendinfo.BackendInfo"]]  # noqa: F821 # fmt: skip
    optimisation_level: TKR[int]  # noqa: F821 # fmt: skip

    @staticmethod
    def out() -> type[TKR[OpaqueType["pytket._tket.passes.BasePass"]]]:  # noqa: F821 # fmt: skip
        return TKR[OpaqueType["pytket._tket.passes.BasePass"]]  # noqa: F821 # fmt: skip

    @property
    def namespace(self) -> str:
        return "tkr_reimei"


class compile(NamedTuple):
    circuit: TKR[OpaqueType["pytket._tket.circuit.Circuit"]]  # noqa: F821 # fmt: skip
    optimisation_level: TKR[int]  # noqa: F821 # fmt: skip

    @staticmethod
    def out() -> type[TKR[OpaqueType["pytket._tket.circuit.Circuit"]]]:  # noqa: F821 # fmt: skip
        return TKR[OpaqueType["pytket._tket.circuit.Circuit"]]  # noqa: F821 # fmt: skip

    @property
    def namespace(self) -> str:
        return "tkr_reimei"


class compile_offline(NamedTuple):
    circuit: TKR[OpaqueType["pytket._tket.circuit.Circuit"]]  # noqa: F821 # fmt: skip
    optimisation_level: TKR[int] | None = None  # noqa: F821 # fmt: skip

    @staticmethod
    def out() -> type[TKR[OpaqueType["pytket._tket.circuit.Circuit"]]]:  # noqa: F821 # fmt: skip
        return TKR[OpaqueType["pytket._tket.circuit.Circuit"]]  # noqa: F821 # fmt: skip

    @property
    def namespace(self) -> str:
        return "tkr_reimei"


class sqcsub_submit_circuits(NamedTuple):
    circuits: TKR[list[OpaqueType["pytket._tket.circuit.Circuit"]]]  # noqa: F821 # fmt: skip
    n_shots: TKR[int]  # noqa: F821 # fmt: skip
    simulate: TKR[bool] | None = None  # noqa: F821 # fmt: skip

    @staticmethod
    def out() -> type[TKR[list[dict[str, list[str]]]]]:  # noqa: F821 # fmt: skip
        return TKR[list[dict[str, list[str]]]]  # noqa: F821 # fmt: skip

    @property
    def namespace(self) -> str:
        return "tkr_reimei"


class sqcsub_submit_circuit(NamedTuple):
    circuit: TKR[OpaqueType["pytket._tket.circuit.Circuit"]]  # noqa: F821 # fmt: skip
    n_shots: TKR[int]  # noqa: F821 # fmt: skip
    simulate: TKR[bool] | None = None  # noqa: F821 # fmt: skip

    @staticmethod
    def out() -> type[TKR[dict[str, list[str]]]]:  # noqa: F821 # fmt: skip
        return TKR[dict[str, list[str]]]  # noqa: F821 # fmt: skip

    @property
    def namespace(self) -> str:
        return "tkr_reimei"


class sqcsub_submit_batched(NamedTuple):
    circuit: TKR[OpaqueType["pytket._tket.circuit.Circuit"]]  # noqa: F821 # fmt: skip
    n_shots: TKR[int]  # noqa: F821 # fmt: skip
    batch_size: TKR[int] | None = None  # noqa: F821 # fmt: skip
    simulate: TKR[bool] | None = None  # noqa: F821 # fmt: skip

    @staticmethod
    def out() -> type[TKR[dict[str, list[str]]]]:  # noqa: F821 # fmt: skip
        return TKR[dict[str, list[str]]]  # noqa: F821 # fmt: skip

    @property
    def namespace(self) -> str:
        return "tkr_reimei"


class parse_sqcsub_output(NamedTuple):
    sqcsub_output: TKR[bytes]  # noqa: F821 # fmt: skip

    @staticmethod
    def out() -> type[TKR[dict[str, list[str]]]]:  # noqa: F821 # fmt: skip
        return TKR[dict[str, list[str]]]  # noqa: F821 # fmt: skip

    @property
    def namespace(self) -> str:
        return "tkr_reimei"


class set_up_tokens(NamedTuple):
    token_dir: TKR[str]  # noqa: F821 # fmt: skip

    @staticmethod
    def out() -> type[TKR[str]]:  # noqa: F821 # fmt: skip
        return TKR[str]  # noqa: F821 # fmt: skip

    @property
    def namespace(self) -> str:
        return "tkr_reimei"


class ensure_token(NamedTuple):
    token_dir: TKR[str]  # noqa: F821 # fmt: skip
    device_name: TKR[str]  # noqa: F821 # fmt: skip

    @staticmethod
    def out() -> type[TKR[str]]:  # noqa: F821 # fmt: skip
        return TKR[str]  # noqa: F821 # fmt: skip

    @property
    def namespace(self) -> str:
        return "tkr_reimei"
