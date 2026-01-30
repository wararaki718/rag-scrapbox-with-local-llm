from fastapi import APIRouter, Depends, HTTPException

from ..deps import get_encoder
from ..encoder import SpladeEncoder
from ..models import EncodeRequest, EncodeResponse

router = APIRouter()


@router.post("/encode", response_model=EncodeResponse)
async def encode(
    request: EncodeRequest, encoder: SpladeEncoder = Depends(get_encoder)  # noqa: B008
):
    try:
        sparse_vector = encoder.encode(request.text)
        return EncodeResponse(sparse_vector=sparse_vector)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/encode_debug", response_model=EncodeResponse)
async def encode_debug(
    request: EncodeRequest, encoder: SpladeEncoder = Depends(get_encoder)  # noqa: B008
):
    try:
        sparse_vector_tokens = encoder.encode(request.text, return_tokens=True)
        token_ids = encoder.encode(request.text, return_tokens=False)
        return EncodeResponse(sparse_vector=sparse_vector_tokens, token_ids=token_ids)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
