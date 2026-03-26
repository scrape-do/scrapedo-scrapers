import requests
from urllib.parse import quote
import json

token = "<your_token>"
keyword = "coffee"
timeframe = "today 3-m"
geo = ""  # "" = worldwide; "US", "GB", "TR" = country; "US-CA" = state
category = 0  # 0 = all; 3 = Business, 71 = Science/Tech
property_filter = ""  # "" = Web, "youtube", "news", "images", "froogle"
hl = "en-GB"
tz = -180  # minutes offset: -180 = UTC+3, 0 = UTC

# Timeframe options:
#   "now 1-H"    - past hour       "now 4-H"    - past 4 hours
#   "now 1-d"    - past day        "now 7-d"    - past 7 days
#   "today 1-m"  - past 30 days    "today 3-m"  - past 90 days
#   "today 12-m" - past 12 months  "today 5-y"  - past 5 years

ENDPOINTS = {"TIMESERIES": "multiline", "GEO_MAP": "comparedgeo", "RELATED_QUERIES": "relatedsearches"}
BASE = "https://trends.google.com/trends/api"


def scrape_do(url):
    resp = requests.get(
        "https://api.scrape.do/?token=" + token + "&url=" + quote(url, safe=""),
        timeout=60,
    )
    resp.raise_for_status()
    text = resp.text
    return json.loads(text[5:] if text.startswith(")]}'") else text)


def get_widgets():
    req = json.dumps({
        "comparisonItem": [{"keyword": keyword, "geo": geo, "time": timeframe}],
        "category": category,
        "property": property_filter,
    }, separators=(",", ":"))
    data = scrape_do(f"{BASE}/explore?hl={hl}&tz={tz}&req={quote(req)}")
    return {w["id"]: w for w in data["widgets"] if w["id"] in ENDPOINTS}


def fetch_widget(widget):
    endpoint = ENDPOINTS[widget["id"]]
    req = json.dumps(widget["request"], separators=(",", ":"))
    return scrape_do(f"{BASE}/widgetdata/{endpoint}?hl={hl}&tz={tz}&req={quote(req)}&token={widget['token']}")


print("Fetching widget tokens...")
widgets = get_widgets()

result = {"keyword": keyword, "timeframe": timeframe, "geo": geo or "Worldwide"}

print("Fetching interest over time...")
time_data = fetch_widget(widgets["TIMESERIES"])
result["interest_over_time"] = [
    {"time": p["formattedTime"], "value": p["value"][0], "has_data": p["hasData"][0]}
    for p in time_data["default"]["timelineData"]
]

print("Fetching interest by region...")
geo_data = fetch_widget(widgets["GEO_MAP"])
result["interest_by_region"] = [
    {"country_code": e["geoCode"], "country": e["geoName"], "value": e["value"][0]}
    for e in geo_data["default"]["geoMapData"] if e["hasData"][0]
]

print("Fetching related queries...")
ranked = fetch_widget(widgets["RELATED_QUERIES"])["default"]["rankedList"]
result["related_queries"] = {
    "top": [{"query": kw["query"], "value": kw["value"]} for kw in ranked[0].get("rankedKeyword", [])] if ranked else [],
    "rising": [{"query": kw["query"], "change": kw["formattedValue"]} for kw in ranked[1].get("rankedKeyword", [])] if len(ranked) > 1 else [],
}

output_file = "google-trends.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2, ensure_ascii=False)

print(f"\nSaved to {output_file}")
print(f"  {len(result['interest_over_time'])} time points, {len(result['interest_by_region'])} countries")
print(f"  {len(result['related_queries']['top'])} top queries, {len(result['related_queries']['rising'])} rising")
