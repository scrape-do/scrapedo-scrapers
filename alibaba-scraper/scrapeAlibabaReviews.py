# Scrape Alibaba product reviews via Scrape.do and export to CSV.
# Flow: (1) GET PDP for companyId/sellerAliId/productId,
#        (2) Dummy MTOP call to auto-obtain _m_h5_tk session cookies,
#        (3) Signed MTOP scatter calls for paginated reviews.

import csv
import hashlib
import json
import re
import time
import urllib.parse

import requests

TOKEN = "<your_token>"
PRODUCT_URL = "https://www.alibaba.com/product-detail/Smart-TV-55-Inches-Television-4K_1601578880652.html"

MTOP_MAX_PAGES = 10
MTOP_PAGE_SIZE = 10
MTOP_DELAY_SEC = 1.0

# MTOP endpoint config (copy from DevTools Network tab if Alibaba changes these)
MTOP_API = "mtop.alibaba.icbu.review.new.shopreview.scatter"
MTOP_APP_KEY = "12574478"
MTOP_JSV = "2.7.5"

OUTPUT_CSV = "alibaba-reviews.csv"
OUTPUT_CONTEXT = "alibaba-reviews-context.json"
FIELDS = ["review_text", "reviewer", "rating", "date", "attached_images"]


def fetch(target_url, extra=None):
    params = {"token": TOKEN, "url": target_url, "super": "true", "geoCode": "us"}
    params.update(extra or {})
    api_url = "http://api.scrape.do/?" + urllib.parse.urlencode(params, quote_via=urllib.parse.quote)
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


def obtain_mtop_cookies():
    # Hit the MTOP gateway with a throwaway request so it sets _m_h5_tk cookies
    dummy_data = json.dumps(
        {"clusterId": 0, "currentPage": 1, "countryCode": "US",
         "pageSize": 1, "language": "en", "currency": "USD",
         "companyId": 1, "sellerAliId": 1, "productId": 1},
        separators=(",", ":"),
    )
    dummy_url = (
        f"https://acs.h.alibaba.com/h5/{MTOP_API}/1.0/?"
        + urllib.parse.urlencode({
            "jsv": MTOP_JSV, "appKey": MTOP_APP_KEY, "t": "1", "sign": "dummy",
            "api": MTOP_API, "v": "1.0", "H5Request": "true",
            "type": "originaljson", "dataType": "json", "data": dummy_data,
        }, quote_via=urllib.parse.quote)
    )
    r = fetch(dummy_url)
    if not r:
        return None, None
    # Scrape.do forwards the target's Set-Cookie values in this header
    raw = r.headers.get("Scrape.do-Cookies", "")
    cookies = {}
    for part in raw.split(";"):
        if "=" in part:
            k, _, v = part.strip().partition("=")
            cookies[k.strip()] = v.strip()
    return cookies.get("_m_h5_tk", ""), cookies.get("_m_h5_tk_enc", "")


def normalize_review(rv):
    text = rv.get("reviewContent", "")
    reviewer = rv.get("simpleReviewUserVO", {}).get("anonymousName", "")
    score = rv.get("latitudeScore", {})
    rating = str(score.get("score", ""))
    date = rv.get("reviewTimeFormat", "")

    # Collect review images
    images = []
    for img in rv.get("reviewImageList") or []:
        url = str(img.get("imageId", ""))
        if url.startswith("//"):
            url = "https:" + url
        if url.startswith("http"):
            images.append(url)

    return {
        "review_text": text,
        "reviewer": reviewer,
        "rating": rating,
        "date": date,
        "attached_images": " | ".join(dict.fromkeys(images)),
    }


# --- Step 1: Fetch PDP for MTOP IDs ---

print(f"Fetching PDP: {PRODUCT_URL}")
response = fetch(PRODUCT_URL)
if not response:
    raise SystemExit("PDP request failed.")

detail_data = extract_json_blob(response.text, r"window\.detailData\s*=\s*(\{)")
if not detail_data:
    raise SystemExit("Could not parse window.detailData from HTML.")

gd = detail_data["globalData"]
seller = gd["seller"]
product = gd["product"]
store_review = gd["review"]["storeReview"]

company_id = int(seller["companyId"])
seller_ali_id = int(seller["aliId"])
product_id = int(product["productId"])


# --- Step 2: Auto-obtain MTOP session cookies ---

print("Obtaining MTOP session cookies...")
mtop_h5_tk, mtop_h5_tk_enc = obtain_mtop_cookies()
if not mtop_h5_tk:
    raise SystemExit("Could not obtain _m_h5_tk cookie from MTOP gateway.")

print(f"  Got _m_h5_tk ({mtop_h5_tk[:12]}...)")
h5_token = mtop_h5_tk.split("_", 1)[0]
cookie_str = f"_m_h5_tk={mtop_h5_tk}; _m_h5_tk_enc={mtop_h5_tk_enc}"


# --- Step 3: MTOP scatter (paginated review feed) ---

reviews = []
seen = set()

print(f"MTOP scatter, pages 1..{MTOP_MAX_PAGES}, pageSize={MTOP_PAGE_SIZE}")
for page in range(1, MTOP_MAX_PAGES + 1):
    data_str = json.dumps({
        "clusterId": 0, "currentPage": page, "countryCode": "US",
        "pageSize": MTOP_PAGE_SIZE, "language": "en", "currency": "USD",
        "companyId": company_id, "sellerAliId": seller_ali_id, "productId": product_id,
    }, separators=(",", ":"), ensure_ascii=False)

    # MTOP requires an MD5 signature: token + timestamp + appKey + payload
    ts = str(int(time.time() * 1000))
    sign = hashlib.md5(f"{h5_token}&{ts}&{MTOP_APP_KEY}&{data_str}".encode()).hexdigest()

    mtop_url = f"https://acs.h.alibaba.com/h5/{MTOP_API}/1.0/?" + urllib.parse.urlencode({
        "jsv": MTOP_JSV, "appKey": MTOP_APP_KEY, "t": ts, "sign": sign,
        "api": MTOP_API, "v": "1.0", "H5Request": "true",
        "type": "originaljson", "dataType": "json", "data": data_str,
    }, quote_via=urllib.parse.quote)

    r = fetch(mtop_url, {"setCookies": cookie_str})
    if not r:
        break

    text = r.text.strip()
    # Strip JSONP wrapper if present (mtopjsonpN({...}))
    if text.startswith("mtopjsonp") and "(" in text:
        text = text[text.find("{") : text.rfind("}") + 1]

    body = json.loads(text)
    ret = body["ret"][0]
    if not ret.upper().startswith("SUCCESS"):
        print(f"  page {page}: MTOP ret {ret!r}")
        break

    mtop_data = body["data"]
    # MTOP sometimes returns data as a JSON string instead of an object
    if isinstance(mtop_data, str):
        mtop_data = json.loads(mtop_data)

    # Walk fixed path: data.target.mobileShopReviewVOList[].productReviewVOList[]
    page_reviews = []
    for block in mtop_data["target"]["mobileShopReviewVOList"]:
        for rv in block.get("productReviewVOList") or []:
            if rv.get("reviewContent"):
                page_reviews.append(rv)

    if not page_reviews:
        if page == 1:
            print("  page 1: SUCCESS but no reviews found.")
        break

    count = 0
    for rv in page_reviews:
        key = rv.get("reviewId") or (rv.get("reviewContent"), rv.get("reviewTime"))
        if key not in seen:
            seen.add(key)
            reviews.append(normalize_review(rv))
            count += 1

    print(f"  page {page}: +{count} reviews (total {len(reviews)})")
    if len(page_reviews) < MTOP_PAGE_SIZE:
        break
    time.sleep(MTOP_DELAY_SEC)


# --- Output ---

with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=FIELDS)
    writer.writeheader()
    writer.writerows(reviews)

context = {
    "product_url": PRODUCT_URL,
    "ids": {"companyId": company_id, "sellerAliId": seller_ali_id, "productId": product_id},
    "store_review": store_review,
    "csv_data_rows": len(reviews),
}
with open(OUTPUT_CONTEXT, "w", encoding="utf-8") as f:
    json.dump(context, f, ensure_ascii=False, indent=2)

print(f"Wrote {OUTPUT_CSV} ({len(reviews)} rows)")
print(f"Wrote {OUTPUT_CONTEXT}")
