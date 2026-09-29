from app.services.embedding_service import (
    get_embedding,
    cosine_similarity,
)
from app.retrieval.indexer import build_index
from app.retrieval.vector_store import search

async def retrieve(
    question: str,
    top_k: int = 2,
) -> list[dict]:

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