from pathlib import Path

from app.retrieval.document_loader import load_text_document


PROJECT_ROOT = Path(__file__).resolve().parents[2]

API_GUIDE_PATH = PROJECT_ROOT / "data" / "api-guide.txt"

documents = [
    {
        "id": 1,
        "text": (
            "Dependency injection provides dependencies to a "
            "class from outside rather than creating them internally."
        ),
        "source": "software-design-notes",
        "section": "dependency-injection",
    },
    {
        "id": 2,
        "text": (
            "An API is an interface that allows software "
            "systems to communicate."
        ),
        "source": "api-documentation",
        "section": "introduction",
    },
    {
        "id": 3,
        "text": (
            "FastAPI is a Python web framework used to build APIs."
        ),
        "source": "fastapi-notes",
        "section": "overview",
    },
    load_text_document(
        file_path=API_GUIDE_PATH,
        document_id=4,
        section="rest",
    ),
]