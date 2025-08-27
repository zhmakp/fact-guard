from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Ollama Configuration
    ollama_base_url: str = "http://host.docker.internal:11434"
    ollama_model: str = "gemma2:2b"
    
    # Qdrant Configuration  
    qdrant_host: str = "host.docker.internal"
    qdrant_port: int = 6333
    qdrant_collection_name: str = "fact_guard_docs"
    
    # Application Settings
    log_level: str = "INFO"
    debug: bool = False
    max_upload_size: int = 10485760  # 10MB
    chunk_size: int = 500
    chunk_overlap: int = 100
    
    # External APIs (optional)
    pubmed_api_key: Optional[str] = None
    crossref_email: Optional[str] = None
    
    class Config:
        env_file = ".env"


settings = Settings()