from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    ELASTICSEARCH_URL: str = Field(default="http://localhost:9200")
    ELASTICSEARCH_INDEX: str = Field(default="scrapbox-pages")
    
    SPLADE_API_URL: str = Field(default="http://localhost:8000/encode")
    
    GEMINI_API_KEY: str | None = Field(default=None)
    GEMINI_MODEL_NAME: str = Field(default="gemini-3-flash-preview")  # デフォルトを安定したものに
    
    # チャンク処理とRPM制限用の設定
    GEMINI_CONTEXT_CHUNK_SIZE: int = Field(default=3)
    GEMINI_RPM_DELAY: float = Field(default=1.0)  # 秒単位での遅延

settings = Settings()
