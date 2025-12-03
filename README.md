# BiohackDE-2025-dina-mcp
MVP for a DINA MCP to support LLMs search for data in DINA

Exposes MCP tools to access and query DINA's ElasticSearch index for discovering material samples.

Run with

```
uv run dina-mcp
```

Optionally, set configuration parameter `DINA_BASE_URL` via environment variable

```
DINA_BASE_URL=https://{dina_base} uv run dina-mcp
```

