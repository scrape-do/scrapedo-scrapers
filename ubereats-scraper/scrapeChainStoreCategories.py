import requests
import urllib.parse
import json
import csv

# --- Scrape.do token and store/section configuration ---
scrape_token = "<your-token>"
store_uuid = "<store_uuid>" # extract from URL, e.g. 41b7a1bf-9cbc-57b5-8934-c59f5f829fa7
section_uuids = ["<section_uuid>"] # extract from URL, e.g. 63eaa833-9345-41dd-9af5-2d7da547f6da

# --- Target Uber Eats CatalogPresentationV2 endpoint ---
catalog_url = "https://www.ubereats.com/_p/api/getCatalogPresentationV2"

# --- Prepare Scrape.do API URL ---
api_url = (
    f"https://api.scrape.do/?url={urllib.parse.quote_plus(catalog_url)}"
    f"&token={scrape_token}"
    f"&extraHeaders=true"
    f"&super=true"
    f"&geoCode=us"
)

# --- Headers for Scrape.do (includes location and anti-bot fields) ---
headers = {
    "sd-cookie": "uev2.loc={%22address%22:{%22address1%22:%22Central%20Park%22,%22address2%22:%22New%20York,%20NY%22,%22aptOrSuite%22:%22%22,%22eaterFormattedAddress%22:%22New%20York,%20NY,%20USA%22,%22subtitle%22:%22New%20York,%20NY%22,%22title%22:%22Central%20Park%22,%22uuid%22:%22%22},%22latitude%22:40.7825547,%22longitude%22:-73.9655834,%22reference%22:%22ChIJ4zGFAZpYwokRGUGph3Mf37k%22,%22referenceType%22:%22google_places%22,%22type%22:%22google_places%22,%22addressComponents%22:{%22city%22:%22New%20York%22,%22countryCode%22:%22US%22,%22firstLevelSubdivisionCode%22:%22NY%22,%22postalCode%22:%22%22},%22categories%22:[%22PARK%22,%22ATTRACTION%22,%22OUTDOORS%22,%22LANDMARK%22,%22AREAS_AND_BUILDINGS%22,%22place%22],%22originType%22:%22user_autocomplete%22,%22source%22:%22manual_auto_complete%22,%22userState%22:%22Unknown%22};",
    "sd-content-type": "application/json",
    "sd-x-csrf-token": "x",
    "sd-x-uber-client-gitref": "x"
}

# --- Main scraping logic: robust pagination and dual-payload handling ---
all_results = []
offset = 0
has_more = True
first = True
while has_more:
    # Build two payload variants: with and without sectionTypes
    payload_with_section_types = json.dumps({
        "sortAndFilters": None,
        "storeFilters": {
            "storeUuid": store_uuid,
            "sectionUuids": section_uuids,
            "subsectionUuids": None,
            "sectionTypes": ["COLLECTION"]
        },
        "pagingInfo": {"enabled": True, "offset": offset},
        "source": "NV_L2_CATALOG"
    })
    payload_without_section_types = json.dumps({
        "sortAndFilters": None,
        "storeFilters": {
            "storeUuid": store_uuid,
            "sectionUuids": section_uuids,
            "subsectionUuids": None
        },
        "pagingInfo": {"enabled": True, "offset": offset},
        "source": "NV_L2_CATALOG"
    })
    # Log which request is being sent
    if first:
        print("Requesting first items")
        first = False
    else:
        print(f"Requesting next items (offset={offset})")
    # Try with sectionTypes first
    response = requests.post(api_url, data=payload_with_section_types, headers=headers)
    data = response.json()
    catalogs = data.get("data", {}).get("catalog", [])
    results = []
    for section in catalogs:
        items = section.get("payload", {}).get("standardItemsPayload", {}).get("catalogItems", [])
        for item in items:
            price_cents = item.get("price")
            price = f"{price_cents / 100:.2f}" if price_cents is not None else ""
            results.append({
                "uuid": item.get("uuid"),
                "title": item.get("title"),
                "description": item.get("titleBadge", {}).get("text", ""),
                "price": price,
                "imageUrl": item.get("imageUrl"),
                "isAvailable": item.get("isAvailable"),
                "isSoldOut": item.get("isSoldOut"),
                "sectionUuid": item.get("sectionUuid"),
                "productUuid": item.get("productInfo", {}).get("productUuid", "")
            })
    # If no results, try without sectionTypes
    if results:
        variant_used = "with sectionTypes"
    else:
        response = requests.post(api_url, data=payload_without_section_types, headers=headers)
        data = response.json()
        catalogs = data.get("data", {}).get("catalog", [])
        results = []
        for section in catalogs:
            items = section.get("payload", {}).get("standardItemsPayload", {}).get("catalogItems", [])
            for item in items:
                price_cents = item.get("price")
                price = f"{price_cents / 100:.2f}" if price_cents is not None else ""
                results.append({
                    "uuid": item.get("uuid"),
                    "title": item.get("title"),
                    "description": item.get("titleBadge", {}).get("text", ""),
                    "price": price,
                    "imageUrl": item.get("imageUrl"),
                    "isAvailable": item.get("isAvailable"),
                    "isSoldOut": item.get("isSoldOut"),
                    "sectionUuid": item.get("sectionUuid"),
                    "productUuid": item.get("productInfo", {}).get("productUuid", "")
                })
        variant_used = "without sectionTypes" if results else None
    all_results.extend(results)
    has_more = data.get("data", {}).get("meta", {}).get("hasMore", False)
    # Log which variant returned results
    if variant_used:
        print(f"Fetched {len(results)} items using {variant_used}, total so far: {len(all_results)}")
    else:
        print("No more items returned, breaking loop.")
        break
    offset += len(results)

# --- Write all results to CSV ---
with open("catalog_items.csv", "w", newline='', encoding="utf-8") as csvfile:
    fieldnames = ["uuid", "title", "description", "price", "imageUrl", "isAvailable", "isSoldOut", "sectionUuid", "productUuid"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for row in all_results:
        writer.writerow(row)
print(f"Wrote {len(all_results)} items to catalog_items.csv")
