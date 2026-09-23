import asyncio
import chromadb

from app.services.embedding_service import get_embedding


client = chromadb.PersistentClient(
    path="./data/chroma"
)

collection = client.get_or_create_collection(
    name="rag_documents"
)


async def main():
    question = "How can software applications communicate?"

    query_embedding = await get_embedding(question)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=2
    )

    print("Results:")
    print(results)


if __name__ == "__main__":
    asyncio.run(main())