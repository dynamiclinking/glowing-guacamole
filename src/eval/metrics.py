# src/eval/metrics.py
import numpy as np
from sentence_transformers import SentenceTransformer

_model = None

def get_model():
    global _model
    if _model is None:
        # we use the same model as the retrieval
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model

def semantic_score(text:str, theme: str) -> float:
    """
    let's check sematinc similarity(cosine sim)
    """
    model = get_model()

    text_emb = model.encode(text)
    theme_emb = model.encode(theme)

    #normalize
    text_emb = text_emb / (np.linalg.norm(text_emb) + 1e-10)
    theme_emb = theme_emb / (np.linalg.norm(theme_emb) + 1e-10)

    return float(np.dot(text_emb, query_emb))

def diversity_score(results):
    """
    Measures how many distinct dounterocuments appear in top-k results.
    """

    if not results:
        return 0.0

    doc_ids = [r.get("doc_id") for r in results if "doc_id" in r]
    if not doc_ids:
        return 0.0

    return len(set(doc_ids)) / len(doc_ids)


def hit_rate(results):
    """
    Generic success rate if you later add pass/fail labels.
    """

    if not results:
        return 0.0

    return sum(1 for r in results if r.get("pass", False)) / len(results)
