# Changelog

The OKstays MCP server follows semantic versioning: `serverInfo.version` in the `initialize` response, the same version
on the [official MCP Registry](https://registry.modelcontextprotocol.io) (`com.okstays/okstays`) and here.

- **Additive changes** (a new tool, a new optional parameter, a new field in results) ship in minor versions without
  notice.
- **Breaking changes** (removing or renaming a tool, a required parameter or a result field) get a major version,
  are announced here and on https://okstays.com/mcp at least 30 days before, and integration partners hear about them
  by email.
- Questions: hello@okstays.com

## 3.0.0 (live)

Breaking changes, released without the usual 30 days' notice because no integration depended on these fields yet:
- `get_hotel` returns a summary by default: the score breakdown, the five must-haves, the strongest signals and the
  complaints, each with its reason, in about a quarter of the length. `detail: "full"` returns every signal as before
  (`filters`), where `must_have` now appears only on the five must-haves.
- `search_hotels` and `find_similar_hotels` no longer repeat the destination's page on every hotel (`city_page`): it
  is in `see_also`, once per answer.

New:
- The user's stay on every link: `search_hotels`, `get_hotel`, `compare_hotels`, `find_similar_hotels` and
  `get_city_overview` take `checkin`, `checkout` (YYYY-MM-DD) and `adults`. Every hotel and listing link then opens on
  that stay, and the page's Book Now opens the booking site on those nights. Results say so in `stay` and `stay_note`.
- `search_hotels`: `limit` (1-10) and `page` (up to 5) for more results, with `pages` and `next_page` in the answer;
  `hotel_name` looks up a hotel the user names (typos and extra words are fine), including hotels outside the rankings,
  with the reason (`in_rankings`, `not_ranked_because`).
- `get_hotel`: `focus` adds the signals the user asked about; new fields `in_rankings` and `evidence` (what the scores
  are based on).
- Hotels scored from guest reviews carry an `evidence` line and, per signal, how many guests praised or complained
  about it (`guests`).
- Filter names: one-word names that point to a single filter work, e.g. "wifi", "bed", "ac".
- Prompts for clients that show them: `find_hotel`, `plan_my_trip`, `compare_my_hotels`, `choose_area`.

## 2.5.0

- New tool `plan_trip`: hotels for a multi-stop trip (stops in travel order, nights per stop, optional neighbourhood,
  start date, travel style, qualities, budget). For each stop: the best match and alternatives, the stay dates and
  links that open each hotel's page with those dates; the trip gets an indicative total.
- `search_hotels`: `tags` also accepts filter names and URL slugs ("quiet", "Reliable WiFi"), suggests the closest
  filter for an unknown one, and `district` matches typos and hotels whose address names the area.

## 2.4.0

Seven read-only tools: `get_city_overview`, `search_hotels`, `get_hotel`, `compare_hotels`, `find_similar_hotels`,
`list_cities`, `get_filters`. Hotel cards for hosts that support MCP Apps.
