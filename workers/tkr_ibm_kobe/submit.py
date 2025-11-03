import json
import os
from pathlib import Path
import subprocess
from tempfile import NamedTemporaryFile
from pytket.extensions.qiskit.qiskit_convert import tk_to_qiskit
from pytket._tket.circuit import Circuit
from qiskit import qasm3  # type: ignore


def submit_circuit(circuit: Circuit, n_shots: int) -> bytes:
    script_file = "submit_local.sh" if os.environ.get("IS_DEV") else "submit.sh"
    script_path = Path(__file__).parent / "scripts" / script_file

    qiskit_circuit = tk_to_qiskit(circuit)
    with NamedTemporaryFile("w+", delete=False) as output_file:
        with NamedTemporaryFile("w+", delete=False) as input_file:
            qasm3.dump(qiskit_circuit, input_file)  # type: ignore

            env: dict[str, str] = {
                "input_nqubits_value": str(circuit.n_qubits),
                "input_nshots_value": str(n_shots),
                "input_ifile_file": input_file.name,
                "input_iformat_value": "qasm",
                "output_value_file": output_file.name,
                "input_oformat_value": "raw",
                "input_qpu_value": "ibm-kobe-dacc",
            }
            subprocess.run([script_path], env=env)
        return json.load(output_file)


if __name__ == "__main__":

    def ghz() -> Circuit:
        circ1 = Circuit(2)
        circ1.H(0)
        circ1.CX(0, 1)
        circ1.measure_all()
        return circ1

    res = submit_circuit(ghz(), 10)
    print(res)
