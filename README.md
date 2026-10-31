# OKstays MCP server

[![MCP health](https://github.com/okstays/okstays-mcp/actions/workflows/health.yml/badge.svg)](https://github.com/okstays/okstays-mcp/actions/workflows/health.yml)

Find hotels you'll actually sleep well in. OKstays scores 30,000+ hotels in 80+ destinations on 67 comfort signals
(efficient AC, comfy beds, real soundproofing, quiet nights, spacious rooms, recent renovations, safe and walkable neighbourhoods and more) and combines
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

All eight tools only read data. Inputs, outputs and access level for each: [TOOLS.md](TOOLS.md).

| Tool | What it does |
|---|---|
| `get_city_overview` | A destination at a glance: hotels scored, average Comfort Score, median price, what its hotels do best and worst, the best neighbourhoods, the travel styles it suits |
| `search_hotels` | Up to 10 hotels per page in a city ranked by Comfort Score, optionally for a travel style (deep sleep, digital nomad, family, romantic, business, solo, luxury, budget, avoid the crowds), required qualities, price, neighbourhood or distance from a landmark; or a hotel looked up by name |
| `get_hotel` | One hotel: score breakdown, what the scores are based on, the must-haves, strengths and complaints with their explanations (every signal on request), price, link |
| `compare_hotels` | Two to four hotels side by side, with a verdict: best comfort, cheapest, best value |
| `find_similar_hotels` | Hotels in the same city that score most like a given one, optionally cheaper |
| `list_cities` | The destinations covered, with hotel counts, optionally for one country |
| `get_filters` | Every comfort filter and travel style usable in `search_hotels` |
| `plan_trip` | Hotels for a multi-stop trip (e.g. Lisbon 4 nights, Porto 3, Madrid 5): the best match and alternatives for each stop, the stay dates and an indicative total, with links that open each hotel's page with those dates |

Give your assistant your dates and the number of guests, and every hotel link it shows opens on that stay: Book Now on
the hotel's page then books those nights. Clients that show MCP prompts (Claude, Claude Desktop, VS Code) also get four
ready-made ones: Find a comfortable hotel, Plan a multi-stop trip, Compare hotels, Choose where to stay.

## Example prompts

- Which neighbourhoods in Lisbon have the most comfortable hotels?
- Find a quiet hotel in Porto under $200 a night
- Hotels in Bangkok with efficient AC and soundproof rooms
- Compare the top two and tell me which is better value
- Find something like the first one, but cheaper
- Plan hotels for Lisbon 4 nights, Porto 3 and Madrid 5 from 10 May
- Is the Pestana Palace in Lisbon quiet? We're there 12 to 15 March, two of us

## Data, privacy and limits

- Results link to each hotel's page on okstays.com, with photos, a map and prices. Prices are indicative rates for
  two adults on a sample date. OKstays earns a commission when people book through the booking links on its website;
  this never affects the rankings, and tool results contain no affiliate links.
- Fair use: 60 requests a minute and 2,000 a day per caller. Each tool call and prompt is logged (tool or prompt,
  search parameters, client name, a hashed caller id) for 30 days for limits and abuse prevention: https://okstays.com/privacy
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
- the logo (`logo-400.png`);
- [`.github/workflows/health.yml`](.github/workflows/health.yml), a daily check that the live server answers (the badge
  above).

The configuration files and documentation are MIT-licensed ([LICENSE](LICENSE)); the OKstays name and logo are not.
