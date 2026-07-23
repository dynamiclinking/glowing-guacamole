from .schema import Chunk

def chunk_text(text: str, doc_id, chunk_size: int = 500, overlap: int =100):
    words = text.split()
    chunks = []

    i = 0
    chunk_index = 0
    while i < len(words):
        chunk_words = words[i:i + chunk_size]
        chunk_text = " ".join(chunk_words)

        chunk = Chunk(
          doc_id = doc_id,
          chunk_id = f"{doc_id}::chunk_{chunk_index}",
          text = chunk_text
        )

        chunks.append(chunk)

        i += chunk_size - overlap # dont make overlap bigger than chunk size
        chunk_index += 1

    return chunks
