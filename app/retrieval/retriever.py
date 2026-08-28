import re

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

STOP_WORDS = {
    "a",
    "an",
    "the",
    "is",
    "what",
    "how",
    "why",
    "are",
    "of",
    "to",
    "in",
}

def tokenize(text: str) -> set[str]:
    text = text.lower()

    words = re.findall(
        r"\b\w+\b",
        text
    )

    return {
        word
        for word in words
        if word not in STOP_WORDS
    }

def retrieve(question: str, top_k: int = 2) -> list[str]:
    question_words = tokenize(question)

    scored_documents = []

    for document in documents:
        document_words = tokenize(
            document["text"]
        )

        score = len(
            question_words & document_words
        )

        scored_documents.append(
            (score, document["text"])
        )
        

    scored_documents.sort(
        key=lambda item: item[0],
        reverse=True
    )

    return [
        {
            "score": score,
            "text": text
        }
        for score, text in scored_documents[:top_k]
        if score > 0
    ]


if __name__ == "__main__":
    results = retrieve("How can two programs exchange information?")

    for result in results:
        print(
            f"Score: {result['score']} | "
            f"Document: {result['text']}"
        )