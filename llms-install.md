# Installing the OKstays MCP server

OKstays is a hosted, remote MCP server. There is nothing to download, build or run, and no API key or account.

1. Add this server to the MCP client's configuration, using streamable HTTP:
   ```json
   {
     "mcpServers": {
       "okstays": {
         "type": "streamableHttp",
         "url": "https://okstays.com/api/mcp"
       }
     }
   }
   ```
   Clients that use another key for the transport take `"type": "http"` (VS Code) or only `"url"` (Cursor).
2. Do not add headers, environment variables or credentials: the server needs none.
3. Check the connection by listing the tools. There should be eight, all read-only: `get_city_overview`,
   `search_hotels`, `get_hotel`, `compare_hotels`, `find_similar_hotels`, `plan_trip`, `list_cities`, `get_filters`.
4. Try it: call `list_cities` with `{"country": "Spain"}`, then `search_hotels` with `{"location": "Barcelona"}`.

If the connection fails, test the endpoint directly:
```
curl -X POST https://okstays.com/api/mcp -H 'Content-Type: application/json' -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'
```
Limits: 60 requests a minute and 2,000 a day per caller. More: https://okstays.com/mcp
