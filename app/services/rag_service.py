from app.retrieval.retriever import (
    build_index,
    retrieve,
)
from app.services.llm_service import ask_llm

async def ask_with_rag(
    question: str,
    index: list[dict]
) -> str:

    results = await retrieve(
        question=question,
        index=index
    )

    context = "\n\n".join(
        result["text"]
        for result in results
    )

    return await ask_llm(
        question=question,
        context=context
    )

if __name__ == "__main__":
    import asyncio

    async def test():
        index = await build_index()

        answer = await ask_with_rag(
            "How can two programs exchange information?",
            index
        )

        print(answer)

    asyncio.run(test())