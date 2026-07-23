from dataclasses import dataclass

@dataclass(frozen=True)
class Chunk:
    doc_id: str
    chunk_id: str
    text: str
