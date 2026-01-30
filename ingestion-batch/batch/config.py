from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    SCRAPBOX_PROJECT: str = Field(default="dummy-project")
    SCRAPBOX_SID: str | None = Field(default=None)
    
    ELASTICSEARCH_URL: str = Field(default="http://localhost:9200")
    ELASTICSEARCH_INDEX: str = Field(default="scrapbox-pages")
    
    SPLADE_API_URL: str = Field(default="http://localhost:8000/encode")
    
    CHUNK_SIZE: int = Field(default=500)
    CHUNK_OVERLAP: int = Field(default=50)

settings = Settings()
