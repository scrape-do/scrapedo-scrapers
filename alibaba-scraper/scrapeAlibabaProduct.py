# Scrape an Alibaba product detail page via Scrape.do and export to JSON.
# Data comes from embedded window.detailData JSON (globalData.product / trade / review).

import json
import re
import urllib.parse

import requests

TOKEN = "<your_token>"
PRODUCT_URL = "https://www.alibaba.com/product-detail/Smart-TV-55-Inches-Television-4K_1601578880652.html"

OUTPUT_JSON = "alibaba-product.json"


def extract_json_blob(html, pattern):
    # Walk forward from the regex match, counting braces to find the full JSON object
    m = re.search(pattern, html)
    if not m:
        return None
    start = m.start(1)
    depth = 0
    for i in range(start, min(len(html), start + 3_000_000)):
        if html[i] == "{":
            depth += 1
        elif html[i] == "}":
            depth -= 1
            if depth == 0:
                return json.loads(html[start : i + 1])
    return None


# --- Fetch PDP ---

print(f"Fetching PDP: {PRODUCT_URL}")
api_url = "http://api.scrape.do/?" + urllib.parse.urlencode(
    {"token": TOKEN, "url": PRODUCT_URL, "super": "true", "geoCode": "us"},
    quote_via=urllib.parse.quote,
)
response = requests.get(api_url, timeout=120)
if response.status_code != 200:
    raise SystemExit(f"HTTP {response.status_code}")

detail_data = extract_json_blob(response.text, r"window\.detailData\s*=\s*(\{)")
if not detail_data:
    raise SystemExit("Could not parse window.detailData from HTML.")

gd = detail_data["globalData"]
product = gd["product"]
trade = gd["trade"]
store_review = gd["review"]["storeReview"]

# Gallery images (prefer big URLs)
images = []
for item in product.get("mediaItems") or []:
    if item.get("type") != "image":
        continue
    url = item["imageUrl"].get("big") or item["imageUrl"].get("normal", "")
    if url and url not in images:
        images.append(url)

# Price tiers (MOQ bands)
price_block = product.get("price") or {}
price_tiers = []
for tier in price_block.get("productLadderPrices") or []:
    price_tiers.append({
        "min_quantity": tier.get("min"),
        "max_quantity": tier.get("max"),
        "format_price": tier.get("formatPrice", ""),
        "price": tier.get("price"),
    })

# Dynamic attributes (vary by product category)
attributes = {}
for prop_list in ("productBasicProperties", "productOtherProperties"):
    for prop in product.get(prop_list) or []:
        name = prop.get("attrName", "").strip()
        value = str(prop.get("attrValue", "")).strip()
        if name and value:
            attributes[name] = value

trade_info = trade.get("tradeInfo") or {}

record = {
    "product_url": PRODUCT_URL,
    "title": product.get("subject", "").strip(),
    "images": images,
    "format_ladder_price": price_block.get("formatLadderPrice", "").strip(),
    "price_tiers": price_tiers,
    "moq": product.get("moq"),
    "quantity_unit": (trade_info.get("quantityUnitStr") or "").strip(),
    "store_review_rating": store_review.get("averageStar"),
    "store_review_count": store_review.get("totalReviewCount"),
    "sales_volume_text": trade.get("salesVolume", "").strip(),
    "attributes": attributes,
}

with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False, indent=2)

print(f"Wrote {OUTPUT_JSON}")
