import json
from pathlib import Path
from core.graph_builder import hash_text

CACHE_FILE = Path(".cache/graph.json")
CACHE_VERSION = 1

def save_graph(graph):
    payload = {
        "version": CACHE_VERSION,
        "graph": graph,
    }

    CACHE_FILE.write_text(json.dumps(payload, indent=2))

def load_graph():
    if not CACHE_FILE.exists():
        return None

    return json.loads(CACHE_FILE.read_text())

def is_stale(cached, documents):
    if cached is None:
        return True

    if cached.get("version") != CACHE_VERSION:
        return True

    cached_manifest = cached["graph"]["manifest"]

    for doc in documents:
        path = doc["path"]
        if path not in cached_manifest:
            return True

        if cached_manifest[path] != hash_text(doc["text"]):
            return True

    return False

