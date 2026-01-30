import pytest
from unittest.mock import AsyncMock, patch
from api.search import SearchClient
from api.models import SearchResult

@pytest.fixture
async def search_client():
    with patch("elasticsearch.AsyncElasticsearch"):
        client = SearchClient()
        yield client
        await client.close()

@pytest.mark.asyncio
async def test_search_empty_vector(search_client):
    results = await search_client.search({}, top_k=5)
    assert results == []

@pytest.mark.asyncio
async def test_search_success(search_client):
    # Mock ES response
    mock_response = {
        "hits": {
            "hits": [
                {
                    "_source": {
                        "text": "test text",
                        "title": "test title",
                        "url": "http://test",
                    },
                    "_score": 1.5,
                }
            ]
        }
    }
    search_client.es.search = AsyncMock(return_value=mock_response)
    
    sparse_vector = {"token1": 0.5, "token2": 1.2}
    results = await search_client.search(sparse_vector, top_k=2)
    
    assert len(results) == 1
    assert results[0].title == "test title"
    assert results[0].score == 1.5
    
    # Verify query structure
    search_client.es.search.assert_called_once()
    call_args = search_client.es.search.call_args[1]
    assert call_args["size"] == 2
    query = call_args["query"]
    assert "bool" in query
    should = query["bool"]["should"]
    assert len(should) == 2
    assert should[0]["rank_feature"]["field"] == "sparse_vector.token1"

@pytest.mark.asyncio
async def test_search_error(search_client):
    search_client.es.search = AsyncMock(side_effect=Exception("ES connection error"))
    
    with pytest.raises(Exception) as excinfo:
        await search_client.search({"test": 1.0})
    
    assert "ES connection error" in str(excinfo.value)
