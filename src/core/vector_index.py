import faiss
import numpy as np

class VectorIndex:
    def __init__(self):
        self.index = None
        self.chunks = []

    def build(self, documents):
        vectors = []
        self.chunks = []

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

    def search(self, query_embedding, k=5):
        q_emb = self.model.encode([query_embedding]).astype("float32").reshape(1, -1)

        scores, [indexes] = self.index.search(q_emb, k)

        results = []
        for i in indexes:
            results.append(self.chunks[i])


        return results
