from pathlib import Path

from tierkreis.namespace import Namespace

REPO_DIR = Path(__file__).parent.parent
TSP_WORKERS = [REPO_DIR / "workers" / "tkr_sqcsub" / "schema.tsp"]


def generate_tsp_stubs(tsp_path: Path):
    namespace = Namespace.from_spec_file(tsp_path)
    namespace.write_stubs(tsp_path.parent / "stubs.py")


def generate_stubs():
    [generate_tsp_stubs(w) for w in TSP_WORKERS]


if __name__ == "__main__":
    generate_stubs()
