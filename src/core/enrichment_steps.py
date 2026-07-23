from core.obsidian_graph import extract_links
from sentence_transformers import SentenceTransformer
from core.chunker import chunk_text
import numpy as np

_model = None

def step_links(docs):
    for d in docs:
        if "text" in d:
            d["links_out"] = extract_links(d["text"])
        else:
            d["links_out"] = []

    return docs

def step_passthrough(docs):
    return docs

PIPELINE_STEPS = {
    "links": step_links,
    "embaddings": step_embeddings,
    "noop": step_passthrough,
}

def step_embeddings(docs):
    model = get_model()

    all_chunks = []
    all_vectors = []

    for doc in docs:
        chunks = chunk_text(doc["text"], doc["path"])

        doc_chunks = []
        for c in chunks:
            vec = model.encode(c.text).astype("float")

            doc_chunks.append({
                "text": c.text,
                "doc_id": doc["path"],
                "embedding": vec
            })

        doc["chunks"] = doc_chunks
        all_chunks.extend(doc_chunks)
    return docs

def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")

    return _model
