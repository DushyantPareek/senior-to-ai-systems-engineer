from app.retrieval.documents import load_documents
from app.retrieval.chunker import chunk_text
from app.services.embedding_service import get_embedding
from app.retrieval.manifest import load_manifest, save_manifest
from app.retrieval.index_store import load_index, save_index


def get_document_status(
    document: dict,
    previous_hashes: dict[str, str],
) -> str:
    document_id = document["id"]
    current_hash = document["content_hash"]

    if document_id not in previous_hashes:
        return "NEW"

    if previous_hashes[document_id] == current_hash:
        return "UNCHANGED"

    return "CHANGED"


async def build_index() -> list[dict]:
    previous_manifest = load_manifest()
    previous_index = load_index()

    indexed_chunks = []
    current_manifest = {}

    documents = load_documents()

    for document in documents:
        status = get_document_status(
            document,
            previous_manifest,
        )

        print(
            f"Document: {document['source']} | "
            f"Status: {status} | "
            f"Hash: {document['content_hash'][:12]}"
        )

        if status == "UNCHANGED":
            existing_chunks = [
                chunk
                for chunk in previous_index
                if chunk["document_id"] == document["id"]
            ]

            indexed_chunks.extend(existing_chunks)
            current_manifest[document["id"]] = document["content_hash"]
            continue

        chunks = chunk_text(
            document["text"],
            chunk_size=20,
            overlap=5,
        )

        for chunk_id, chunk in enumerate(chunks):
            vector = await get_embedding(chunk)

            indexed_chunks.append(
                {
                    "document_id": document["id"],
                    "chunk_id": chunk_id,
                    "text": chunk,
                    "source": document["source"],
                    "section": document["section"],
                    "content_hash": document["content_hash"],
                    "embedding": vector,
                }
            )

        current_manifest[document["id"]] = document["content_hash"]

    save_index(indexed_chunks)
    save_manifest(current_manifest)

    return indexed_chunks
