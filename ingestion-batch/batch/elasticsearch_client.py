from typing import Any

from elasticsearch import Elasticsearch, helpers
from loguru import logger

from .config import settings


class ESClient:
    def __init__(self):
        self.es = Elasticsearch(
            settings.ELASTICSEARCH_URL,
            verify_certs=False,
            request_timeout=30,
        )
        self.index_name = settings.ELASTICSEARCH_INDEX

    def create_index(self):
        """
        インデックスを作成し、マッピングを設定する
        """
        mappings = {
            "properties": {
                "text": {"type": "text", "analyzer": "kuromoji"},
                "title": {
                    "type": "text",
                    "analyzer": "kuromoji",
                    "fields": {"keyword": {"type": "keyword"}},
                },
                "url": {"type": "keyword"},
                "updated": {"type": "date"},
                "sparse_vector": {"type": "rank_features"},
            }
        }

        try:
            # すでに存在する場合は削除して作り直す（バッチの性質上、今回はシンプルに再作成）
            if self.es.indices.exists(index=self.index_name):
                logger.info(f"Deleting existing index: {self.index_name}")
                self.es.indices.delete(index=self.index_name)

            logger.info(f"Creating index: {self.index_name}")
            self.es.indices.create(index=self.index_name, mappings=mappings)
        except Exception as e:
            logger.error(f"Failed to create index: {e}")
            if hasattr(e, 'body'):
                logger.error(f"Error body: {e.body}")
            raise e

    def bulk_index(self, documents: list[dict[str, Any]]):
        """
        ドキュメントを一括登録する
        """
        actions = [
            {
                "_index": self.index_name,
                "_source": doc
            }
            for doc in documents
        ]
        helpers.bulk(self.es, actions)
        logger.info(f"Indexed {len(documents)} documents to {self.index_name}")
