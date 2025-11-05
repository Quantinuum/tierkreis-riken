from pathlib import Path
from pytket._tket.circuit import Circuit

RIKEN_WORKERS_DIR = Path(__file__).parent / ".." / "workers"


def ghz() -> Circuit:
    circ1 = Circuit(2)
    circ1.H(0)
    circ1.CX(0, 1)
    circ1.measure_all()
    return circ1
