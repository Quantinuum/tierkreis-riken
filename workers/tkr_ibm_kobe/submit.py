import json
import os
from pathlib import Path
import subprocess
from tempfile import NamedTemporaryFile
from pytket.extensions.qiskit.qiskit_convert import tk_to_qiskit
from pytket._tket.circuit import Circuit
from qiskit import qasm3  # type: ignore


def submit_circuit(circuit: Circuit, n_shots: int) -> bytes:
    command = [".", "/vol0300/share/ra010014/jhpcq/x86/scripts/setenv-sqcsub.sh"]
    command.append("ibm-kobe-dacc")
    command.extend(["&&", "sqcsub"])
    if os.environ.get("IS_DEV"):
        command = [str(Path(__file__).parent / "scripts" / "submit_local.sh")]

    command.extend(["--nqubits", str(circuit.n_qubits)])
    command.extend(["--nshots", str(n_shots)])
    command.extend(["--iformat", "qasm"])
    command.extend(["--oformat", "raw"])
    command.extend(["--qpu", "ibm_kobe_dacc"])

    qiskit_circuit = tk_to_qiskit(circuit)
    with NamedTemporaryFile("w+", delete=False) as output_file:
        with NamedTemporaryFile("w+", delete=False) as input_file:
            command.extend(["--ifile", input_file.name])
            command.extend(["--ofile", output_file.name])
            qasm3.dump(qiskit_circuit, input_file)  # type: ignore
            subprocess.run(command)
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
