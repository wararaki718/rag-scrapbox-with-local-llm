import asyncio
import httpx
from loguru import logger
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from .config import settings
from .models import SearchResult


class LLMClient:
    def __init__(self):
        self.api_base = settings.LLM_API_BASE.rstrip("/")
        self.api_key = settings.LLM_API_KEY
        self.model_name = settings.LLM_MODEL_NAME

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(Exception),
        before_sleep=lambda retry_state: logger.warning(
            f"LLM API request failed. Retrying... (attempt {retry_state.attempt_number})"
        ),
    )
    async def _generate_with_retry(self, prompt: str) -> str:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{self.api_base}/chat/completions",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={
                    "model": self.model_name,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.7,
                },
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]

    async def generate_answer(self, query: str, contexts: list[SearchResult]) -> str:
        if not contexts:
            return "関連する情報が見つかりませんでした。"

        # チャンクごとに分割
        chunk_size = settings.LLM_CONTEXT_CHUNK_SIZE
        chunks = [
            contexts[i : i + chunk_size] for i in range(0, len(contexts), chunk_size)
        ]

        current_answer = ""
        for i, chunk in enumerate(chunks):
            context_text = "\n\n".join(
                [f"--- Source: {c.title} ({c.url}) ---\n{c.text}" for c in chunk]
            )

            if i == 0:
                # 初回の回答生成
                prompt = f"""あなたはScrapboxの知識を熟知したアシスタントです。
提供されたコンテキスト情報のみを使用して、ユーザーの質問に回答してください。
回答の最後には、参考にしたページのタイトルとURLを記載してください。

# コンテキスト
{context_text}

# ユーザーの質問
{query}
"""
            else:
                # 回答のブラッシュアップ（Refine）
                prompt = f"""あなたはScrapboxの知識を熟知したアシスタントです。
既存の回答を、新しく追加されたコンテキスト情報を用いて更新・改善してください。
必要に応じて情報を追加し、矛盾がある場合は新しい情報を優先してください。
回答の最後には、これまでに参考にしたすべてのページのタイトルとURLを記載してください。

# ユーザーの質問
{query}

# 既存の回答
{current_answer}

# 追加のコンテキスト
{context_text}
"""

            logger.info(f"Processing chunk {i+1}/{len(chunks)}...")
            current_answer = await self._generate_with_retry(prompt)

        return current_answer
