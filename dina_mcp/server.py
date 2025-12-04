"""MCP server for DINA CMS."""

import logging

from mcp.server.fastmcp import FastMCP
from typing import Any

from .client import search_query, get_mappings
from .config import Config


logger = logging.getLogger(__name__)

# Initialize the MCP server
config = Config()
mcp = FastMCP("dina-mcp", host=config.host)


@mcp.tool(
    name="search_material_samples",
    title="Search Material Samples",
    description="""Search for a material samples/ physical specimen records in in the DINA Database using ElasticSearch query syntax.

    Build an ElasticSearch query JSON object for free text queries.
    Optionally combined with additional constraints.
    The mandatory parameter "queryBody" must be a json object/ python dictonary follow ElasticSearch query syntax. For example,
    for a simple free text query looking for "Haematostaphis barter" pass the following JSON:
    {
        "query": {
            "bool": {
                "must": [
                    {
                        "simple_query_string": {
                            "query": "Haematostaphis barter",
                            "fields": ["*"],
                        }
                    }
                ]
            }
        },
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
        }
    }

    For a more refined query with additional constraints, for example looking only for recors in a collection with the
    name "Herbarium Senckenbergianum (FR) - Plantae", the JSON can be extended accordingly:
    {
        "query": {
        "bool": {
            "must": [
            {
                "nested": {
                "path": "included",
                "query": {
                    "bool": {
                    "must": [
                        {
                        "term": {
                            "included.attributes.name.keyword": "Herbarium Senckenbergianum (FR) - Plantae"
                        }
                        },
                        {
                        "term": {
                            "included.type": "collection"
                        }
                        }
                    ]
                    }
                }
                }
            },
            {
                "simple_query_string": {
                "query": "Haematostaphis barter",
                "fields": [
                    "*"
                ]
                }
            }
            ]
        }
        },
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
        }
    }

    The "_source" parameter defines which fields to return. A good standard configuration
    for "_source" is included in the examples above. Use this for standard material sample queries,
    but adapt or remove "_source" from the queryBody according to the requirements.

    More advanced query like faceted search using the "aggs" parameter (alongside "query") are also supported.

    The result returns the Elasticsearch response in json. Retrieve the count and the
    id(s) of the record.
    """,
)
async def search_objects(
    queryBody: dict[str, Any],
) -> str:
    """Search for digital objects in the Cordra repository with pagination support.

    Args:
        queryBody: The search query JSON object as in the examples above

    Returns:
        JSON object containing the record data
    """
    res = search_query(queryBody)
    return res


@mcp.tool(
    name="get_search_index_mappings",
    title="Get search index mappings",
    description="""
    Retrieve the mappings from the ElasticSearch index of material samples.
    This will return a JSON dict with the current mappings.
    This function should be x^called before building the query and
    calling the search_material_samples tool, because the query has to be build
    based on the mappings.
    """,
)
async def get_search_index_mappings() -> str:
    """Search for digital objects in the Cordra repository with pagination support.

    Args:

    Returns:
        JSON object containing the ElasticSearch mappings
    """
    res = get_mappings()
    return res


def main() -> None:
    """Main entry point for the MCP server."""
    logger.warning(
        "Initializing DINA MCP server "
        + f" with DINA base { config.base_url }"
    )
    mcp.run(transport="streamable-http")


if __name__ == "__main__":
    main()
