SYSTEM_PROMPT = (
    "You are a concise technical assistant. "
    "Explain concepts clearly for a software engineer."
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