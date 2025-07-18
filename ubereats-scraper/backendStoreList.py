import requests
import urllib.parse
import json
import csv

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

# --- Parse and extract store details for CSV (match frontendStoreList.py format) ---
results = []
for section in all_feed_items:
    stores = section.get("carousel", {}).get("stores")
    if not stores:
        continue
    for store in stores:
        href = store.get("actionUrl", "")
        name = store.get("title", {}).get("text", "")
        # Promotion: from signposts or offerMetadata
        promo = ""
        signposts = store.get("signposts")
        if signposts:
            promo = signposts[0].get("text", "") if signposts and len(signposts) > 0 else ""
        elif store.get("tracking", {}).get("storePayload", {}).get("offerMetadata", {}).get("offerTypeCount"):
            count = store["tracking"]["storePayload"]["offerMetadata"].get("offerTypeCount", 0)
            if count:
                promo = f"{count} Offers Available"
        # Rating and review count
        rating = store.get("rating", {}).get("text", "")
        review_count = ""
        rating_access = store.get("rating", {}).get("accessibilityText", "")
        # Extract review count using string methods
        marker = "based on more than "
        if marker in rating_access:
            after = rating_access.split(marker, 1)[-1]
            num = after.split(" reviews", 1)[0].strip()
            if num:
                review_count = f"({num})"
        results.append({
            'href': href,
            'name': name,
            'promotion': promo,
            'rating': rating,
            'review_count': review_count
        })

# --- Write results to CSV ---
with open('ubereats_store_cards.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['href', 'name', 'promotion', 'rating', 'review_count']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(results)
print(f"Wrote {len(results)} store cards to ubereats_store_cards.csv")

print(f"Total stores collected: {len(all_feed_items)}") 