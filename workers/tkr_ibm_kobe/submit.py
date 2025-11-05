import json
import os
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory
from typing import Any

from pytket._tket.circuit import Circuit
from pytket.backends.backendresult import BackendResult
from pytket.extensions.qiskit.qiskit_convert import tk_to_qiskit
from pytket.utils.outcomearray import OutcomeArray
from qiskit import qasm3  # type: ignore
from qiskit.primitives.containers import SamplerPubResult, BitArray, PrimitiveResult, PubResult  # type: ignore
from qiskit_ibm_runtime import RuntimeDecoder


def submit_circuit(circuit: Circuit, n_shots: int) -> bytes:
    script_file = "submit_local.sh" if os.environ.get("IS_DEV") else "submit.sh"
    script_path = Path(__file__).parent / "scripts" / script_file

    qiskit_circuit = tk_to_qiskit(circuit)
    with TemporaryDirectory(delete=False) as dirname:
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
        subprocess.run([script_path], env=env)

        with open(output_file_name) as fh:
            return json.load(fh)


def parse_results(res: Any) -> BackendResult:
    print(res["results"][0]["data"]["c"]["samples"])
    ba = BitArray.from_samples(res["results"][0]["data"]["c"]["samples"])
    print(ba.get_counts())
    print(ba.get_bitstrings())
    print(ba.get_int_counts())
    brs = [
        backend_result_from_bitstrings(ba["samples"])
        for _, ba in res["results"][0]["data"].items()
    ]
    assert len(brs) == 1
    return brs[0]


if __name__ == "__main__":

    circ = Circuit(2, 2)
    circ.X(1).measure_all()

    res = submit_circuit(circ, 10)
    parse_results(res)
