from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ollama_url: str = "http://localhost:11434"
    ollama_model: str = "qwen3:4b"

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()