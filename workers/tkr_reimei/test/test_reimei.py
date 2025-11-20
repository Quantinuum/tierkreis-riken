from pathlib import Path
from pytket._tket.unit_id import Bit
from pytket.backends.backendresult import BackendResult
from pytket.utils.outcomearray import OutcomeArray

from workers.tkr_reimei.sqcsub_impl import parse_qsubmit_to_dict, parse_qsubmit


def test_backend_result_conversion() -> None:
    original_result = BackendResult(
        shots=OutcomeArray.from_readouts([[1, 1, 0] for _ in range(10)]),
        c_bits=[Bit("c", 0), Bit("d", 0), Bit("d", 1)],
    )
    with open(Path(__file__).parent / "results.txt", "r") as fh:
        result = parse_qsubmit(fh.read())
    assert original_result.get_shots().tolist() == result.get_shots().tolist()


def test_parse_to_dict() -> None:
    with open(Path(__file__).parent / "results.txt", "r") as fh:
        result = parse_qsubmit_to_dict(fh.read())
    assert result == {"c": ["1"] * 10, "d": ["10"] * 10}
