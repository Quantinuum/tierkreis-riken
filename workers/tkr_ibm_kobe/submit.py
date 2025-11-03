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
    with NamedTemporaryFile("r") as output_file:
        with NamedTemporaryFile("w+") as input_file:
            qasm3.dump(qiskit_circuit, input_file)  # type: ignore
            subprocess.run(
                [
                    script_path,
                    input_file.name,
                    str(circuit.n_qubits),
                    str(n_shots),
                    output_file.name,
                ]
            )
        return json.load(output_file)


if __name__ == "__main__":
    res = submit_circuit(Circuit(2), 10)
    print(res)
