from typing import Any

import requests
from loguru import logger

from .config import settings


class ScrapboxClient:
    def __init__(self):
        self.project = settings.SCRAPBOX_PROJECT
        self.sid = settings.SCRAPBOX_SID
        self.base_url = f"https://scrapbox.io/api/pages/{self.project}"
        self.headers = {}
        if self.sid:
            self.headers["Cookie"] = f"connect.sid={self.sid}"

    def get_all_pages(self) -> list[dict[str, Any]]:
        """
        全ページのメタデータを取得し、詳細を取得する
        """
        logger.info(f"Fetching all pages from Scrapbox project: {self.project}")
        
        # まずは一覧を取得 (limit=1000としたが、大規模な場合はページネーションが必要)
        response = requests.get(f"{self.base_url}?limit=1000", headers=self.headers)
        response.raise_for_status()
        data = response.json()
        
        pages = []
        for page_meta in data.get("pages", []):
            try:
                page_detail = self.get_page(page_meta["title"])
                pages.append(page_detail)
            except Exception as e:
                logger.error(f"Failed to fetch page {page_meta['title']}: {e}")
                
        return pages

    def get_page(self, title: str) -> dict[str, Any]:
        """
        特定のページの詳細を取得する
        """
        url = f"{self.base_url}/{requests.utils.quote(title)}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
