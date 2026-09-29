import asyncio

from app.retrieval.vector_store import search
from app.services.embedding_service import get_embedding


async def main():
    question = "How do applications communicate using HTTP?"

    query_embedding = await get_embedding(question)

    results = search(
        query_embedding=query_embedding,
        top_k=3,
    )

    print(results)


if __name__ == "__main__":
    asyncio.run(main())