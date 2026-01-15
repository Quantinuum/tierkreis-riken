import json
import logging
import os
from pathlib import Path
import subprocess
from tempfile import NamedTemporaryFile
from typing import NamedTuple
from qiskit_ibm_runtime.models.backend_properties import BackendProperties  # type: ignore
from qiskit_ibm_runtime.models.backend_configuration import QasmBackendConfiguration  # type: ignore
from tierkreis.models import portmapping


logger = logging.getLogger(__name__)


@portmapping
class TranspileInfo(NamedTuple):
    config: QasmBackendConfiguration
    props: BackendProperties


def get_info() -> TranspileInfo:
    script_file = (
        "transpile_info_local.sh" if os.environ.get("IS_DEV") else "transpile_info.sh"
    )
    script_path = Path(__file__).parent / "scripts" / script_file

    with NamedTemporaryFile("w+") as config_file:
        with NamedTemporaryFile("w+") as props_file:
            cmd: list[str] = [str(script_path), config_file.name, props_file.name]
            logger.info(cmd)
            subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

            config_json = json.load(config_file)
            props_json = json.load(props_file)

            return TranspileInfo(config_json, props_json)


if __name__ == "__main__":
    info = get_info()
    print(info)
