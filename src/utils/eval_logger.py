import json
import time
from pathlib import Path


class EvalLogger:
    def __init__(self, path="eval_logs.jsonl"):
        self.path = Path(path)

    def log_query(self, query, results, selected_ids=None):
        record = {
            "timestamp": time.time(),
            "query": query,
            "results": [
                {
                    "doc_id": r.doc_id,
                    "chunk_id": r.chunk_id,
                    "text": r.text[:200]
                }
                for r in results
            ],
            "selected_ids": selected_ids or []
        }

        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")
