from app.services.embedding_service import get_embedding
from app.retrieval.indexer import build_index
from app.retrieval.vector_store import search
from app.config import settings


async def retrieve(
    question: str,
    top_k: int | None = None,
) -> list[dict]:

    if top_k is None:
        top_k = settings.rag_top_k

    question_vector = await get_embedding(question)

    results = search(
        query_embedding=question_vector,
        top_k=top_k,
    )

    retrieved_chunks = []

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    for document, metadata, distance in zip(
        documents,
        metadatas,
        distances,
    ):
        if distance > settings.rag_max_distance:
            continue

        retrieved_chunks.append(
            {
                "document_id": metadata["document_id"],
                "chunk_id": metadata["chunk_id"],
                "distance": distance,
                "text": document,
                "source": metadata["source"],
                "section": metadata["section"],
            }
        )

    return retrieved_chunks

if __name__ == "__main__":
    import asyncio

    async def test():
        await build_index()

        results = await retrieve(
            "How can two applications exchange data using HTTP?",
        )

        for result in results:
            print(
                f"Distance: {result['distance']:.4f} | "
                f"Document: {result['text']}"
            )

    asyncio.run(test())