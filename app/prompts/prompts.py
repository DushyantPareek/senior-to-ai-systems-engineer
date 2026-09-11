SYSTEM_PROMPT = (
    "You are a concise technical assistant. "
    "Explain concepts clearly for a software engineer."
)

RAG_SYSTEM_PROMPT = (
    "You are a grounded question-answering assistant. "
    "Answer using only the provided context. "
    "If the context does not contain enough information "
    "to answer the question, say that you do not have "
    "enough information."
)


def build_prompt(
    question: str,
    context: str = ""
) -> str:

    if context:
        return f"""
Context:
{context}

Question:
{question}
""".strip()

    return f"""
Question:
{question}
""".strip()