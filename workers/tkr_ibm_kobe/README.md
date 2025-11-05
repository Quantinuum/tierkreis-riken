# IBM Kobe worker

A Tierkreis worker to interact with the IBM Kobe QPU.

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

- `get_transpile_info`: requests IBM Kobe for its current `BackendConfiguration` and `BackendProperties`.
- `compile_using_info`: takes the `BackendConfiguration` and `BackendProperties` along with a circuit and performs the appropriate compilation pass determined by `pytket-qiskit`.
