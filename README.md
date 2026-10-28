# OKstays MCP server

Find hotels you'll actually sleep well in. OKstays scores 30,000+ hotels in 80+ destinations on 67 comfort signals
(quiet rooms, bed comfort, shower, WiFi, air conditioning, cleanliness, neighbourhood safety and more) and combines
them into one Comfort Score from 0 to 10. Five must-haves (clean, comfy beds, good shower, bug-free, safe area) weigh
40%, and a hotel that fails one is never ranked. Hotels can't pay to be ranked.

This is a hosted, read-only MCP server. There is nothing to install and no account or API key.

- **Endpoint:** `https://okstays.com/api/mcp` (streamable HTTP)
- **Authentication:** none
- **Documentation:** https://okstays.com/mcp
- **Website:** https://okstays.com

## Connect

**Claude (web and desktop):** Customize → Add → Add custom connector. Name it OKstays, paste
`https://okstays.com/api/mcp` as the server URL, no sign-in, then connect and allow the tools. Works on every Claude
plan, including Free.

**Claude Code:**
```
claude mcp add --transport http okstays https://okstays.com/api/mcp
```

**ChatGPT (web):** Connectors → Add → Add custom MCP server. Name it OKstays, paste `https://okstays.com/api/mcp`,
choose No authentication, create it and connect. In a chat, pick OKstays (or type `@OKstays`).

**Cursor** (`~/.cursor/mcp.json`):
```json
{
  "mcpServers": {
    "okstays": { "url": "https://okstays.com/api/mcp" }
  }
}
```

**VS Code** (`.vscode/mcp.json`):
```json
{
  "servers": {
    "okstays": { "type": "http", "url": "https://okstays.com/api/mcp" }
  }
}
```

**Cline** (MCP settings):
```json
{
  "mcpServers": {
    "okstays": { "type": "streamableHttp", "url": "https://okstays.com/api/mcp" }
  }
}
```

**Any client, by hand:**
```
curl -X POST https://okstays.com/api/mcp -H 'Content-Type: application/json' -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'
```

## Tools

All seven tools only read data.

| Tool | What it does |
|---|---|
| `get_city_overview` | A destination at a glance: hotels scored, average Comfort Score, median price, what its hotels do best and worst, the best neighbourhoods, the travel styles it suits |
| `search_hotels` | Up to 10 hotels in a city ranked by Comfort Score, optionally for a travel style (deep sleep, digital nomad, family, romantic, business, solo, luxury, budget, avoid the crowds), required qualities, price, neighbourhood or distance from a landmark |
| `get_hotel` | One hotel in full: score breakdown, every signal's score with its explanation, caveats, price, link |
| `compare_hotels` | Two to four hotels side by side, with a verdict: best comfort, cheapest, best value |
| `find_similar_hotels` | Hotels in the same city that score most like a given one, optionally cheaper |
| `list_cities` | The destinations covered, with hotel counts, optionally for one country |
| `get_filters` | Every comfort filter and travel style usable in `search_hotels` |

## Example prompts

- Which neighbourhoods in Lisbon have the most comfortable hotels?
- Find a quiet hotel in Porto under $200 a night
- Best hotels in Tokyo for digital nomads
- Compare the top two and tell me which is better value
- Find something like the first one, but cheaper

## Data, privacy and limits

- Results link to each hotel's page on okstays.com, with photos, a map and prices. Prices are indicative rates for
  two adults on a sample date. OKstays earns a commission when people book through the booking links on its website;
  this never affects the rankings, and tool results contain no affiliate links.
- Fair use: 60 requests a minute and 2,000 a day per caller. Each tool call is logged (tool, search parameters,
  client name, a hashed caller id) for 30 days for limits and abuse prevention: https://okstays.com/privacy
- Terms: https://okstays.com/terms
- Support: hello@okstays.com

## About this repository

The server runs on OKstays' own infrastructure; its code isn't public. This repository holds what MCP directories and
clients need:
- this README and [`llms-install.md`](llms-install.md), for people and agents that set servers up;
- [`server.json`](server.json), published to the [official MCP Registry](https://registry.modelcontextprotocol.io)
  as `com.okstays/okstays`;
- [`gemini-extension.json`](gemini-extension.json) (Gemini CLI) and [`.cursor-plugin/plugin.json`](.cursor-plugin/plugin.json)
  with [`mcp.json`](mcp.json) (Cursor), which only point those clients at the endpoint;
- the logo (`logo-400.png`).

The configuration files and documentation are MIT-licensed ([LICENSE](LICENSE)); the OKstays name and logo are not.
