. /vol0300/share/ra010014/jhpcq/x86/scripts/install-cert-files.sh reimei;
source /vol0003/share/ra010014/jhpcq/bin/jhpc-q-setup.sh
fetch_qtm_jwt.py
mv $HOME/.qtm.jwt $HOME/.sqc_rpc_sched/jwt.token

. /vol0300/share/ra010014/jhpcq/x86/scripts/setenv-sqcsub.sh reimei-simulator
sqcsub --nqubits 10 --nshots 30 --ifile simple_reimei_simulator.qasm --iformat qasm --ofile result.txt --oformat raw --qpu reimei-simulator
