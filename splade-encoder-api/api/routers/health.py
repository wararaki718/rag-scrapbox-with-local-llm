from fastapi import APIRouter

from ..deps import MODEL_ID

router = APIRouter()


@router.get("/health")
async def health():
    return {"status": "ok", "model": MODEL_ID}
