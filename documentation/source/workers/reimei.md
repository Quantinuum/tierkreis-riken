# Reimei worker

The Tierkreis worker which (directly) interacts with the Fugaku `reimei` Quantinuum backend.

## Installation

To install the worker dependencies do the following

```sh
cd workers/tkr_reimei
uv sync
```

> [!WARNING]
> Currently the package `pyqir` does not have a release candidate for the Fugaku architectures
> As `pytket-qir` depends on it we offer a work-around by installing with `uv sync --extra qir`.
>
> Use at your own risk!
>
> To load the extension you have to overwrite pyqir imports like so:
>
> ```
> from sys import argv, modules
> from unittest.mock import Mock
> mock = Mock()
> modules["pyqir"] = mock  # pyqir is not installed on fugaku
> from pytket.extensions.quantinuum.backends.quantinuum import QuantinuumBackend
> ```

## Authentication

To access the reimei backend information the worker uses the default mechanisms provided by the `qnexus` Python package.

```bash
uv run python -c "from qnexus.client.auth import login; login()"
```

Compilation can be only accessed if reimei is accessible by this account.

## Elementary tasks

The pytket worker exposes the following elementary tasks to the user:

- `qnx_login` terminal based login for Quantinuum Nexus
- `get_backend_info` gets the BackendInfo object for reimei
- `pass_from_info` gets the default pass from an BackendInfo object
- `compile` compiles a circuit for reimei
- `sqcsub_submit_circuits` and `sqcsub_submit_circuit` submit one/multiple circuits to reimei using `sqcsub` through python
- `parse_sqcsub_output` parses the output of the `sqcsub` command to a BackendResult.

Experimental

- `sqcsub_submit_batched` Experimental. Does a checkpointed/batched submission over total shots. This function has state in `_scr/batches/batch_file.txt`.
  A cleaner way would be to do a manual loop/map in the graph itself!

## Example

```python
from uuid import UUID
from tierkreis import run_graph  # type: ignore
from tierkreis.builder import GraphBuilder
from tierkreis.controller.data.models import TKR, OpaqueType
from tierkreis.executor import UvExecutor
from tierkreis.storage import FileStorage, read_outputs  # type: ignore

from data import RIKEN_WORKERS_DIR, ghz
from workers.tkr_reimei.stubs import compile, sqcsub_submit_circuit

Circuit = OpaqueType["pytket._tket.circuit.Circuit"]
BackendResult = OpaqueType["pytket.backends.backendresult.BackendResult"]
g = GraphBuilder(TKR[Circuit], TKR[BackendResult])
compiled_circuit = g.task(compile(g.inputs, g.const(3)))
results = g.task(sqcsub_submit_circuit(compiled_circuit, g.const(1024)))
g.outputs()

if __name__ == "__main__":
    storage = FileStorage(UUID(int=201), do_cleanup=True)
    exec = UvExecutor(RIKEN_WORKERS_DIR, storage.logs_path)
    run_graph(storage, exec, g, ghz(), polling_interval_seconds=1)
    output = read_outputs(g, storage)
    print(output)
```
