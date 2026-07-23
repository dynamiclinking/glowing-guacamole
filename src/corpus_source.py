from dataclasses import dataclass
from typing import Callable, Any

@Dataclass
class CorpusSource:
    id: str
    path: str
    importer: Callable[[str], lsit[dict]]
    label: str
    attribution: list[str]
