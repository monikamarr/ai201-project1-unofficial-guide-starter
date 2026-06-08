from pathlib import Path
import json
import re
import html
import random

RAW_DIR = Path("data/raw")
OUTPUT_FILE = Path("chunks.json")

CHUNK_SIZE = 700
CHUNK_OVERLAP = 150


def clean_text(text):
    text = html.unescape(text)

    # Remove HTML tags if any were copied
    text = re.sub(r"<[^>]+>", " ", text)

    # Remove extra whitespace
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    chunks = []

    if not text:
        return chunks

    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()

        if len(chunk) > 0:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def load_documents():
    documents = []

    for file_path in RAW_DIR.glob("*.txt"):
        raw_text = file_path.read_text(encoding="utf-8")
        cleaned_text = clean_text(raw_text)

        documents.append({
            "source": file_path.name,
            "text": cleaned_text
        })

    return documents


def main():
    documents = load_documents()
    all_chunks = []

    for doc in documents:
        chunks = chunk_text(doc["text"])

        for i, chunk in enumerate(chunks):
            all_chunks.append({
                "chunk_id": f"{doc['source']}_{i}",
                "source": doc["source"],
                "text": chunk
            })

    OUTPUT_FILE.write_text(
        json.dumps(all_chunks, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

    print(f"Loaded documents: {len(documents)}")
    print(f"Total chunks: {len(all_chunks)}")
    print("\nSample chunks:\n")

    for chunk in random.sample(all_chunks, min(5, len(all_chunks))):
        print("=" * 80)
        print(f"Source: {chunk['source']}")
        print(f"Chunk ID: {chunk['chunk_id']}")
        print(chunk["text"])
        print()


if __name__ == "__main__":
    main()