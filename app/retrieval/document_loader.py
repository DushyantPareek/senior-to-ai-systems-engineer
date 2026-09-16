from pathlib import Path


def load_text_document(
    file_path: str | Path,
    document_id: int,
    section: str,
) -> dict:

    path = Path(file_path)

    text = path.read_text(encoding="utf-8")

    return {
        "id": document_id,
        "text": text,
        "source": path.name,
        "section": section,
    }