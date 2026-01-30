import httpx

from .config import settings


class SpladeClient:
    def __init__(self, api_url: str = settings.SPLADE_API_URL):
        self.api_url = api_url

    async def encode(self, text: str) -> dict[str, float]:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.api_url, json={"text": text}, timeout=30.0
            )
            response.raise_for_status()
            return response.json()["sparse_vector"]
