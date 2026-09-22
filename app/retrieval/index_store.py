import json
from pathlib import Path


INDEX_PATH = Path("data/index.json")


def load_index() -> list[dict]:
    if not INDEX_PATH.exists():
        return []

    with INDEX_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_index(indexed_chunks: list[dict]) -> None:
    INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)

    with INDEX_PATH.open("w", encoding="utf-8") as file:
        json.dump(indexed_chunks, file, indent=2)