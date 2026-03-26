import json
import re
import urllib.parse
import requests

# Extract full place details via the /maps/preview/place endpoint.
# Uses the same protobuf-over-JSON approach as the search scraper.
TOKEN = "<your_token>"

# Feature ID from a Google Maps URL or from our searchScraper results.
FEATURE_ID = "0x47e66e2eeaaaaaa3:0xdc3fd08aa701960a"  # Musée de l'Orangerie

# The pb parameter is our data shopping list again. This time we include the
# feature ID (!1s) and request all the good stuff: name, rating, hours,
# photos, address, phone, website, and coordinates.
DETAIL_PB = (
    "!1m14!1s{fid}"
    "!3m9!1m3!1d5000!2d0!3d0!2m0!3m2!1i1024!2i768!4f13.1"
    "!4m2!3d0!4d0"
    "!13m1!2m0"
    "!15m47!1m8!4e2!18m5!3b0!6b0!14b1!17b1!20b1!20e2!4b1"
    "!10m1!8e3!11m1!3e1!17b1!20m2!1e3!1e6!24b1!25b1!26b1!29b1"
    "!30m1!2b1!36b1!43b1!52b1!55b1!56m1!1b1"
    "!65m5!3m4!1m3!1m2!1i224!2i298"
    "!22m1!1e81!29m0!30m6!3b1!6m1!2b1!7m1!2b1!9b1!32b1!37i771"
)

pb = DETAIL_PB.format(fid=FEATURE_ID)

TARGET_URL = (
    f"https://www.google.com/maps/preview/place"
    f"?authuser=0&hl=en&gl=us"
    f"&pb={urllib.parse.quote(pb, safe='')}"
)

# Same super=true approach we use across all our Google scrapers.
api_url = (
    f"http://api.scrape.do/?token={TOKEN}"
    f"&url={urllib.parse.quote(TARGET_URL)}"
    f"&geoCode=us&super=true"
)

print(f"Fetching place details for: {FEATURE_ID}")
response = requests.get(api_url, timeout=60)

if not response.text.startswith(")]}'"):
    print("Error: unexpected response format")
    print(response.text[:500])
    exit(1)

text = response.text
print(f"Response: {len(text)} chars")

# The response is a massive nested array. We'll pull each field out with
# targeted regex patterns against the serialized response.

# --- Name & Types ---
fid_match = re.search(
    r'"(0x[0-9a-f]+:0x[0-9a-f]+)",\s*"([^"]+)",\s*null,\s*\[((?:"[^"]*"(?:,\s*)?)+)\]',
    text,
)
name = fid_match.group(2) if fid_match else None
types = re.findall(r'"([^"]+)"', fid_match.group(3)) if fid_match else []

# --- Rating & Review Count ---
rating_match = re.search(r',\s*(\d\.\d),\s*(\d+)\]', text[:fid_match.start()] if fid_match else text)
rating = rating_match.group(1) if rating_match else None
review_count = rating_match.group(2) if rating_match else None

# --- Full Address ---
# Google stores it as "Place Name, full address string" in the response.
addr_match = re.search(r'"' + re.escape(name) + r',\s*([^"]+)"', text) if name else None
address = addr_match.group(1).strip() if addr_match else None

# --- Website ---
# The website URL appears before the feature ID in the response,
# paired with a clean domain string right next to it.
website = None
if fid_match:
    before_fid = text[:fid_match.start()]
    for wm in re.finditer(r'"(https?://[^"]+)",\s*"([a-z0-9][a-z0-9.-]+\.[a-z]{2,})"', before_fid):
        url = wm.group(1)
        if "google" not in url and "gstatic" not in url:
            website = url
            break

# --- Phone ---
phone = None
phone_match = re.search(r'"(\+\d[\d ]+\d)"', text)
if phone_match:
    phone = phone_match.group(1)

# --- Coordinates ---
coord_match = re.search(r'\[null,\s*null,\s*(-?\d+\.\d+),\s*(-?\d+\.\d+)\]', text)
latitude = coord_match.group(1) if coord_match else None
longitude = coord_match.group(2) if coord_match else None

# --- Description ---
# Google returns editorial snippets in arrays like:
#   [null,"Description text here",null,null,null,1]
description = None
for dm in re.finditer(r'\[null,"([^"]{30,500})",null,null,null,1\]', text):
    candidate = dm.group(1)
    if not candidate.startswith("http") and not candidate.startswith("0x"):
        description = candidate

# --- Image ---
img_match = re.search(r'"(https://lh3\.googleusercontent\.com/gps-cs-s/[^"]+)"', text)
image = None
if img_match:
    image = img_match.group(1).split("\\u003d")[0].split("=")[0]

# --- Hours ---
# Each day's hours appear as: ["Monday", ...[[" 9 AM–5 PM"
hours = {}
days_pattern = re.findall(
    r'\["(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)".*?\[\["([^"]+)"',
    text,
)
for day, time_str in days_pattern:
    if day not in hours:
        cleaned = re.sub(r"[\u200b\u202f\xa0]", " ", time_str)
        hours[day] = cleaned.replace("\u2013", "-").replace("\u2014", "-")

place_data = {
    "name": name,
    "feature_id": FEATURE_ID,
    "rating": rating,
    "review_count": review_count,
    "types": types,
    "address": address,
    "phone": phone,
    "website": website,
    "latitude": latitude,
    "longitude": longitude,
    "description": description,
    "hours": hours if hours else None,
    "image": image,
}

with open("maps_place_details.json", "w", encoding="utf-8") as f:
    json.dump(place_data, f, indent=2, ensure_ascii=False)

print(f"\nName:         {name}")
print(f"Rating:       {rating}")
print(f"Reviews:      {review_count}")
print(f"Types:        {', '.join(types)}")
print(f"Address:      {address}")
print(f"Phone:        {phone}")
print(f"Website:      {website}")
print(f"Coords:       {latitude}, {longitude}")
print(f"Description:  {description[:80]}..." if description else "Description:  N/A")
print(f"Hours:        {hours if hours else 'N/A'}")
print(f"Image:        {image[:80]}..." if image else "Image:        N/A")

print(f"\nPlace details saved to maps_place_details.json")
