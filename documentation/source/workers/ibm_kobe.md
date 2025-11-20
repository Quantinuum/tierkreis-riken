# IBM Kobe

Interact with the IBM Kobe QPU.

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
