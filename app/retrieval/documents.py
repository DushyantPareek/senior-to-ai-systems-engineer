from pathlib import Path

from app.retrieval.document_loader import load_text_documents


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIRECTORY = PROJECT_ROOT / "data"


def load_documents() -> list[dict]:
    return load_text_documents(DATA_DIRECTORY)