# src/eval/dataset_loader.py

import json
from pathlib import Path


def load_json_dataset(path: str):
    """
    Load evaluation datasets from JSON files.

    Future:
    - versioned datasets (eval_v1, eval_v2)
    - per-source datasets (obsidian-only, multi-source)
    """

    path = Path(path)

    with path.open("r", encoding="utf-8") as f:
        return json.load(f)
