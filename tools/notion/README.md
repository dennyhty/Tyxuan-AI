# Notion API CLI

Single-file, stdlib-only Python CLI for the "Tyxuan Dev" Notion workspace. It is not subject to the hosted Notion MCP query quota.

- Token: env var `NOTION_TOKEN` only (internal integration secret). Never commit it. Set it in the project's cloud environment.
- Each page/database must be shared with the integration (page menu → Connections).
- Throttled to ~3 req/s; retries on 429/5xx honoring `Retry-After`.
- `NOTION_VERSION` defaults to `2025-09-03` (data sources); set `2022-06-28` for legacy behaviour.

```
python3 tools/notion/notion_cli.py me
python3 tools/notion/notion_cli.py search 樣品單
python3 tools/notion/notion_cli.py query <db-or-data-source-id> --count
python3 tools/notion/notion_cli.py create <db-id> --props '{"Name":{"title":[{"text":{"content":"x"}}]}}'
python3 tools/notion/notion_cli.py archive <page-id>   # to trash, restorable
```
