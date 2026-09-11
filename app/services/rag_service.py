from app.retrieval.retriever import (
    build_index,
    retrieve,
)
from app.services.llm_service import ask_llm
from app.prompts.prompts import RAG_SYSTEM_PROMPT

async def ask_with_rag(
    question: str,
    index: list[dict]
) -> dict:

    results = await retrieve(
        question=question,
        index=index
    )

    if not results:
        return {
            "answer": (
                "I couldn't find relevant information "
                "in the available knowledge base."
            ),
            "sources": [],
        }

    context = "\n\n".join(
        (
            f"[Source: {result['source']} | "
            f"Section: {result['section']}] "
            f"{result['text']}"
        )
        for result in results
    )

    answer = await ask_llm(
        question=question,
        context=context,
        system_prompt=RAG_SYSTEM_PROMPT
    )

    sources = [
        {
            "id": result["id"],
            "source": result["source"],
            "section": result["section"],
            "score": result["score"],
        }
        for result in results
    ]

    return {
        "answer": answer,
        "sources": sources,
    }

if __name__ == "__main__":
    import asyncio

    async def test():
        index = await build_index()

        result = await ask_with_rag(
            "What is Kubernetes?",
            index
        )

        print("\n[Answer]")
        print(result["answer"])

        print("\n[Sources]")

        for source in result["sources"]:
            print(
                f"{source['source']} | "
                f"{source['section']} | "
                f"{source['score']:.4f}"
            )

    asyncio.run(test())