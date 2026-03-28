from pathlib import Path

from tierkreis.hpc import JobSpec, ResourceSpec, MpiSpec

NTCHEM_SPEC = JobSpec(
    job_name="ntchem",
    command="main.sh",  # make sure the path to main is correct
    resource=ResourceSpec(
        nodes=64, cores_per_node=None, memory_gb=None, gpus_per_node=None
    ),
    walltime="08:00:00",
    account="hp240496",
    queue="q-QTM-M",
    extra_scheduler_args={
        "--llio": "sharedtmp-size=61Gi",
        "-z": "jid",
    },
    output_path=Path("./output"),
    error_path=Path("./errors"),
    mpi=MpiSpec(max_proc_per_node=4),
    environment={
        "FLIB_SCCR_CNTL": "FALSE",
        "OMP_NUM_THREADS": "12",
        "OMP_STACKSIZE": "3G",
    },
)
