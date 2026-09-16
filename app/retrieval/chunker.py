def chunk_text(
    text: str,
    chunk_size: int = 100,
    overlap: int = 20,
) -> list[str]:

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0")

    if overlap < 0:
        raise ValueError("overlap cannot be negative")

    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    words = text.split()

    chunks = []
    start = 0

    while start < len(words):
        end = start + chunk_size

        chunk_words = words[start:end]

        chunks.append(" ".join(chunk_words))

        start += chunk_size - overlap

    return chunks

if __name__ == "__main__":
    text = (
        "REST APIs use HTTP requests and responses to communicate "
        "between applications. GET retrieves resources while POST "
        "commonly creates new resources. Authentication can be "
        "implemented using API keys sessions or access tokens."
    )

    chunks = chunk_text(
        text,
        chunk_size=10,
        overlap=3,
    )

    for i, chunk in enumerate(chunks, start=1):
        print(f"Chunk {i}: {chunk}")