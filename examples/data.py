from pathlib import Path
from pytket._tket.circuit import Circuit

RIKEN_WORKERS_DIR = Path(__file__).parent / ".." / "workers"


def deterministic() -> Circuit:
    circ = Circuit(2, 2)
    circ.X(1).measure_all()
    return circ
