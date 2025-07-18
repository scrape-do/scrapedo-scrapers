import requests
import urllib.parse
import json

# --- Scrape.do API token and Uber Eats backend endpoint ---
TOKEN = "<your-token>"
# 'uev2.loc' encodes the location; extract from Uber Eats cookies after you select an address
uev2_loc = "<your-uev2.loc>" # e.g. uev2.loc={...}
# 'placeId' is the Google Place ID for your  location; extract from payload in your browser
place_id = "<your-placeId>" # e.g. ChIJ4zGFAZpYwokRGUGph3Mf37k
TARGET_URL = "https://www.ubereats.com/_p/api/getFeedV1"

# --- Build the Scrape.do API URL ---
api_url = (
    "https://api.scrape.do/?"
    f"url={urllib.parse.quote_plus(TARGET_URL)}"
    f"&token={TOKEN}"
    f"&extraHeaders=true"
    f"&super=true"
    f"&geoCode=us"
)

# --- Headers for Scrape.do (includes location and anti-bot fields) ---
headers = {
    "sd-cookie": uev2_loc,
    "sd-content-type": "application/json",
    "sd-x-csrf-token": "x",
    "sd-x-uber-client-gitref": "x"
}

# --- Main scraping logic: paginate through all feed items ---
all_feed_items = []
offset = 0
page_size = 80
has_more = True

while has_more:
    # Build the POST payload for the current page
    payload = json.dumps({
        "placeId": place_id,
        "provider": "google_places",
        "source": "manual_auto_complete",
        "pageInfo": {"offset": offset, "pageSize": page_size}
    })
    # Send the POST request to Scrape.do
    response = requests.post(api_url, data=payload, headers=headers)
    data = response.json()
    # Extract feed items from the response
    feed_items = data.get("data", {}).get("feedItems", [])
    all_feed_items.extend(feed_items)
    # Check if there are more pages
    has_more = data.get("data", {}).get("meta", {}).get("hasMore", False)
    offset += page_size
    print(f"Fetched {len(feed_items)} items, total so far: {len(all_feed_items)}")

# --- Save all feed items to a JSON file ---
with open("feed_response.json", "w", encoding="utf-8") as f:
    json.dump(all_feed_items, f, ensure_ascii=False, indent=2)

print(f"Total stores collected: {len(all_feed_items)}") 