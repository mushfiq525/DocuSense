from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    GEMINI_API_KEY: str = ""
    GROQ_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-flash-latest"
    GROQ_MODEL: str = "openai/gpt-oss-20b"

    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    CHUNK_SIZE: int = 500
    CHUNK_OVERLAP: int = 50
    TOP_K: int = 3
    SIMILARITY_THRESHOLD: float = 0.6

    CHROMA_DIR: str = "./chroma_db"
    COLLECTION_NAME: str = "docusense"
    SOURCE_MD_PATH: str = "docs/source.md"


settings = Settings()