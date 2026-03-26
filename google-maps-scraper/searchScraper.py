import json
import re
import urllib.parse
import requests

# Google Maps' tbm=map endpoint returns structured place data as JSON,
# which means clean data without HTML parsing.
TOKEN = "<your_token>"
SEARCH_QUERY = "museums in paris"

# The pb (protobuf) parameter tells the server which fields we want back.
# Think of it as our shopping list: !7i20 requests 20 results, and the rest
# enables metadata like coordinates, ratings, and place types.
SEARCH_PB = (
    "!1s{query}!7i20!10b1"
    "!12m6!1m1!18b1!2m1!20e3!6m1!114b1"
    "!17m1!3e1"
    "!20m57!2m2!1i203!2i100!3m2!2i4!5b1"
    "!6m6!1m2!1i86!2i86!1m2!1i408!2i240"
    "!7m33!1m3!1e1!2b0!3e3!1m3!1e2!2b1!3e2!1m3!1e2!2b0!3e3"
    "!1m3!1e8!2b0!3e3!1m3!1e10!2b0!3e3!1m3!1e10!2b1!3e2"
    "!1m3!1e10!2b0!3e4!1m3!1e9!2b1!3e2!2b1!9b0"
    "!15m8!1m7!1m2!1m1!1e2!2m2!1i195!2i195!3i20"
)

pb = SEARCH_PB.format(query=urllib.parse.quote_plus(SEARCH_QUERY))

TARGET_URL = (
    f"https://www.google.com/search?tbm=map&hl=en&gl=us"
    f"&q={urllib.parse.quote_plus(SEARCH_QUERY)}"
    f"&pb={urllib.parse.quote(pb, safe='')}"
)

# Maps needs super=true for bot protection.
api_url = (
    f"http://api.scrape.do/?token={TOKEN}"
    f"&url={urllib.parse.quote(TARGET_URL)}"
    f"&geoCode=us&super=true"
)

print(f"Searching Google Maps for: {SEARCH_QUERY}")
response = requests.get(api_url, timeout=60)

if not response.text.startswith(")]}'"):
    print("Error: unexpected response format")
    print(response.text[:500])
    exit(1)

text = response.text

# The response is a nested JSON array (Google's protobuf-over-JSON format).
# Rather than navigating brittle array indices, we extract place data with
# regex against the serialized text. Each place follows a predictable pattern:
#   ... rating, review_count] ... "feature_id", "name", null, ["type", ...]
PLACE_PATTERN = re.compile(
    r',\s*(\d\.\d),\s*(\d+)\]'          # rating, review_count
    r'.*?'                                # intervening metadata
    r'"(0x[0-9a-f]+:0x[0-9a-f]+)"'       # feature_id
    r',\s*"([^"]{2,80})"'                # name
    r',\s*null'                           # null separator
    r',\s*\[((?:"[^"]*"(?:,\s*)?)+)\]',  # ["type1", "type2", ...]
    re.DOTALL,
)

all_results = []
seen = set()

for m in PLACE_PATTERN.finditer(text):
    fid = m.group(3)
    if fid in seen:
        continue
    seen.add(fid)

    name = m.group(4)
    rating = m.group(1)
    reviews = m.group(2)
    types = re.findall(r'"([^"]+)"', m.group(5))

    # We grab a context window around the match to extract nearby fields
    # like address, website, coordinates, and thumbnail image.
    start = max(0, m.start() - 500)
    end = min(len(text), m.end() + 5000)
    ctx = text[start:end]

    addr_match = re.search(r'"' + re.escape(name) + r',\s*([^"]+)"', ctx)
    address = addr_match.group(1).strip() if addr_match else None

    website = None
    for wm in re.finditer(r'"(https?://[^"]+)"', ctx):
        url = wm.group(1)
        if "google" not in url and "gstatic" not in url:
            website = url
            break

    coord_match = re.search(
        r'\[null,\s*null,\s*(-?\d+\.\d+),\s*(-?\d+\.\d+)\]', ctx
    )

    img_match = re.search(
        r'"(https://lh3\.googleusercontent\.com/gps-cs-s/[^"]+)"', ctx
    )
    image = None
    if img_match:
        image = img_match.group(1).split("\\u003d")[0].split("=")[0]

    all_results.append({
        "name": name,
        "feature_id": fid,
        "rating": rating,
        "review_count": reviews,
        "types": types,
        "address": address,
        "website": website,
        "latitude": coord_match.group(1) if coord_match else None,
        "longitude": coord_match.group(2) if coord_match else None,
        "image": image,
    })

with open("maps_search_results.json", "w", encoding="utf-8") as f:
    json.dump(all_results, f, indent=2, ensure_ascii=False)

for i, r in enumerate(all_results, 1):
    print(f"\n--- Place {i} ---")
    print(f"Name:    {r['name']}")
    print(f"Rating:  {r['rating']} ({r['review_count']} reviews)")
    print(f"Types:   {', '.join(r['types'])}")
    print(f"Address: {r['address']}")
    print(f"Website: {r['website']}")
    print(f"Coords:  {r['latitude']}, {r['longitude']}")
    print(f"FID:     {r['feature_id']}")

print(f"\nTotal: {len(all_results)} places saved to maps_search_results.json")
