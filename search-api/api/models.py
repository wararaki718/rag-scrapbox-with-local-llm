from pydantic import BaseModel, Field


class SearchRequest(BaseModel):
    query: str = Field(..., description="User query for search")


class SearchResult(BaseModel):
    text: str
    title: str
    url: str
    score: float


class ChatResponse(BaseModel):
    answer: str
    sources: list[SearchResult]
