from typing import Dict, Optional

from pydantic import BaseModel


class EncodeRequest(BaseModel):
    text: str


class EncodeResponse(BaseModel):
    sparse_vector: Dict[str, float]
    token_ids: Optional[Dict[str, float]] = None
