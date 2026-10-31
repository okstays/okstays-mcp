"""Checks that the public OKstays MCP server answers like it should: the handshake, the tool list, a real search, one
hotel's details, the hotel cards and the prompts. Any failure exits non-zero, so the GitHub Actions run fails and
GitHub emails the repository owner. Standard library only.

    python3 .github/health_check.py [endpoint]
"""
import json
import sys
import urllib.request

ENDPOINT = sys.argv[1] if len(sys.argv) > 1 else "https://okstays.com/api/mcp"
# OKstays' usage report leaves this caller out: it is a check, not someone planning a trip
USER_AGENT = "okstays-health-check/1 (+https://github.com/okstays/okstays-mcp)"
_ids = iter(range(1, 100))


def rpc(method, params=None):
    body = json.dumps({"jsonrpc": "2.0", "id": next(_ids), "method": method, "params": params or {}}).encode()
    req = urllib.request.Request(ENDPOINT, data=body, headers={
        "Content-Type": "application/json", "Accept": "application/json, text/event-stream", "User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=60) as resp:
        answer = json.loads(resp.read())
    if "error" in answer:
        raise AssertionError(f"{method}: {answer['error']}")
    return answer["result"]


def tool(name, arguments):
    result = rpc("tools/call", {"name": name, "arguments": arguments})
    text = result["content"][0]["text"]
    if result.get("isError"):
        raise AssertionError(f"{name}: {text}")
    return json.loads(text)


def main():
    init = rpc("initialize", {"protocolVersion": "2025-06-18", "capabilities": {},
                              "clientInfo": {"name": "okstays-health-check", "version": "1"}})
    version = init["serverInfo"]["version"]
    tools = rpc("tools/list")["tools"]
    names = {t["name"] for t in tools}
    missing = {"search_hotels", "get_hotel", "compare_hotels", "plan_trip", "get_city_overview"} - names
    assert not missing, f"tools missing: {sorted(missing)}"

    found = tool("search_hotels", {"location": "Lisbon", "limit": 3})
    hotels = found["hotels"]
    assert hotels, "search_hotels returned no hotels for Lisbon"
    assert all(h["page"].startswith("https://okstays.com/hotel/") for h in hotels), "a hotel link doesn't point to okstays.com"
    hotel = tool("get_hotel", {"hotel_id": hotels[0]["id"]})
    assert isinstance(hotel.get("comfort_score"), (int, float)), "get_hotel has no Comfort Score"

    ui = next((t["_meta"]["ui"]["resourceUri"] for t in tools if (t.get("_meta") or {}).get("ui")), None)
    assert ui, "no tool declares the hotel cards"
    cards = rpc("resources/read", {"uri": ui})["contents"][0]["text"]
    assert "<html" in cards.lower(), "the hotel cards resource isn't HTML"
    prompts = [p["name"] for p in rpc("prompts/list").get("prompts", [])] if "prompts" in init.get("capabilities", {}) else []

    print(f"OK: OKstays MCP {version}, {len(tools)} tools, {len(prompts)} prompts, Lisbon search -> "
          f"{hotels[0]['name']} ({hotels[0]['comfort_score']}), cards {ui}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:   # one plain line in the run log and in GitHub's failure email
        print(f"FAILED: {type(e).__name__}: {e}")
        sys.exit(1)
