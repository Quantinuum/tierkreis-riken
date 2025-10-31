import json
import os
from pathlib import Path
import subprocess
from tempfile import NamedTemporaryFile
from typing import NamedTuple
from qiskit_ibm_runtime.models.backend_properties import BackendProperties  # type: ignore
from qiskit_ibm_runtime.models.backend_configuration import QasmBackendConfiguration  # type: ignore


class TranspileInfo(NamedTuple):
    config: QasmBackendConfiguration
    props: BackendProperties


def get_transpile_info_inner() -> TranspileInfo:
    script_file = "run_local.sh" if os.environ.get("IS_DEV") else "run.sh"
    script_path = Path(__file__).parent / "scripts" / script_file

    with NamedTemporaryFile("w+") as config_file:
        with NamedTemporaryFile("w+") as props_file:
            subprocess.run([script_path, config_file.name, props_file.name])

            config_json = json.load(config_file)
            props_json = json.load(props_file)

    config = QasmBackendConfiguration.from_dict(config_json)
    props = BackendProperties.from_dict(props_json)  # type: ignore

    return TranspileInfo(config, props)


if __name__ == "__main__":
    info = get_transpile_info_inner()
    print(info)
