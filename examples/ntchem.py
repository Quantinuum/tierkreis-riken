from uuid import UUID
from tierkreis import run_graph
from tierkreis.controller import resume_graph
from tierkreis.storage import FileStorage, read_outputs  # type: ignore
from tierkreis.executor import PJSUBExecutor, ShellExecutor
from tierkreis.builder import GraphBuilder
from tierkreis.models import EmptyModel, TKR

from workers.consts import WORKERS_DIR
from workers.ntchem_worker.stubs import run
from workers.ntchem_worker.spec import NTCHEM_SPEC

storage = FileStorage(UUID(int=107))


def graph():
    g = GraphBuilder(EmptyModel, TKR[str])
    filename = g.task(run())
    g.outputs(filename)
    return g


def main():
    # executor = PJSUBExecutor(WORKERS_DIR, storage.logs_path, NTCHEM_SPEC)
    executor = ShellExecutor(WORKERS_DIR, storage.logs_path.parent)
    storage.clean_graph_files()
    run_graph(storage, executor, graph().get_data(), {})
    print(read_outputs(graph().get_data(), storage))  # type: ignore


if __name__ == "__main__":
    main()
