from collections import defaultdict
import hashlib

def hash_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def build_graph(documents):
    """
    Returns:
        edges: list of(source,target)
        manifest: simple hash map for staleness checks
    """

    edges = []
    manifest = {}

    for doc in documents:
        src = doc["path"]
        text = doc["text"]

        manifest[src] = hash_text(text)

        for link in doc.get("links_out", []):
            # implying that target exists
            edges.append((src,link))


    graph = {
        "edges": edges,
        "manifest": manifest,
    }

    return graph
