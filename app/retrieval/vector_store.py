import chromadb


CHROMA_PATH = "data/chroma"
COLLECTION_NAME = "rag_documents"


client = chromadb.PersistentClient(
    path=CHROMA_PATH
)

collection = client.get_or_create_collection(
    name=COLLECTION_NAME
)


def get_collection():
    return collection

def upsert_chunks(chunks: list[dict]) -> None:
    if not chunks:
        return

    ids = []
    documents = []
    embeddings = []
    metadatas = []

    for chunk in chunks:
        ids.append(
            f"document-{chunk['document_id']}-chunk-{chunk['chunk_id']}"
        )

        documents.append(chunk["text"])
        embeddings.append(chunk["embedding"])

        metadatas.append(
            {
                "document_id": chunk["document_id"],
                "chunk_id": chunk["chunk_id"],
                "source": chunk["source"],
                "section": chunk["section"],
                "content_hash": chunk["content_hash"],
            }
        )

    collection.upsert(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
    )

def delete_document(document_id: int) -> None:
    collection.delete(
        where={"document_id": document_id}
    )

def search(
    query_embedding: list[float],
    top_k: int = 2,
) -> dict:
    return collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=[
            "documents",
            "metadatas",
            "distances",
        ],
    )