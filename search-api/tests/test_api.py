import pytest
from unittest.mock import AsyncMock
from api.main import app
from api.deps import get_search_client, get_splade_client, get_gemini_client

@pytest.fixture(autouse=True)
def cleanup_overrides():
    app.dependency_overrides.clear()
    yield
    app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_health(client):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

@pytest.mark.asyncio
async def test_chat_success(client):
    # Mock implementations
    mock_sparse_vector = {"hello": 1.5, "world": 2.0}
    mock_search_results = [
        {"text": "mock text", "title": "mock title", "url": "http://mock", "score": 10.0}
    ]
    mock_answer = "This is a mock answer from Gemini."

    # Create mock objects
    mock_splade = AsyncMock()
    mock_splade.encode.return_value = mock_sparse_vector
    
    mock_search = AsyncMock()
    mock_search.search.return_value = mock_search_results
    
    mock_gemini = AsyncMock()
    mock_gemini.generate_answer.return_value = mock_answer

    # Setup dependency overrides
    app.dependency_overrides[get_splade_client] = lambda: mock_splade
    app.dependency_overrides[get_search_client] = lambda: mock_search
    app.dependency_overrides[get_gemini_client] = lambda: mock_gemini

    response = await client.post(
        "/chat",
        json={"query": "test query"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["answer"] == mock_answer
    assert len(data["sources"]) == 1
    assert data["sources"][0]["title"] == "mock title"

@pytest.mark.asyncio
async def test_chat_error(client):
    mock_splade = AsyncMock()
    mock_splade.encode.side_effect = Exception("Encoding failed")
    
    app.dependency_overrides[get_splade_client] = lambda: mock_splade

    response = await client.post(
        "/chat",
        json={"query": "test query"}
    )

    assert response.status_code == 500
    assert "Encoding failed" in response.json()["detail"]
