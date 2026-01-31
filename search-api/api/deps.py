from .encoder import SpladeClient
from .llm import LLMClient
from .search import SearchClient

# Singleton-like instances
_search_client = SearchClient()
_splade_client = SpladeClient()
_llm_client = LLMClient()


def get_search_client():
    return _search_client


def get_splade_client():
    return _splade_client


def get_llm_client():
    return _llm_client
