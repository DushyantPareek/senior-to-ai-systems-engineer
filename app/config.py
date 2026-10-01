from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ollama_url: str = "http://localhost:11434"
    ollama_model: str = "qwen3:4b"
    
    rag_max_distance: float = 0.8
    rag_top_k: int = 2

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()