# OKstays MCP tools

Endpoint: `https://okstays.com/api/mcp` (streamable HTTP, no authentication). Setup: [README.md](README.md).

Every tool is **Read**: it retrieves information without changing data, account state or permissions, and needs no
sign-in. All tools carry the MCP annotations `readOnlyHint: true`, `destructiveHint: false`, `idempotentHint: true`,
`openWorldHint: false`. Results are JSON text. Prices are indicative nightly prices in USD. Hotel ids are numeric
strings from search results. Each hotel comes with a link to its page on okstays.com. Hotels, apartments and hostels are
ranked apart; every place carries its `kind` (`hotels`, `apartments`, `hostels` or `other`).

**The user's stay:** `search_hotels`, `get_hotel`, `compare_hotels`, `find_similar_hotels` and `get_city_overview` also
take `checkin` and `checkout` (YYYY-MM-DD, 1-30 nights, check-in today or later) and `adults` (1-8). Every hotel and
listing link in the answer then carries that stay, and the page's Book Now opens the booking site on those nights; the
answer repeats it in `stay` and `stay_note`. Prices stay indicative, not quotes for those dates.

## get_city_overview

**Access:** Read. A destination at a glance.

**Inputs:** `location` (string, required): destination name or slug, e.g. `Lisbon`; the stay inputs. An area of a grouped
destination (`Canggu`, `Positano`, `Maafushi`) gives that destination's overview, with a `location_note`.

**Outputs:** hotels scored, average Comfort Score, median price, where the destination's hotels beat and trail the
average hotel, the best neighbourhoods, the travel styles it suits, its top hotels (id, name, Comfort Score, price) and
its ranked places by kind (`ranked_by_kind`), the city tax at a 4-star hotel for 2 adults (`city_tax`, with
`city_tax_study`) and `when_to_go`: `best` (pleasant months), `sleep` (months with nights below 20°C), `quiet` (where
official visitor figures exist) and `typical_weather` (each month's high and low in °C and rainy days).


`where_to_stay` (where okstays.com has a guide): `picks` (for a first visit, quiet nights, nightlife, families and value: the area and why, as the guide words it), `areas` (up to 10: `places`, `typical_price_usd`, `comfort_score`, `km_from_centre`, `hotels_on_loud_streets_percent`, `bars_within_300m_of_typical_hotel`, `sights_within_500m_of_typical_hotel`, `traits`, `top_places`) and `guide`, the page's link. Area names work as `search_hotels`' `district`.
## search_hotels

**Access:** Read. Up to 10 hotels per page in a destination, ranked by Comfort Score or by a travel style's score, or
the hotels matching a name.

**Inputs:**
- `location` (string, required): a destination, or an area of a grouped one (`Canggu` or `Ubud` in Bali, `Positano`,
  `Maafushi`), which lists that area's places and adds a `location_note`
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
- `property_type` (string): `hotels` (default; includes guest houses, B&Bs, aparthotels and resorts), `apartments`
  (includes holiday homes, villas and homestays), `hostels` or `any`; the `long-stays` travel style defaults to `any`
- `hotel_name` (string): look up a hotel by name in this destination (part of the name or a typo works), including
  hotels outside the rankings; the other filters are then ignored
- the stay inputs

**Outputs:** the destination, the kind of stay searched, what the list is ranked by, the number of matches, and up to
10 places, each with id, name, `kind`, Comfort Score, price, guest rating and review count (both null unless a booking
site confirmed them), district, strengths, caveats, the city tax where we know it (`city_tax`, in the currency it's
charged in) and a link to its page; the
destination's page comes once, in `see_also`. When relevant, the
hotels also carry the travel style's score, the distance in km or comfort points per $100. With more than one page:
`pages` (current, total) and `next_page`. Hotels scored from guest reviews carry `evidence`. With `hotel_name`: the
matching hotels, each with `in_rankings` and, when false, `not_ranked_because`.

## get_hotel

**Access:** Read. One hotel: a summary by default, every signal on request.

**Inputs:** `hotel_id` (string, required); `detail` (`summary`, the default, or `full`: every signal, about four times
longer); `focus` (array of filter ids or names the user asked about, e.g. `["quiet", "wifi"]`); the stay inputs.

**Outputs:** name, location, district, address, description, image, price, guest rating and review count (null unless
a booking site confirmed them), `kind`, Comfort Score (with `comfort_score_note` when few reviews lowered it), rank among places of its kind in its destination (`city_rank`,
out of `city_hotels`, and `rank_line`, e.g. "#1 hotel for comfort in Barcelona"), whether it is in the rankings
(`in_rankings`), what the scores are based on (`evidence`), the Comfort Score's parts (`score_breakdown`: `must_haves`,
`sleep_room`, `service`, `extras`, `location`), the five must-haves, the strongest signals, the `focus` signals and the
complaints, each with a one-sentence explanation, the city tax with its notes (`city_tax`), and links. `detail:
"full"` lists every filter's score instead
(`filters`, with `must_have` on the five must-haves).

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

**Outputs:** every comfort filter (id, name, description, category), the Comfort Score's parts with their weights
(`comfort_score_parts`) and every travel style.

## plan_trip

**Access:** Read. Hotels for a multi-stop trip.

**Inputs:** `stops` (array of 1-8, required: `location`, `nights` 1-30, optional `district`), `start_date`
(YYYY-MM-DD), `persona`, `property_type` (as in `search_hotels`), `tags`, `max_price`, `min_score`, `adults` (1-8,
default 2), `alternatives` (0-3, default 2).

**Outputs:** for each stop, the best match and alternatives with the stay dates, prices, city tax and links that open
each hotel's page with those dates, and, with dates, the stop's `typical_weather` in its check-in month; an indicative
total for the trip.

## Prompts

For clients that show MCP prompts (Claude, Claude Desktop, VS Code): `find_hotel` (destination; optional what matters,
budget, dates, guests), `plan_my_trip` (stops; optional start date, travel style, budget), `compare_my_hotels`
(hotel names; optional city) and `choose_area` (destination; optional what matters). Each returns a user message that
asks for the right tools with those details. Clients with argument completion (`completion/complete`) suggest
destinations, travel styles and the next stop of a trip as the user types.

## Hotel cards (MCP Apps)

In hosts that render MCP Apps (Claude, ChatGPT and others), `search_hotels`, `find_similar_hotels`, `compare_hotels`,
`get_city_overview` and `plan_trip` also show hotel cards (`ui://okstays/hotel-cards-v5`): photo, Comfort Score, price,
area, top strengths, the main guest complaint and a link to the hotel's page. The model reads the same JSON text as
always; the cards' data travels in the result's `_meta` and never reaches the model.
- Lists show up to 8 cards; sort buttons reorder the hotels shown without a tool call.
- Where the host offers full screen: every loaded hotel in a grid, and Show more, which calls `search_hotels` for the
  next page through the host (the tool is visible to the model and the app). The host is told which hotels the user
  loaded (`ui/update-model-context`).
- `compare_hotels` can show a table: Comfort Score, price, guest rating, area, the four parts and the main differences.

## Errors and limits

- Bad input, or a destination or hotel we don't cover: an MCP tool error (`isError: true`) with a plain explanation,
  e.g. `Unknown location "Atlantis". Use list_cities to see coverage.`
- Per caller: 60 tool calls a minute and 2,000 a day (400 a day for `get_hotel` and `compare_hotels`). Over a limit,
  a tool error says when to retry.
- Support: hello@okstays.com. Security reports: [SECURITY.md](SECURITY.md).
