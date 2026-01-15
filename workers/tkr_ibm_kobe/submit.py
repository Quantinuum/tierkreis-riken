import json
import os
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory
from typing import Any

from pytket._tket.circuit import Circuit
from pytket.extensions.qiskit.qiskit_convert import tk_to_qiskit
from qiskit import qasm3  # type: ignore
from qiskit.primitives.containers import BitArray  # type: ignore


def submit_circuit(circuit: Circuit, n_shots: int) -> bytes:
    script_file = "submit_local.sh" if os.environ.get("IS_DEV") else "submit.sh"
    script_path = Path(__file__).parent / "scripts" / script_file

    qiskit_circuit = tk_to_qiskit(circuit)
    with TemporaryDirectory() as dirname:
        input_file_name = f"{dirname}/input"
        output_file_name = f"{dirname}/output"
        Path(output_file_name).touch()
        with open(input_file_name, "w+") as fh:
            qasm3.dump(qiskit_circuit, fh)  # type: ignore

        env: dict[str, str] = {
            "input_nqubits_value": str(circuit.n_qubits),
            "input_nshots_value": str(n_shots),
            "input_ifile_file": input_file_name,
            "input_iformat_value": "qasm",
            "output_value_file": output_file_name,
            "input_oformat_value": "raw",
            "input_qpu_value": "ibm-kobe-dacc",
        }
        subprocess.run(
            [script_path], env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )

        with open(output_file_name) as fh:
            return json.load(fh)


def parse_results(res: Any) -> dict[str, list[str]]:
    raw_result = res["results"][0]["data"]
    results: dict[str, list[str]] = {}

    for k, v in raw_result.items():
        ba = BitArray.from_samples(v["samples"])
        bitstrings = ba.get_bitstrings()
        bitstrings = [x[::-1] for x in bitstrings]
        results[k] = bitstrings

    return results


if __name__ == "__main__":
    circ = Circuit(2, 2)
    circ.X(1).measure_all()

    res = submit_circuit(circ, 10)
    shots = parse_results(res)
    print(shots)
