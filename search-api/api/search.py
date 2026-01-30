from elasticsearch import AsyncElasticsearch

from .config import settings
from .models import SearchResult


class SearchClient:
    def __init__(self):
        self.es = AsyncElasticsearch(
            settings.ELASTICSEARCH_URL,
            verify_certs=False,
            request_timeout=30,
        )
        self.index_name = settings.ELASTICSEARCH_INDEX

    async def search(
        self, sparse_vector: dict[str, float], top_k: int = 5
    ) -> list[SearchResult]:
        if not sparse_vector:
            return []

        # Construct rank_feature query
        should_clauses = [
            {"rank_feature": {"field": f"sparse_vector.{token}", "boost": weight}}
            for token, weight in sparse_vector.items()
        ]

        query = {"bool": {"should": should_clauses}}

        try:
            response = await self.es.search(
                index=self.index_name, query=query, size=top_k
            )

            results = []
            for hit in response["hits"]["hits"]:
                source = hit["_source"]
                results.append(
                    SearchResult(
                        text=source["text"],
                        title=source["title"],
                        url=source["url"],
                        score=hit["_score"],
                    )
                )
            return results
        except Exception as e:
            # In a real app, handle connection errors etc.
            raise e

    async def close(self):
        await self.es.close()
