# Changelog

The OKstays MCP server follows semantic versioning: `serverInfo.version` in the `initialize` response, the same version
on the [official MCP Registry](https://registry.modelcontextprotocol.io) (`com.okstays/okstays`) and here.

- **Additive changes** (a new tool, a new optional parameter, a new field in results) ship in minor versions without
  notice.
- **Breaking changes** (removing or renaming a tool, a required parameter or a result field) get a major version,
  are announced here and on https://okstays.com/mcp at least 30 days before, and integration partners hear about them
  by email.
- Questions: hello@okstays.com

## 4.2.1 (live)

- Fix: an area of a grouped destination works as `location`: "Canggu" or "Ubud" in Bali, "Phuket Town" or "Rawai" in
  Phuket, "Positano" on the Amalfi Coast, "Oia" in Santorini, "Maafushi" or "Malé" in the Maldives. Canggu and Phuket
  Town became areas of Bali and Phuket on 3 November 2026 and answered "Unknown location" since. `search_hotels` lists
  that area's places and says so in `location_note`; `get_city_overview` gives the destination's overview with the
  same note; `plan_trip` stops can name areas.

## 4.2.0

All additive.
- City tax: hotel results (`search_hotels`, `get_hotel`, `compare_hotels`, `plan_trip` picks) carry `city_tax` where
  our research covers the place, worded as on its OKstays page and in the currency the tax is charged in, e.g. "City
  tax: about €6 a night for 2 adults, paid at the hotel". `get_hotel` adds the notes (exemptions, night caps, taxes
  on hold).
- `get_city_overview` adds `city_tax` (a 4-star hotel, 2 adults, as on the tourist-tax study) with `city_tax_study`,
  and `when_to_go`: the pleasant months, the months with nights below 20°C, the quietest months where official visitor
  figures exist, and the typical weather of every month (high, low, rainy days).
- `plan_trip`: each dated stop gets its `typical_weather` in the check-in month.

## 4.1.0

- New Comfort Score weights, with the filter categories now the score's parts: Comfort & Essentials 60% (the five
  must-haves 30%, sleep and room 30%), Perks & Facilities 15%, Service & Hospitality 15% and Access & Convenience 10%.
  Style & Value (renamed from Vibe & Atmosphere) is not part of the score. Within each part, a quality counts by how
  much it matters to guests and by how many reviews mention it at that place; one nobody mentions counts as at a
  typical place, at half weight, so a single review never decides a part.
- The `score_breakdown` keys stay the same; their names in `get_filters` `comfort_score_parts` are now "Must-haves",
  "Sleep & room", "Service & Hospitality", "Perks & Facilities" (`extras`) and "Access & Convenience" (`location`).
- `get_filters` groups the filters by these categories: Service & Hospitality now holds staff and services (12
  qualities), and eleven filters changed category (for example quiet and safe area are in Comfort & Essentials, value
  for money is in Style & Value).
- The Comfort Score and travel-style scores are shown with two decimals everywhere, the hotel cards included (cards
  resource `ui://okstays/hotel-cards-v4`). Signal scores and guest ratings keep one decimal.
- The 8+ listing bar no longer rounds: a place needs a score of 8.00 or more (a 7.95 used to count as 8.0).
- Lists sort by the score as shown, highest first; ties go to the place more guests reviewed. In 4.0.0 the order also
  weighed how many guests reviewed each place, which could put a 9.30 above a 9.31.

## 4.0.0

Breaking changes, released without the usual 30 days' notice because no integration depended on these fields yet:
- `score_breakdown` keys are now `must_haves`, `sleep_room`, `service`, `extras` and `location` (were `must_haves`,
  `comfort`, `perks`, `access` and `service`): the Comfort Score is built from these parts.
- The per-signal `guests` counts (praise, complaints) are removed: on hotels with thousands of reviews, "5 praise, 3
  complaints" read as five reviews.

New and changed:
- Hotels, apartments and hostels are ranked apart: `property_type` on `search_hotels` and `plan_trip` (`hotels` by
  default, `apartments`, `hostels` or `any`; the `long-stays` travel style defaults to `any`), and every place carries
  `kind`. Rank lines follow the kind ("#1 hotel for comfort in Barcelona"); `city_rank` and `city_hotels` count within it.
- Rankings weigh how many guests reviewed each place, so a high score from a handful of reviews doesn't outrank one
  backed by hundreds. Complaints come in order of importance.
- All five must-haves keep a place out of the rankings when guests keep reporting problems with them.
- Travel-style scores are half the Comfort Score and half how well the place fits the style.
- `get_city_overview`: `top_hotels` lists hotels only; `ranked_by_kind` gives the ranked places of each kind.
- `get_filters` adds `comfort_score_parts` (id, name, weight).
- Evidence lines say what the scores come from without review counts, and flag places with little evidence so far.
- Every explanation is one plain sentence.
- `guest_rating` and `reviews` are null unless a booking site confirmed them; impossible prices are null.
- Faster first answers for large destinations.

## 3.1.0

- Every tool has a display title, and its description says when to use it and what it returns.
- Hotel links also carry `via=mcp`, so okstays.com still recognises them after ChatGPT replaces `utm_source` with its own.
- `get_hotel` no longer shows hotel cards. In ChatGPT, one card area per answer is redrawn by every call that has cards,
  so the last hotel looked up kept replacing the list. Lists, comparisons, similar hotels, destination overviews and
  trips keep their cards.
- The hotel cards also declare ChatGPT's own content and link policy (`openai/widgetCSP`).
- `get_hotel` adds `city_hotels`, the number of hotels its `city_rank` is out of.
- An unexpected failure returns a tool error that says what to try, instead of a bare JSON-RPC error.

## 3.0.0

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
