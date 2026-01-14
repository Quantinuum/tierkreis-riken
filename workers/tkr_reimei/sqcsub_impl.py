import ast
from collections import defaultdict
import json
import logging
import re
import subprocess
from pathlib import Path
from typing import Any
from uuid import uuid4

from pytket._tket.circuit import Circuit
from pytket._tket.unit_id import Bit
from pytket.backends.backendresult import BackendResult
from pytket.utils.outcomearray import OutcomeArray
from pytket.qasm.qasm import circuit_to_qasm

logger = logging.getLogger(__name__)


def run_sqcsub(circuit: Circuit, n_shots: int, simulate: bool) -> str:
    device_name = "reimei-simulator" if simulate else "reimei"
    # Scratch directory.
    name = f"{uuid4()}"
    dname = Path().home() / "_scr" / name
    dname.mkdir(parents=True, exist_ok=True)
    # Scratch files.
    in_file = dname / "circ.in"
    result_file = dname / "result.txt"
    log_file = dname / "result.out"
    n_qubits = circuit.n_qubits

    # Write input circuit to file
    circuit_to_qasm(circuit, str(in_file))

    # Generate a command
    args = [
        f"source /vol0300/share/ra010014/jhpcq/x86/scripts/setenv-sqcsub.sh {device_name}",
        "&&",
        "sqcsub",
    ]
    args.extend(["--nqubits", str(n_qubits)])
    args.extend(["--nshots", str(n_shots)])
    args.extend(["--ifile", str(in_file)])
    args.extend(["--iformat", "qasm"])
    args.extend(["--ofile", str(result_file)])
    args.extend(["--oformat", "raw"])
    args.extend(["--qpu", device_name])

    cmd = " ".join(args)
    with open(log_file, "w") as fh:
        print(cmd, file=fh)
        try:
            subprocess.check_call(
                cmd,
                shell=True,
                stderr=fh,
                stdout=fh,
            )
        except subprocess.CalledProcessError as e:
            with open(log_file) as fh:
                logger.error(fh.read())
            raise e

    return str(result_file)


def parse_qsubmit(input_str: str) -> BackendResult:
    blocks = re.findall(r"\{\s*\n(.*?)\n\s*\}", input_str, re.DOTALL)
    processed_data = [_parse_block(block) for block in blocks]
    readouts, all_bits_configs = zip(*processed_data)
    if len(set(all_bits_configs)) != 1:
        raise ValueError("Inconsistent bit configurations found in results.")
    return BackendResult(
        shots=OutcomeArray.from_readouts(readouts), c_bits=all_bits_configs[0]
    )


def _parse_block(block: str) -> tuple[list[int], tuple[Bit, ...]]:
    bit_register, bits = [], []
    for line in block.splitlines():
        regname, bits_str = map(str.strip, line.split(":", 1))
        bits += [int(i) for i in ast.literal_eval(bits_str)][::-1]
        bit_register += [Bit(regname, i) for i in range(len(bits))]
        if not bit_register:
            return [], ()
    sorted_pairs = sorted(zip(bits, bit_register), key=lambda pair: str(pair[1]))
    sorted_readout, sorted_bits = zip(*sorted_pairs)
    return list(sorted_readout), sorted_bits


def parse_qsubmit_to_dict(input_str: str) -> dict[str, list[str]]:
    blocks: list[str] = re.findall(r"\{\s*\n(.*?)\n\s*\}", input_str, re.DOTALL)
    results: dict[str, list[str]] = defaultdict(list)
    for block in blocks:
        for line in block.splitlines():
            register, bits_str = map(str.strip, line.split(":", 1))
            results[register].append(bits_str.strip('"')[::-1])
    return dict(results)
