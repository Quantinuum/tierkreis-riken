# /// script
# requires-python = ">=3.12"
# dependencies = ["tierkreis"]
# ///

from pathlib import Path
from tierkreis import Worker
from tierkreis.namespace import Namespace


if __name__ == "__main__":
    tsp_path = Path(__file__).parent / "schema.tsp"
    namespace = Namespace.from_spec_file(tsp_path)
    worker = Worker("ntchem_worker")
    worker.namespace = namespace
    worker.write_stubs(tsp_path.parent / "stubs.py")
