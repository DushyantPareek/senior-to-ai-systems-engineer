from app.retrieval.documents import documents
from app.retrieval.chunker import chunk_text
from app.services.embedding_service import (
    get_embedding,
    cosine_similarity,
)


async def build_index() -> list[dict]:
    indexed_chunks = []

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
                "embedding": vector,
            })

    return indexed_chunks

async def retrieve(
    question: str,
    index: list[dict],
    top_k: int = 2,
    min_score: float = 0.55,
) -> list[dict]:

    question_vector = await get_embedding(question)

    scored_chunks = []

    for chunk in index:
        score = cosine_similarity(
            question_vector,
            chunk["embedding"]
        )

        scored_chunks.append({
            "document_id": chunk["document_id"],
            "chunk_id": chunk["chunk_id"],
            "score": score,
            "text": chunk["text"],
            "source": chunk["source"],
            "section": chunk["section"],
        })

    scored_chunks.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    return [
        chunk
        for chunk in scored_chunks[:top_k]
        if chunk["score"] >= min_score
    ]

if __name__ == "__main__":
    import asyncio

    async def test():
        index = await build_index()

        results = await retrieve(
            "How can two applications exchange data using HTTP?",
            index
        )

        for result in results:
            print(
                f"Score: {result['score']:.4f} | "
                f"Document: {result['text']}"
            )

    asyncio.run(test())