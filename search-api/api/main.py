from fastapi import Depends, FastAPI, HTTPException
from loguru import logger

from .deps import get_gemini_client, get_search_client, get_splade_client
from .encoder import SpladeClient
from .llm import GeminiClient
from .models import ChatResponse, SearchRequest
from .search import SearchClient

logger.info("Starting RAG Search API...")
app = FastAPI(title="RAG Search API")


@app.post("/chat", response_model=ChatResponse)
async def chat(
    request: SearchRequest,
    search_client: SearchClient = Depends(get_search_client),
    splade_client: SpladeClient = Depends(get_splade_client),
    gemini_client: GeminiClient = Depends(get_gemini_client),
):
    try:
        logger.info(f"Query: {request.query}")

        # 1. クエリのベクトル化
        sparse_vector = await splade_client.encode(request.query)

        # 2. スパース検索
        contexts = await search_client.search(sparse_vector)

        # 3. 回答生成
        answer = await gemini_client.generate_answer(request.query, contexts)

        return ChatResponse(answer=answer, sources=contexts)
    except Exception as e:
        logger.error(f"Error during chat: {e}")
        raise HTTPException(status_code=500, detail=str(e)) from e


@app.get("/health")
async def health():
    return {"status": "ok"}
