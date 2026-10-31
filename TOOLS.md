# OKstays MCP tools

Endpoint: `https://okstays.com/api/mcp` (streamable HTTP, no authentication). Setup: [README.md](README.md).

Every tool is **Read**: it retrieves information without changing data, account state or permissions, and needs no
sign-in. All tools carry the MCP annotations `readOnlyHint: true`, `destructiveHint: false`, `idempotentHint: true`,
`openWorldHint: false`. Results are JSON text. Prices are indicative nightly prices in USD. Hotel ids are numeric
strings from search results. Each hotel comes with a link to its page on okstays.com.

**The user's stay:** `search_hotels`, `get_hotel`, `compare_hotels`, `find_similar_hotels` and `get_city_overview` also
take `checkin` and `checkout` (YYYY-MM-DD, 1-30 nights, check-in today or later) and `adults` (1-8). Every hotel and
listing link in the answer then carries that stay, and the page's Book Now opens the booking site on those nights; the
answer repeats it in `stay` and `stay_note`. Prices stay indicative, not quotes for those dates.

## get_city_overview

**Access:** Read. A destination at a glance.

**Inputs:** `location` (string, required): destination name or slug, e.g. `Lisbon`; the stay inputs.

**Outputs:** hotels scored, average Comfort Score, median price, where the destination's hotels beat and trail the
average hotel, the best neighbourhoods, the travel styles it suits, and its top hotels (id, name, Comfort Score, price).

## search_hotels

**Access:** Read. Up to 10 hotels per page in a destination, ranked by Comfort Score or by a travel style's score, or
the hotels matching a name.

**Inputs:**
- `location` (string, required)
- `persona` (string): a travel style, e.g. `deep-sleep`, `digital-nomad`, `family`, `romantic`, `business`, `luxury`
  (`get_filters` lists them all)
- `tags` (array of strings): filters every hotel must score 8+ on, by id or name, e.g. `["soundproofing", "peaceful_quiet"]`
- `min_score` (number, 0-10): minimum Comfort Score
- `max_price` (number): maximum price per night in USD
- `district` (string): a neighbourhood
- `near_lat`, `near_lng` (numbers): a landmark or address the user names (not the user's own location), with
  `radius_km` (number, default 3)
- `sort_by` (string): `best` (default), `cheapest`, `priciest`, `value` or `nearest`
- `limit` (integer 1-10, default 10) and `page` (integer 1-5, default 1)
- `hotel_name` (string): look up a hotel by name in this destination (part of the name or a typo works), including
  hotels outside the rankings; the other filters are then ignored
- the stay inputs

**Outputs:** the destination, what the list is ranked by, the number of matches, and up to 10 hotels, each with id,
name, Comfort Score, price, guest rating, review count, district, strengths, caveats and a link to its page; the
destination's page comes once, in `see_also`. When relevant, the
hotels also carry the travel style's score, the distance in km or comfort points per $100. With more than one page:
`pages` (current, total) and `next_page`. Hotels scored from guest reviews carry `evidence`. With `hotel_name`: the
matching hotels, each with `in_rankings` and, when false, `not_ranked_because`.

## get_hotel

**Access:** Read. One hotel: a summary by default, every signal on request.

**Inputs:** `hotel_id` (string, required); `detail` (`summary`, the default, or `full`: every signal, about four times
longer); `focus` (array of filter ids or names the user asked about, e.g. `["quiet", "wifi"]`); the stay inputs.

**Outputs:** name, location, district, address, description, image, price, guest rating, review count, Comfort Score,
rank in its destination, whether it is in the rankings (`in_rankings`), what the scores are based on (`evidence`),
score breakdown, the five must-haves, the strongest signals, the `focus` signals and the complaints, each with its
explanation, and links. `detail: "full"` lists every filter's score instead (`filters`, with `must_have` on the five
must-haves). Scores from guest reviews also say how many guests praised or complained (`guests`).

## compare_hotels

**Access:** Read. Two to four hotels side by side.

**Inputs:** `hotel_ids` (array of 2-4 strings, required); the stay inputs.

**Outputs:** each hotel's Comfort Score, score breakdown, price, strengths, caveats and links; the filters where they
differ most; a verdict: best comfort, cheapest, best value.

## find_similar_hotels

**Access:** Read. Hotels in the same destination with the closest comfort profile.

**Inputs:** `hotel_id` (string, required), `cheaper_only` (boolean), `max_price` (number), `limit` (integer 1-10,
default 5); the stay inputs.

**Outputs:** the reference hotel and the most similar hotels, each with Comfort Score, price and a link to its page;
the destination's page in `see_also`.

## list_cities

**Access:** Read. The destinations covered.

**Inputs:** `country` (string, optional).

**Outputs:** each destination with its hotel count.

## get_filters

**Access:** Read. What `search_hotels` accepts.

**Inputs:** none.

**Outputs:** every comfort filter (id, name, description, category) and every travel style.

## plan_trip

**Access:** Read. Hotels for a multi-stop trip.

**Inputs:** `stops` (array of 1-8, required: `location`, `nights` 1-30, optional `district`), `start_date`
(YYYY-MM-DD), `persona`, `tags`, `max_price`, `min_score`, `adults` (1-8, default 2), `alternatives` (0-3, default 2).

**Outputs:** for each stop, the best match and alternatives with the stay dates, prices and links that open each
hotel's page with those dates; an indicative total for the trip.

## Prompts

For clients that show MCP prompts (Claude, Claude Desktop, VS Code): `find_hotel` (destination; optional what matters,
budget, dates, guests), `plan_my_trip` (stops; optional start date, travel style, budget), `compare_my_hotels`
(hotel names; optional city) and `choose_area` (destination; optional what matters). Each returns a user message that
asks for the right tools with those details.

## Errors and limits

- Bad input, or a destination or hotel we don't cover: an MCP tool error (`isError: true`) with a plain explanation,
  e.g. `Unknown location "Atlantis". Use list_cities to see coverage.`
- Per caller: 60 tool calls a minute and 2,000 a day (400 a day for `get_hotel` and `compare_hotels`). Over a limit,
  a tool error says when to retry.
- Support: hello@okstays.com. Security reports: [SECURITY.md](SECURITY.md).
