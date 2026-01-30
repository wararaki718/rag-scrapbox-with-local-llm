import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from api.llm import GeminiClient
from api.models import SearchResult
from api.config import settings

@pytest.fixture
def gemini_client():
    with patch("google.genai.Client"):
        client = GeminiClient()
        yield client

@pytest.mark.asyncio
async def test_generate_answer_empty_contexts(gemini_client):
    result = await gemini_client.generate_answer("query", [])
    assert result == "関連する情報が見つかりませんでした。"

@pytest.mark.asyncio
async def test_generate_answer_single_chunk(gemini_client):
    # Setup
    contexts = [
        SearchResult(text="text1", title="title1", url="url1", score=1.0)
    ]
    gemini_client._generate_with_retry = AsyncMock(return_value="Answer 1")
    
    # Execute
    result = await gemini_client.generate_answer("query", contexts)
    
    # Verify
    assert result == "Answer 1"
    gemini_client._generate_with_retry.assert_called_once()
    prompt = gemini_client._generate_with_retry.call_args[0][0]
    assert "text1" in prompt
    assert "title1" in prompt
    assert "# 既存の回答" not in prompt  # 最初のチャンクなのでRefineではない

@pytest.mark.asyncio
async def test_generate_answer_multiple_chunks(gemini_client):
    # Setup: 2 chunks (chunk size is 3 by default, so we need 4 results)
    contexts = [
        SearchResult(text=f"text{i}", title=f"title{i}", url=f"url{i}", score=1.0)
        for i in range(4)
    ]
    
    # Mock return values for each call
    gemini_client._generate_with_retry = AsyncMock()
    gemini_client._generate_with_retry.side_effect = ["Initial Answer", "Refined Answer"]
    
    # Execute
    with patch("api.llm.settings.GEMINI_CONTEXT_CHUNK_SIZE", 3):
        with patch("asyncio.sleep", AsyncMock()) as mock_sleep:
            result = await gemini_client.generate_answer("query", contexts)
            
            # Verify
            assert result == "Refined Answer"
            assert gemini_client._generate_with_retry.call_count == 2
            mock_sleep.assert_called_once_with(settings.GEMINI_RPM_DELAY)
            
            # Check first call (Initial)
            first_prompt = gemini_client._generate_with_retry.call_args_list[0][0][0]
            assert "text0" in first_prompt
            assert "text2" in first_prompt
            assert "text3" not in first_prompt
            assert "# コンテキスト" in first_prompt
            
            # Check second call (Refine)
            second_prompt = gemini_client._generate_with_retry.call_args_list[1][0][0]
            assert "text3" in second_prompt
            assert "# 既存の回答" in second_prompt
            assert "Initial Answer" in second_prompt
