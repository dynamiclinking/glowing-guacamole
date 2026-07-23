import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

from .chunker import chunk_text


class ObsidianSearch:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.chunks = [] # list[Chunk]

    def build(self, documents):
        vectors = []

        for doc in tqdm(documents, desc="Chunking notes"):
            doc_id = doc["path"]
            chunks = chunk_text(doc["text"], doc_id)

            for c in chunks:
                embedding = self.model.encode(c.text)
                vectors.append(embedding)
                self.chunks.append(c)


        vectors = np.array(vectors).astype("float32")

        dim = vectors.shape[1]
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(vectors)

    def search(self, query, k=5):
        q_emb = self.model.encode([query]).astype("float32").reshape(1, -1)

        scores, [indexes] = self.index.search(q_emb, k)

        results = []
        for i in indexes:
            results.append(self.chunks[i])


        return results
