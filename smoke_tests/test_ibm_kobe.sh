. /vol0300/share/ra010014/jhpcq/x86/scripts/install-cert-files.sh ibm-kobe-dacc;
source /vol0003/share/ra010014/jhpcq/bin/jhpc-q-setup.sh
fetch_qtm_jwt.py
mv $HOME/.qtm.jwt $HOME/.sqc_rpc_sched/jwt.token

. /vol0300/share/ra010014/jhpcq/x86/scripts/setenv-sqcsub.sh ibm-kobe-dacc;
sqcsub --nqubits 10 --nshots 30 --ifile simple_ibm_kobe.qasm --iformat qasm --ofile result.txt --oformat raw --qpu ibm-kobe-dacc
