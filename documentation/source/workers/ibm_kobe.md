# IBM Kobe

Interact with the IBM Kobe QPU.

## Authentication

This worker assumes that the following steps have been taken to place a JWT in the appropriate location in the user's filesystem.

```bash
. /vol0300/share/ra010014/jhpcq/x86/scripts/install-cert-files.sh ibm-kobe-dacc
source /vol0003/share/ra010014/jhpcq/bin/jhpc-q-setup.sh
fetch_qtm_jwt.py
mv $HOME/.qtm.jwt $HOME/.sqc_rpc_sched/jwt.token
```

## Building

This worker requires a compilation step linking against libraries accessible on the Fugaku login node.
It also requires a couple Spack packages to be loaded.
(At the time of writing `python` and `gcc` are required.)
To do this run the following command

```bash
./scripts/build.sh
```

in the current directory.

## Running

If this code is run on the Fugaku login node then the worker will load the required Spack packages dynamically.
If the `IS_DEV` environment variable is set some local mocks will be used.
However any meaningful functionality relies on the Fugaku infrastructure.

## Tasks exposed

- `get_transpile_info`: returns an object containing the current backend properties and backend configuration of the IBM Kobe machine. This can be used to inform how we compile our circuits before submission. Uses `subprocess` to call the Riken C API.
- `compile_using_info`: uses the configuration and properties objects returned by `get_transpile_info` to inform which compilation pass to apply. Uses the method `default_compilation_pass_offline` from [pytket-qiskit](https://github.com/CQCL/pytket-qiskit). Intended to be parallelized using Tierkreis map nodes. (The same configuration and properties objects can be used in many parallel compilations if desired.)
- `submit`: Run the given circuit with the specified number of shots on IBM Kobe. The keys of the returned dictionary are the classical reigster names. The values of the returned dictionary are lists of shots. Each shot is a string of 0s and 1s with the lower bits appearing first. Uses `subprocess` to call the Riken `sqcsub` CLI.

## Example graph

A simple graph that shows how to pass the results of the previous stage into the next stage:

```python
g = GraphBuilder(TKR[Circuit], TKR[dict[str, list[str]]])
info = g.task(get_transpile_info())
compiled_circuit = g.task(compile_using_info(info.config, info.props, g.inputs))
res = g.task(submit(compiled_circuit, g.const(10)))
g.outputs(res)
```

A full example graph can be found in `examples/compile_run_ibm.py`.
