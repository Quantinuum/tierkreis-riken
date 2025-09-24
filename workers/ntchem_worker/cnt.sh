#!/usr/bin/env bash
# GLOBALS
export FLIB_SCCR_CNTL=FALSE
export OMP_NUM_THREADS=12
export OMP_STACKSIZE=3G


# LOCALS
MOL="cnt"
curdir=`pwd`
bindir="/home/${USER}/20250811mpiomp"
scrdir="${curdir}/_scr"
wrkdir="${PJM_SHAREDTMP}/ntchem/${MOL}"
sub="_mpiomp"
mpirun="mpiexec -std-proc ${wrkdir}/job.out"

# Shell settings
set -ex
ulimit -s unlimited

# Prepare working directory
rm -rf $wrkdir
rm -rf $scrdir
mkdir -p $wrkdir
mkdir -p $scrdir
cd $wrkdir
rm -rf $curdir/$MOL.out

# Actual script


# --- LR ---
# Basis
cp -pr $curdir/$MOL.LR.basis.inp INPUT
$mpirun $bindir/basinp${sub}.exe
mv job.out.*.0 ${scrdir}
# --- LM ---
# Basis
cp -pr $curdir/$MOL.LM.basis.inp INPUT
$mpirun $bindir/basinp${sub}.exe
mv job.out.*.0 ${scrdir}
# --- HM ---
# Basis
cp -pr $curdir/$MOL.HM.basis.inp INPUT
$mpirun $bindir/basinp${sub}.exe
mv job.out.*.0 ${scrdir}
# --- ONIOM ---
# Basis
cp -pr $curdir/$MOL.basis.inp INPUT
$mpirun $bindir/basinp${sub}.exe
mv job.out.*.0 ${scrdir}
# ONIOMPrep
cp -pr $curdir/$MOL.oniom.inp INPUT
$mpirun $bindir/oniomprep${sub}.exe
mv job.out.*.0 ${scrdir}

#--- LR ---
# NDDO
cp -pr $curdir/$MOL.LR.nddo.inp INPUT
$mpirun $bindir/mdint1${sub}.exe
mv job.out.*.0 ${scrdir}
$mpirun $bindir/scf${sub}.exe
mv job.out.*.0 ${scrdir}
# HF
cp -pr $curdir/$MOL.LR.hf0.inp INPUT
$mpirun $bindir/mdint1${sub}.exe
mv job.out.*.0 ${scrdir}
$mpirun $bindir/scf${sub}.exe
mv job.out.*.0 ${scrdir}
# DFT+TDDFT
cp -pr $curdir/$MOL.LR.dft.inp INPUT
$mpirun $bindir/mdint1${sub}.exe
mv job.out.*.0 ${scrdir}
###cp -pr $curdir/$MOL.LR.MO .
$mpirun $bindir/scf${sub}.exe
mv job.out.*.0 ${scrdir}
$mpirun $bindir/tddft${sub}.exe
mv job.out.*.0 ${scrdir}
#--- LM ---
# NDDO
cp -pr $curdir/$MOL.LM.nddo.inp INPUT
$mpirun $bindir/mdint1${sub}.exe
mv job.out.*.0 ${scrdir}
$mpirun $bindir/scf${sub}.exe
mv job.out.*.0 ${scrdir}
# HF
cp -pr $curdir/$MOL.LM.hf0.inp INPUT
$mpirun $bindir/mdint1${sub}.exe
mv job.out.*.0 ${scrdir}
$mpirun $bindir/scf${sub}.exe
mv job.out.*.0 ${scrdir}
# DFT+TDDFT
cp -pr $curdir/$MOL.LM.dft.inp INPUT
$mpirun $bindir/mdint1${sub}.exe
mv job.out.*.0 ${scrdir}
###cp -pr $curdir/$MOL.LM.MO .
$mpirun $bindir/scf${sub}.exe
mv job.out.*.0 ${scrdir}
###cp -pr $MOL.LM.MO $curdir/.
$mpirun $bindir/tddft${sub}.exe
mv job.out.*.0 ${scrdir}
#--- HM ---
# HF with low-level MOs
cp -pr $curdir/$MOL.HM.dft.inp INPUT
$mpirun $bindir/mdint1${sub}.exe
mv job.out.*.0 ${scrdir}
#--- projection of low-level MOs into high-level ones
cp -pr $MOL.LM.MO $MOL.HM.MO
$mpirun $bindir/projmo${sub}.exe
mv job.out.*.0 ${scrdir}
$mpirun $bindir/scf${sub}.exe
mv job.out.*.0 ${scrdir}
###$mpirun $bindir/tddft${sub}.exe
# FCIDUMP
cp -pr $curdir/$MOL.HM.fcidump.inp INPUT
$mpirun $bindir/fcidumpd${sub}.exe
mv job.out.*.0 ${scrdir}
cp -pr FCIDUMP $curdir/
# --- ONIOM ---


cd $curdir
