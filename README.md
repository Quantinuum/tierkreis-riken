# Tierkreis Riken

Tierkreis workers and example workflows for accessing features specific to Fugaku.

## Set up

It is intended that this repository be cloned onto the Fugaku login server,
for example into the user's home directory.

### Registration smoke tests

In order to access Quantinuum Reimei or IBM Kobe an out-of-band registration process is required.
The registration process is out of scope for this repository but the following scripts can be used to veryify that this part has been set up correctly.
From the root of the repository run the following commands, which will prompt for the credentials used to access Quantinuum Reimei and/or IBM Kobe.

```bash
./smoke_tests/test_reimei_simulator.sh
```

```bash
./smoke_tests/test_ibm_kobe.sh
```
