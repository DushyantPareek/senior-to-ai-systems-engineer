import httpx
import math


OLLAMA_EMBED_URL = "http://localhost:11434/api/embed"


async def get_embedding(text: str) -> list[float]:
    payload = {
        "model": "nomic-embed-text",
        "input": text
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            OLLAMA_EMBED_URL,
            json=payload
        )

        response.raise_for_status()
        result = response.json()

    return result["embeddings"][0]


def cosine_similarity(
    vector_a: list[float],
    vector_b: list[float]
) -> float:

    dot_product = sum(
        a * b
        for a, b in zip(vector_a, vector_b)
    )

    magnitude_a = math.sqrt(
        sum(a * a for a in vector_a)
    )

    magnitude_b = math.sqrt(
        sum(b * b for b in vector_b)
    )

    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0

    return dot_product / (magnitude_a * magnitude_b)

if __name__ == "__main__":
    import asyncio

    async def test():
        print("Test started")

        text_a = "An API allows software systems to communicate."
        text_b = "Chocolate cake requires flour, sugar, and eggs."

        print("Getting vector A...")
        vector_a = await get_embedding(text_a)

        print("Getting vector B...")
        vector_b = await get_embedding(text_b)

        similarity = cosine_similarity(
            vector_a,
            vector_b
        )

        print(f"Vector A length: {len(vector_a)}")
        print(f"Vector B length: {len(vector_b)}")
        print(f"Similarity: {similarity}")

    asyncio.run(test())