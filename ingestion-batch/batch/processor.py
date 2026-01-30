from typing import Any

import requests
from loguru import logger

from .config import settings


class Processor:
    def __init__(self):
        self.splade_url = settings.SPLADE_API_URL
        self.chunk_size = settings.CHUNK_SIZE
        self.chunk_overlap = settings.CHUNK_OVERLAP

    def split_text(self, text: str) -> list[str]:
        """
        テキストをチャンクに分割する。
        簡易的な実装として、一定の文字数で分割（オーバーラップあり）を行う。
        """
        if not text:
            return []
            
        chunks = []
        start = 0
        while start < len(text):
            end = start + self.chunk_size
            chunks.append(text[start:end])
            if end >= len(text):
                break
            start += (self.chunk_size - self.chunk_overlap)
        return chunks

    def get_sparse_vector(self, text: str) -> dict[str, float]:
        """
        SPLADE API を叩いてスパースベクトルを取得する
        """
        try:
            response = requests.post(self.splade_url, json={"text": text})
            response.raise_for_status()
            return response.json()["sparse_vector"]
        except Exception as e:
            logger.error(f"Failed to get sparse vector: {e}")
            return {}

    def process_page(self, page: dict[str, Any]) -> list[dict[str, Any]]:
        """
        Scrapboxの1ページを複数のチャンク・ドキュメントに変換する
        """
        title = page.get("title", "")
        updated = page.get("updated", 0) * 1000  # ms に変換
        project_name = settings.SCRAPBOX_PROJECT
        page_url = f"https://scrapbox.io/{project_name}/{requests.utils.quote(title)}"
        
        # 行を結合して全文を作成
        lines = [line.get("text", "") for line in page.get("lines", [])]
        full_text = "\n".join(lines)
        
        chunks = self.split_text(full_text)
        
        processed_docs = []
        for i, chunk in enumerate(chunks):
            logger.info(f"Encoding chunk {i+1}/{len(chunks)} of page: {title}")
            sparse_vector = self.get_sparse_vector(chunk)
            
            if not sparse_vector:
                continue
                
            doc = {
                "title": title,
                "text": chunk,
                "url": page_url,
                "updated": updated,
                "sparse_vector": sparse_vector
            }
            processed_docs.append(doc)
            
        return processed_docs
