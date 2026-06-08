import os
from dotenv import load_dotenv
from groq import Groq
import chromadb
from sentence_transformers import SentenceTransformer

load_dotenv()

CHROMA_DIR = "chroma_db"
COLLECTION_NAME = "omscs_ai_reviews"
MODEL_NAME = "all-MiniLM-L6-v2"
TOP_K = 5

embedding_model = SentenceTransformer(MODEL_NAME)
chroma_client = chromadb.PersistentClient(path=CHROMA_DIR)
collection = chroma_client.get_collection(name=COLLECTION_NAME)

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def retrieve(question, k=TOP_K):
    query_embedding = embedding_model.encode([question]).tolist()[0]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k,
        include=["documents", "metadatas", "distances"]
    )

    chunks = []

    for doc, metadata, distance in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0]
    ):
        chunks.append({
            "text": doc,
            "source": metadata["source"],
            "chunk_id": metadata["chunk_id"],
            "distance": distance
        })

    return chunks


def build_prompt(question, chunks):
    context_blocks = []

    for i, chunk in enumerate(chunks, start=1):
        context_blocks.append(
            f"[Source {i}: {chunk['source']} | Chunk: {chunk['chunk_id']}]\n"
            f"{chunk['text']}"
        )

    context = "\n\n".join(context_blocks)

    return f"""
You are answering questions about Georgia Tech OMSCS AI specialization course reviews.

Answer the user's question using ONLY the provided context.
Do not use outside knowledge.
If the context does not contain enough information, say:
"I don't have enough information in the provided documents to answer that."

Be concise and grounded in the retrieved documents.

Context:
{context}

Question:
{question}
"""


def ask(question):
    chunks = retrieve(question)

    prompt = build_prompt(question, chunks)

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You are a grounded RAG assistant. Use only the provided retrieved context."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    answer = response.choices[0].message.content

    sources = []
    seen = set()

    for chunk in chunks:
        source_label = f"{chunk['source']} ({chunk['chunk_id']}, distance={chunk['distance']:.4f})"
        if source_label not in seen:
            sources.append(source_label)
            seen.add(source_label)

    return {
        "answer": answer,
        "sources": sources,
        "chunks": chunks
    }


if __name__ == "__main__":
    question = "What do students say about ML4T for someone pursuing the AI specialization?"
    result = ask(question)

    print("ANSWER:")
    print(result["answer"])

    print("\nSOURCES:")
    for source in result["sources"]:
        print("-", source)