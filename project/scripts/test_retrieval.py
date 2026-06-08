import chromadb
from sentence_transformers import SentenceTransformer

CHROMA_DIR = "chroma_db"
COLLECTION_NAME = "omscs_ai_reviews"
MODEL_NAME = "all-MiniLM-L6-v2"

TOP_K = 5


def retrieve(query, k=TOP_K):
    model = SentenceTransformer(MODEL_NAME)
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    collection = client.get_collection(name=COLLECTION_NAME)

    query_embedding = model.encode([query]).tolist()[0]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k,
        include=["documents", "metadatas", "distances"]
    )

    return results


def print_results(query):
    results = retrieve(query)

    print("=" * 100)
    print(f"QUERY: {query}")
    print("=" * 100)

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    for i, (doc, metadata, distance) in enumerate(zip(documents, metadatas, distances), start=1):
        print(f"\nResult {i}")
        print(f"Source: {metadata['source']}")
        print(f"Chunk ID: {metadata['chunk_id']}")
        print(f"Distance: {distance:.4f}")
        print(f"Text: {doc}")
        print("-" * 100)


if __name__ == "__main__":
    test_queries = [
        "What courses do OMSCS students commonly recommend as a first course for students interested in AI?"
    ]

    for query in test_queries:
        print_results(query)