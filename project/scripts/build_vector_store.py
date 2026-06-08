from pathlib import Path
import json
import chromadb
from sentence_transformers import SentenceTransformer

CHUNKS_FILE = Path("chunks.json")
CHROMA_DIR = "chroma_db"
COLLECTION_NAME = "omscs_ai_reviews"

MODEL_NAME = "all-MiniLM-L6-v2"


def load_chunks():
    with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def build_vector_store():
    chunks = load_chunks()

    model = SentenceTransformer(MODEL_NAME)

    client = chromadb.PersistentClient(path=CHROMA_DIR)

    # Delete old collection so reruns don't duplicate chunks
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    collection = client.create_collection(name=COLLECTION_NAME)

    documents = []
    ids = []
    metadatas = []

    for chunk in chunks:
        documents.append(chunk["text"])
        ids.append(chunk["chunk_id"])
        metadatas.append({
            "source": chunk["source"],
            "chunk_id": chunk["chunk_id"]
        })

    embeddings = model.encode(documents).tolist()

    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas
    )

    print(f"Stored {len(documents)} chunks in ChromaDB.")


if __name__ == "__main__":
    build_vector_store()