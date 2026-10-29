# Changelog

The OKstays MCP server follows semantic versioning: `serverInfo.version` in the `initialize` response, the same version
on the [official MCP Registry](https://registry.modelcontextprotocol.io) (`com.okstays/okstays`) and here.

- **Additive changes** (a new tool, a new optional parameter, a new field in results) ship in minor versions without
  notice.
- **Breaking changes** (removing or renaming a tool, a required parameter or a result field) get a major version,
  are announced here and on https://okstays.com/mcp at least 30 days before, and integration partners hear about them
  by email.
- Questions: hello@okstays.com

## 2.5.0 (live)

- New tool `plan_trip`: hotels for a multi-stop trip (stops in travel order, nights per stop, optional neighbourhood,
  start date, travel style, qualities, budget). For each stop: the best match and alternatives, the stay dates and
  links that open each hotel's page with those dates; the trip gets an indicative total.
- `search_hotels`: `tags` also accepts filter names and URL slugs ("quiet", "Reliable WiFi"), suggests the closest
  filter for an unknown one, and `district` matches typos and hotels whose address names the area.

## 2.4.0

Seven read-only tools: `get_city_overview`, `search_hotels`, `get_hotel`, `compare_hotels`, `find_similar_hotels`,
`list_cities`, `get_filters`. Hotel cards for hosts that support MCP Apps.
