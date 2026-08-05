import os
import time

from core.graph_cache import load_graph, save_graph, is_stale
from core.graph_builder import build_graph
from core.importers.obsidian import load_markdown_files
from core.engine import ObsidianSearch
from utils.meta import get_git_info, get_timestamp
from utils.logger import StartupLogger
from utils.eval_logger import EvalLogger

from cli.app import SearchApp


def main():
    vault_path = os.environ.get("OBSIDIAN_VAULT")  # <-- change this
    if not vault_path:
        raise ValueError("Please set OBSIDIAN_VAULT environment variable")

    logger = StartupLogger()
    eval_logger = EvalLogger()
    git = get_git_info()

    start_total = time.perf_counter()

    print("Loading vault...")
    t0 = time.perf_counter()
    docs = load_markdown_files(vault_path)
    t_load = time.perf_counter() - t0
    print(f"Loaded {len(docs)} notes")

    cached = load_graph()
    if is_stale(cached, docs):
        print("Building Graph...")
        graph = build_graph(docs)
        save_graph(graph)
    else:
        print("Using cached graph")
        graph = cached["graph"]


    print("Building index...")
    engine = ObsidianSearch()

    t1 = time.perf_counter()
    engine.build(docs)
    t_build = time.perf_counter() - t1

    total = time.perf_counter() - start_total

    record = {
      "timestamp": get_timestamp(),
      "git": git,
      "timings": {
          "load": t_load,
          "build": t_build,
          "total": total
      },
      "num_docs": len(docs)
    }

    logger.log(record)
    print(f"#\nTOTAL statup: {total:3f}s")
    print("Logged run:", record)

    print("Ready. Type queries (or 'exit'):")

    eval_logger = EvalLogger()
    app = SearchApp(engine, eval_logger)
    app.run()




if __name__ == "__main__":
    main()
