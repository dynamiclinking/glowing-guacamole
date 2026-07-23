import json
from pathlib import Path


class StartupLogger:
    def __init__(self, path="startup_logs.jsonl"):
        self.path = Path(path)

    def log(self, data: dict):
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(data) + "\n")
