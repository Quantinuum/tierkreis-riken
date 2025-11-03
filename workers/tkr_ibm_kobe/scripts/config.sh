#!/bin/bash
set -xeuo pipefail

#SQC Library Version
SQC_VERSION=0.9
#Architecture
ARCH=$(uname -m)
if [ "$ARCH" = "x86_64" ]; then
  #Packcage Name：python@3.11.6(yjlixq5), gcc@13.2.0(77gzpid)
  SPACK_PKG="python/yjlixq5 gcc/77gzpid"
  #Target Name
  TARGET_NAME=x86
elif [ "$ARCH" = "aarch64" ]; then
  echo "This architecture is not supported."
  exit 1
  #Packcage Name：gcc@14.1.0/6mygk5q, py-numpy@1.25.2(dgmiy5n), python@3.11.6(qbmpmn2)
  SPACK_PKG="/6mygk5q /dgmiy5n /qbmpmn2"
  #Target Name
  TARGET_NAME=a64fx
else
  echo "error ${ARCH} is unknown"
  exit 1
fi
#Python Virtual Environment Name
VENV_NAME=venv_SQC_${SQC_VERSION}
#SQC Library Directory
SQC_DIR=/vol0300/share/ra010014/jhpcq_modules/${TARGET_NAME}/SDK/SQC_library_${SQC_VERSION}
