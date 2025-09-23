FROM python:3.12.11-slim-trixie

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    mpich \
    build-essential \
    cmake \
    libboost-all-dev \
    git


RUN git clone -b release-v0.6.12 https://github.com/qulacs/qulacs.git
WORKDIR qulacs


RUN pip install pytest numpy mpi4py openfermion

RUN C_COMPILER=mpicc CXX_COMPILER=mpic++ USE_MPI=Yes pip install .


RUN USE_TEST=Yes ./script/build_mpicc.sh
RUN cd build && make test
RUN cd build && make pythontest

COPY check_mpi.py .
RUN python check_mpi.py
RUN chmod +x check_mpi.py

CMD ["python", "check_mpi.py"]