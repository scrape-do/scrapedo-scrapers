# Script to scrape DoorDash restaurant listings using the GraphQL API and save to CSV
import requests
import json
import csv

# API authentication and endpoint setup
TOKEN = "<your-token>"
TARGET_URL = "https://www.doordash.com/graphql/homePageFacetFeed?operation=homePageFacetFeed"
SESSION_ID = "<session-id>"
API_URL = f"http://api.scrape.do/?token={TOKEN}&super=true&url={TARGET_URL}&sessionId={SESSION_ID}"

# GraphQL query for fetching the home page facet feed
QUERY = """query homePageFacetFeed($cursor: String, $filterQuery: String, $displayHeader: Boolean, $isDebug: Boolean, $cuisineFilterVerticalIds: String) { homePageFacetFeed(cursor: $cursor filterQuery: $filterQuery displayHeader: $displayHeader isDebug: $isDebug cuisineFilterVerticalIds: $cuisineFilterVerticalIds) { ...FacetFeedV2ResultFragment __typename } } fragment FacetFeedV2ResultFragment on FacetFeedV2Result { body { id header { ...FacetV2Fragment __typename } body { ...FacetV2Fragment __typename } layout { omitFooter __typename } __typename } page { ...FacetV2PageFragment __typename } header { ...FacetV2Fragment __typename } footer { ...FacetV2Fragment __typename } custom logging __typename } fragment FacetV2Fragment on FacetV2 { ...FacetV2BaseFragment childrenMap { ...FacetV2BaseFragment __typename } __typename } fragment FacetV2BaseFragment on FacetV2 { id childrenCount component { ...FacetV2ComponentFragment __typename } name text { ...FacetV2TextFragment __typename } images { main { ...FacetV2ImageFragment __typename } icon { ...FacetV2ImageFragment __typename } background { ...FacetV2ImageFragment __typename } accessory { ...FacetV2ImageFragment __typename } custom { key value { ...FacetV2ImageFragment __typename } __typename } __typename } events { click { name data __typename } __typename } style { spacing background_color border { color width style __typename } sizeClass dlsType __typename } layout { omitFooter gridSpecs { Mobile { ...FacetV2LayoutGridFragment __typename } Phablet { ...FacetV2LayoutGridFragment __typename } Tablet { ...FacetV2LayoutGridFragment __typename } Desktop { ...FacetV2LayoutGridFragment __typename } WideScreen { ...FacetV2LayoutGridFragment __typename } UltraWideScreen { ...FacetV2LayoutGridFragment __typename } __typename } dlsPadding { top right bottom left __typename } __typename } custom logging __typename } fragment FacetV2ComponentFragment on FacetV2Component { id category __typename } fragment FacetV2TextFragment on FacetV2Text { title titleTextAttributes { textStyle textColor __typename } subtitle subtitleTextAttributes { textStyle textColor __typename } accessory accessoryTextAttributes { textStyle textColor __typename } description descriptionTextAttributes { textStyle textColor __typename } custom { key value __typename } __typename } fragment FacetV2ImageFragment on FacetV2Image { uri videoUri placeholder local style logging events { click { name data __typename } __typename } __typename } fragment FacetV2LayoutGridFragment on FacetV2LayoutGrid { interRowSpacing interColumnSpacing minDimensionCount __typename } fragment FacetV2PageFragment on FacetV2Page { next { name data __typename } onLoad { name data __typename } __typename }"""

# CSV header for output file
header = [
    "Name", "Description", "Delivery Fee", "ETA", "Open Now", "Average Rating", "Number of Ratings", "Price Range", "Distance (mi)", "Store ID", "Link"
]

# Helper to parse 'custom' field from entry, which may be a JSON string or dict
def extract_custom(entry):
    val = entry.get("custom", "{}")
    return json.loads(val) if isinstance(val, str) else val

# Helper to parse 'logging' field from entry, which may be a JSON string or dict
def extract_logging(entry):
    val = entry.get("logging", "{}")
    return json.loads(val) if isinstance(val, str) else val

# Helper to extract the store link from the entry's click event
def extract_link(entry):
    events = entry.get("events", {})
    data = events.get("click", {}).get("data")
    if data:
        try:
            link_data = json.loads(data)
            return link_data.get("domain", "") + link_data.get("uri", "")
        except Exception:
            return None
    return None

# Helper to extract a value from a list of custom fields by key
def extract_custom_value(custom_list, key):
    for c in custom_list:
        if c.get("key") == key:
            return c.get("value", "")
    return ""

# Main scraping logic
def main():
    # Initial cursor for the first page of results
    initial_cursor = "eyJvZmZzZXQiOjAsInZlcnRpY2FsX2lkcyI6WzEwMDMzMywzLDIsMyw3MCwxMDMsMTM5LDE0NiwxMzYsMjM1LDI2OCwyNDEsMjM2LDIzOSw0LDIzOCwyNDMsMjgyXSwicm9zc192ZXJ0aWNhbF9wYWdlX3R5cGUiOiJIT01FUEFHRSIsInBhZ2Vfc3RhY2tfdHJhY2UiOltdLCJsYXlvdXRfb3ZlcnJpZGUiOiJVTlNQRUNJRklFRCIsImlzX3BhZ2luYXRpb25fZmFsbGJhY2siOm51bGwsInNvdXJjZV9wYWdlX3R5cGUiOm51bGwsInZlcnRpY2FsX25hbWVzIjp7fX0="
    cursor = initial_cursor
    page_num = 1
    count = 0
    rows = []

    # Paginate through all available pages
    while True:
        payload = {
            "query": QUERY,
            "variables": {
                "cursor": cursor,
                "filterQuery": "",
                "displayHeader": True,
                "isDebug": False
            }
        }
        print(f"Requesting page {page_num}...")
        try:
            response = requests.post(API_URL, data=json.dumps(payload))
            response.raise_for_status()
            data = response.json()
        except Exception as e:
            print(f"Request or JSON decode failed: {e}")
            break

        # Parse the main feed and find the section with store listings
        home_feed = data.get("data", {}).get("homePageFacetFeed", {})
        sections = home_feed.get("body", [])
        store_feed = next((s for s in sections if s.get("id") == "store_feed"), None)
        if not store_feed:
            print("No store_feed section found!")
            break
        # Extract each store row from the feed
        for entry in store_feed.get("body", []):
            if not entry.get("id", "").startswith("row.store:"):
                continue
            text = entry.get("text", {})
            custom = extract_custom(entry)
            logging = extract_logging(entry)
            row = [
                text.get("title", "N/A"),  # Store name
                text.get("description", ""),  # Store description
                extract_custom_value(text.get("custom", []), "delivery_fee_string"),  # Delivery fee
                extract_custom_value(text.get("custom", []), "eta_display_string"),  # ETA
                custom.get("is_currently_available"),  # Open now
                custom.get("rating", {}).get("average_rating"),  # Average rating
                custom.get("rating", {}).get("display_num_ratings"),  # Number of ratings
                logging.get("price_range"),  # Price range
                logging.get("store_distance_in_miles"),  # Distance in miles
                custom.get("store_id") or logging.get("store_id"),  # Store ID
                extract_link(entry)  # Store link
            ]
            rows.append(row)
            count += 1

        # Check for next page cursor
        page_info = home_feed.get("page", {})
        next_cursor = None
        if page_info.get("next") and page_info["next"].get("data"):
            try:
                next_cursor = json.loads(page_info["next"]["data"]).get("cursor")
            except Exception as e:
                print(f"Failed to parse next cursor: {e}")
                break
        if not next_cursor:
            break
        cursor = next_cursor
        page_num += 1

    # Write all collected rows to CSV file
    with open("doordash_restaurant_listings.csv", "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)
    print(f"Saved {count} restaurants to doordash_restaurant_listings.csv")

if __name__ == "__main__":
    main()