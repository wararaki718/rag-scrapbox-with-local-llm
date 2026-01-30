from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    ELASTICSEARCH_URL: str = Field(default="http://localhost:9200")
    ELASTICSEARCH_INDEX: str = Field(default="scrapbox-pages")
    
    SPLADE_API_URL: str = Field(default="http://localhost:8000/encode")
    
    # LLM設定
    LLM_API_BASE: str = Field(default="http://gemma-api:11434/v1")
    LLM_API_KEY: str = Field(default="not-needed")
    LLM_MODEL_NAME: str = Field(default="gemma-3-4b-it")
    
    # チャンク処理の設定
    LLM_CONTEXT_CHUNK_SIZE: int = Field(default=3)

settings = Settings()
