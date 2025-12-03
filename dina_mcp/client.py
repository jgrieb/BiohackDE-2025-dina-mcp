"""DINA ElasticSearch client wrapper using HTTP requests."""

import requests
import logging


from .config import Config

logger = logging.getLogger(__name__)
config = Config()


def search_query(query: dict) -> dict:
    response = requests.post(
        f"{config.base_url}/api/search-api/search-ws/search?indexName=dina_material_sample_index",
        headers={"Content-Type": "application/json"},
        timeout=5,
        json={
            "query": query,
            "_source": {
                "includes": [
                    "data.id",
                    "data.type",
                    "data.attributes.materialSampleName",
                    "included.attributes.name",
                    "data.attributes.dwcOtherCatalogNumbers",
                    "data.attributes.materialSampleType",
                    "data.attributes.materialSampleState",
                    "data.attributes.effectiveScientificName",
                    "included.attributes.startEventDateTime",
                    "included.type",
                ]
            },
        },
    )
    return response.text


def get_mappings() -> dict:
    response = requests.get(
        f"{config.base_url}/api/search-api/search-ws/mapping?indexName=dina_material_sample_index",
        timeout=5,
    )
    return response.text
