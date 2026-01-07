from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings

from kpbr_chunker import main as load_chunks  # reuse chunker logic


def embed_and_store(chunks):
    client = chromadb.Client(
        Settings(
            persist_directory="vector_store/kpbr",
            anonymized_telemetry=False,
        )
    )

    collection = client.get_or_create_collection(
        name="kpbr_rules"
    )

    model = SentenceTransformer("all-MiniLM-L6-v2")

    texts = [c["text"] for c in chunks]
    metadatas = [c["metadata"] for c in chunks]
    ids = [f"kpbr_{i}" for i in range(len(chunks))]

    embeddings = model.encode(texts, show_progress_bar=True)

    collection.add(
        documents=texts,
        metadatas=metadatas,
        embeddings=embeddings.tolist(),
        ids=ids,
    )

    print(f"Stored {len(chunks)} embeddings in Chroma")



if __name__ == "__main__":
    chunks = load_chunks()
    embed_and_store(chunks)
