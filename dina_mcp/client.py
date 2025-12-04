"""DINA ElasticSearch client wrapper using HTTP requests."""

import requests
import logging


from .config import Config

logger = logging.getLogger(__name__)
config = Config()


def search_query(queryBody: dict) -> dict:
    response = requests.post(
        f"{config.base_url}/api/search-api/search-ws/search?indexName=dina_material_sample_index",
        headers={"Content-Type": "application/json"},
        timeout=5,
        json=queryBody
    )
    return response.text


def get_mappings() -> dict:
    response = requests.get(
        f"{config.base_url}/api/search-api/search-ws/mapping?indexName=dina_material_sample_index",
        timeout=5,
    )
    return response.text
