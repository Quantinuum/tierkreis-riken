import json
import os
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory
from pytket.extensions.qiskit.qiskit_convert import tk_to_qiskit
from pytket._tket.circuit import Circuit
from qiskit import qasm3  # type: ignore


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
        print(output_file_name)

        with open(output_file_name) as fh:
            res = fh.read().encode()
            print(res)
            return res


if __name__ == "__main__":

    def ghz() -> Circuit:
        circ1 = Circuit(2)
        circ1.H(0)
        circ1.CX(0, 1)
        circ1.measure_all()
        return circ1

    res = submit_circuit(ghz(), 10)
    print(res)
