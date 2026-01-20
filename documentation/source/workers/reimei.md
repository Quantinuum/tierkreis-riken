# Reimei worker

The Tierkreis worker which (directly) interacts with the Fugaku `reimei` Quantinuum backend.

## Installation

To install the worker dependencies do the following

```sh
cd workers/tkr_reimei
uv sync
```

````{warning}
Currently the package `pyqir` does not have a release candidate for the Fugaku architectures
As `pytket-qir` depends on it we offer a work-around by installing with `uv sync --extra qir`.

Use at your own risk!

To load the extension you have to overwrite pyqir imports like so:

```
from sys import argv, modules
from unittest.mock import Mock
mock = Mock()
modules["pyqir"] = mock  # pyqir is not installed on fugaku
from pytket.extensions.quantinuum.backends.quantinuum import QuantinuumBackend
```
````

## Authentication

````{important}
Accessing reimeis backend information requires authentication.
The worker uses the default mechanisms provided by the [`pytket-quantinuum`](https://docs.quantinuum.com/tket/extensions/pytket-quantinuum/#persistent-authentication-token-storage) Python package.
Run the following code before using the Quantinuum worker
```python
from pytket.extensions.quantinuum.backends.api_wrappers import QuantinuumAPI
from pytket.extensions.quantinuum.backends.credential_storage import (
    QuantinuumConfigCredentialStorage,
)
from pytket.extensions.quantinuum.backends.quantinuum import QuantinuumBackend

backend = QuantinuumBackend(
    device_name=<device_name>, #e.g. H2-1E
    api_handler=QuantinuumAPI(token_store=QuantinuumConfigCredentialStorage()),
)
backend.login()
```

````

The `BackendInfo` can be only accessed if reimei is accessible by this account.
To submit a circuit this worker uses `sqcsub` which requires the fugaku specific setup.

## Elementary tasks

The pytket worker exposes the following elementary tasks to the user:

- `get_backend_info` gets the BackendInfo object for reimei. **Requires authentication**.
- `pass_from_info` gets the default pass from an BackendInfo object.
- `compile` compiles a circuit for reimei. **Requires authentication**.
- `compile_offline` compiles a circuit for reimei using hardcoded values for the `BackendInfo`.
- `sqcsub_submit_circuits` and `sqcsub_submit_circuit` submit one/multiple circuits to reimei using `sqcsub` through python.
- `parse_sqcsub_output` parses the output of the `sqcsub` command to a dictionary mapping registers to a list of shots.

Experimental

- `sqcsub_submit_batched` Experimental. Does a checkpointed/batched submission over total shots. This function has state in `_scr/batches/batch_file.txt`.
  A cleaner way would be to do a manual loop/map in the graph itself!

## Example

```python
from pathlib import Path
from sys import argv
from uuid import UUID
from tierkreis import run_graph  # type: ignore
from tierkreis.builder import GraphBuilder
from tierkreis.controller.data.models import TKR, OpaqueType
from tierkreis.executor import UvExecutor
from tierkreis.storage import FileStorage, read_outputs  # type: ignore
from pytket.qasm.qasm import circuit_from_qasm

from workers.tkr_reimei.stubs import (
    compile_offline,
    sqcsub_submit_circuit,
)
from workflows.consts import WORKERS_DIR

Circuit = OpaqueType["pytket._tket.circuit.Circuit"]
BackendResult = OpaqueType["pytket.backends.backendresult.BackendResult"]
g = GraphBuilder(TKR[Circuit], TKR[dict[str, list[str]]])
compiled_circuit = g.task(compile_offline(g.inputs))
res = g.task(sqcsub_submit_circuit(compiled_circuit, g.const(10), g.const(True)))
g.outputs(res)

if __name__ == "__main__":
    circuit = circuit_from_qasm(Path(__file__).parent / "data" / "simple.qasm")

    storage = FileStorage(UUID(int=401), do_cleanup=True)
    env = {"IS_DEV": "True"} if len(argv) > 1 and argv[1] == "dev" else {}
    exec = UvExecutor(WORKERS_DIR, storage.logs_path, env=env)
    run_graph(storage, exec, g, circuit, polling_interval_seconds=1)
    output = read_outputs(g, storage)
    print(output)

```
