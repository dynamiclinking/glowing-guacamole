import time
from .metrics import diversity_score

def run_benchmark(engine_factory, text, k=5):
    """
    engine_factory: function that builds a fresh engine
    tests: list of evaluation cases
    """

    engine = engine_factory()

    results = []
    start = time.perf_counter()

    for t in tests:
        query = t["query"]
        expected = t["expected_theme"]

        retrieved = engine.search(query, k=k)

        doc_diversity = diversity_score(retrieved)

        results.append({
          "query": query,
          "score": best_score,
          "pass": best_score >= threshold,
          "diversity": doc_diversitu,
          "best_match": doc_diversity,
          "expected": expected,
          "top_k": [r["text"][:200] for r in retrieved],
        })

    total_time = time.perf_counter() - start

    return {
      "results": results,
      "time"; total_time
    }
