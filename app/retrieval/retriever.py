from app.services.embedding_service import (
    get_embedding,
    cosine_similarity,
)

documents = [
    {
        "id": 1,
        "text": (
            "Dependency injection provides dependencies to a class "
            "from outside rather than creating them internally."
        ),
    },
    {
        "id": 2,
        "text": (
            "An API is an interface that allows software systems "
            "to communicate."
        ),
    },
    {
        "id": 3,
        "text": (
            "FastAPI is a Python web framework used to build APIs."
        ),
    },
]

async def build_index() -> list[dict]:
    indexed_documents = []

    for document in documents:
        vector = await get_embedding(
            document["text"]
        )

        indexed_documents.append({
            "id": document["id"],
            "text": document["text"],
            "embedding": vector
        })

    return indexed_documents

async def retrieve(
    question: str,
    index: list[dict],
    top_k: int = 2
) -> list[dict]:

    question_vector = await get_embedding(question)

    scored_documents = []

    for document in index:
        score = cosine_similarity(
            question_vector,
            document["embedding"]
        )

        scored_documents.append({
            "id": document["id"],
            "score": score,
            "text": document["text"]
        })

    scored_documents.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    return scored_documents[:top_k]

if __name__ == "__main__":
    import asyncio

    async def test():
        index = await build_index()

        results = await retrieve(
            "How can two programs exchange information?",
            index
        )

        for result in results:
            print(
                f"Score: {result['score']:.4f} | "
                f"Document: {result['text']}"
            )

    asyncio.run(test())