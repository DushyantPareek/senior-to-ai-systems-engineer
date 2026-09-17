from app.retrieval.documents import load_documents
from app.retrieval.chunker import chunk_text
from app.services.embedding_service import get_embedding

async def build_index() -> list[dict]:
    indexed_chunks = []
    documents = load_documents()

    for document in documents:
        chunks = chunk_text(
            document["text"],
            chunk_size=20,
            overlap=5,
        )

        for chunk_id, chunk in enumerate(chunks):
            vector = await get_embedding(chunk)

            indexed_chunks.append({
                "document_id": document["id"],
                "chunk_id": chunk_id,
                "text": chunk,
                "source": document["source"],
                "section": document["section"],
                "content_hash": document["content_hash"],
                "embedding": vector,
            })
        
        print(
            f"Document: {document['source']} | "
            f"Hash: {document['content_hash'][:12]}"
        )

    return indexed_chunks