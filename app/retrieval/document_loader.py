import hashlib
from pathlib import Path


def calculate_content_hash(text: str) -> str:
    return hashlib.sha256(
        text.encode("utf-8")
    ).hexdigest()


def load_text_document(
    file_path: str | Path,
    document_id: int,
    section: str,
) -> dict:
    path = Path(file_path)
    text = path.read_text(encoding="utf-8")

    return {
        "id": str(document_id),
        "text": text,
        "source": path.name,
        "section": section,
        "content_hash": calculate_content_hash(text),
    }


def load_text_documents(
    directory: str | Path,
) -> list[dict]:
    directory_path = Path(directory)

    documents = []

    for document_id, file_path in enumerate(
        sorted(directory_path.glob("*.txt")),
        start=1,
    ):
        documents.append(
            load_text_document(
                file_path=file_path,
                document_id=document_id,
                section="general",
            )
        )

    return documents