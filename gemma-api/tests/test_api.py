import pytest
import httpx
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock, patch
from api.main import app

@pytest.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

@pytest.mark.asyncio
async def test_health_success(client):
    with patch("api.main.client.list", new_callable=AsyncMock) as mock_list:
        mock_list.return_value = {"models": []}
        response = await client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok", "ollama_connected": True}

@pytest.mark.asyncio
async def test_health_failure(client):
    with patch("api.main.client.list", new_callable=AsyncMock) as mock_list:
        mock_list.side_effect = Exception("Ollama connection failed")
        response = await client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "error", "ollama_connected": False}

@pytest.mark.asyncio
async def test_chat_completions_success(client):
    mock_response = {
        "message": {
            "role": "assistant",
            "content": "Hello! I am Gemma."
        }
    }
    with patch("api.main.client.chat", new_callable=AsyncMock) as mock_chat:
        mock_chat.return_value = mock_response
        
        request_data = {
            "messages": [
                {"role": "user", "content": "Hi"}
            ],
            "temperature": 0.7
        }
        response = await client.post("/v1/chat/completions", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["choices"][0]["message"]["content"] == "Hello! I am Gemma."
        assert data["choices"][0]["message"]["role"] == "assistant"

@pytest.mark.asyncio
async def test_chat_completions_error(client):
    with patch("api.main.client.chat", new_callable=AsyncMock) as mock_chat:
        mock_chat.side_effect = Exception("Internal Ollama Error")
        
        request_data = {
            "messages": [
                {"role": "user", "content": "Hi"}
            ]
        }
        response = await client.post("/v1/chat/completions", json=request_data)
        
        assert response.status_code == 500
        assert "Internal Ollama Error" in response.json()["detail"]
