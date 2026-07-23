from .engine import ObsidianSearch
from .importers.obsidian import load_markdown_files

def build_engine(vault_path, model_name="all-MiniLM-L6-v2"):
    """
    return a fresh, fully initialized engine isntance.
    used by evaluation and CLi
    """

    def factory():
        docs = load_markdown_files(vault_path)

        engine = ObsidianSearch(model=model_name)
        engine.build(docs)

        return engine

    return factory
