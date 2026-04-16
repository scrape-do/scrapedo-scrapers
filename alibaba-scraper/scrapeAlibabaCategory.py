# Scrape Alibaba category listings via Scrape.do and export to CSV.
# Data comes from embedded window._PAGE_DATA_ JSON, not DOM selectors.
# Pagination uses the showroom's own urlRule (not ?page=).

import csv
import json
import re
import time
import urllib.parse

import requests

TOKEN = "<your_token>"
CATEGORY_URL = "https://www.alibaba.com/category/televisions_634.html"
MAX_PAGES = 3
REQUEST_DELAY_SEC = 1.5

OUTPUT_CSV = "alibaba-category-products.csv"
FIELDS = ["name", "price", "image_url", "min_order", "review_count", "review_rating", "supplier_history_order_count"]


def fetch(target_url):
    api_url = "http://api.scrape.do/?" + urllib.parse.urlencode(
        {"token": TOKEN, "url": target_url, "super": "true", "geoCode": "us"},
        quote_via=urllib.parse.quote,
    )
    r = requests.get(api_url, timeout=120)
    if r.status_code != 200:
        print(f"  HTTP {r.status_code}")
        return None
    return r


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


all_rows = []
url_rule = None

for page_idx in range(1, MAX_PAGES + 1):
    if page_idx == 1:
        target = CATEGORY_URL
    elif url_rule:
        # urlRule looks like "/category/televisions_634/{0}.html" -- fill in page number
        origin = "https://www.alibaba.com"
        path = url_rule.replace("{0}", str(page_idx)).lstrip("/")
        target = f"{origin}/{path}"
    else:
        print("No pagination urlRule found; stopping.")
        break

    print(f"Fetching page {page_idx}: {target}")
    response = fetch(target)
    if not response:
        break

    page_data = extract_json_blob(response.text, r"window\._PAGE_DATA_\s*=\s*(\{)")
    if not page_data:
        print("  Could not parse _PAGE_DATA_.")
        break

    # Grab urlRule from first page for subsequent pagination
    pagination = page_data.get("pagination")
    if pagination:
        url_rule = pagination.get("urlRule") or url_rule

    batch = []
    items = page_data["offerResultData"]["itemInfoList"]
    for item in items:
        offer = item["offer"]
        info = offer.get("information") or {}

        # Skip non-product entries (ads, store cards)
        if "/product-detail/" not in str(info.get("productUrl", "")):
            continue

        trade = offer.get("tradePrice") or {}
        img_block = offer.get("image") or {}
        raw_img = img_block.get("mainImage", "")
        if raw_img.startswith("//"):
            raw_img = "https:" + raw_img

        reviews = offer.get("reviews") or {}
        company = offer.get("company") or {}

        batch.append({
            "name": info.get("puretitle", "").strip(),
            "price": str(trade.get("price", "")).strip(),
            "image_url": raw_img.strip(),
            "min_order": str(trade.get("minOrder", "")).strip(),
            "review_count": str(reviews.get("reviewCount", "")),
            "review_rating": str(reviews.get("reviewScore", "")),
            "supplier_history_order_count": str(company.get("supplierHistoryOrderCount", "")),
        })

    print(f"  {len(batch)} products")
    if not batch:
        break
    all_rows.extend(batch)
    if page_idx < MAX_PAGES:
        time.sleep(REQUEST_DELAY_SEC)


with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=FIELDS)
    writer.writeheader()
    writer.writerows(all_rows)

print(f"Wrote {len(all_rows)} rows to {OUTPUT_CSV}")
