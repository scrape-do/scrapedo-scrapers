import json
import sys
import struct
import urllib.parse
import requests

# Reviews contain international characters (Japanese, Turkish, etc.)
# so we need UTF-8 output to handle them cleanly on Windows consoles.
sys.stdout.reconfigure(encoding="utf-8")

# Google Maps reviews use the listentitiesreviews RPC endpoint,
# which returns clean JSON instead of HTML.
TOKEN = "<your_token>"
FEATURE_ID = "0x47e66e00f9521b7d:0xc8c16b75253918c1"  # Carnavalet Museum

# The reviews endpoint needs the feature ID as signed 64-bit integers
# derived from the hex halves. A fun little conversion puzzle!
parts = FEATURE_ID.split(":")
fid1 = struct.unpack(">q", bytes.fromhex(parts[0][2:]))[0]
fid2 = struct.unpack(">q", bytes.fromhex(parts[1][2:]))[0]

# The pb parameter controls pagination and sorting:
#   !2m1!2i{offset}  → page offset (0-based, increments of 10)
#   !3e{sort}        → 1=relevant, 2=newest, 3=highest, 4=lowest
SORT_RELEVANT = 1
OFFSET = 0

pb = (
    f"!1m2!1y{fid1}!2y{fid2}"
    f"!2m1!2i{OFFSET}"
    f"!3e{SORT_RELEVANT}"
    f"!4m5!3b1!4b1!5b1!6b1!7b1"
    f"!5m2!1s{FEATURE_ID}!7e81"
)

TARGET_URL = (
    f"https://www.google.com/maps/preview/review/listentitiesreviews"
    f"?authuser=0&hl=en&gl=us"
    f"&pb={urllib.parse.quote(pb, safe='')}"
)

# Same super=true approach we use across all our Google scrapers.
api_url = (
    f"http://api.scrape.do/?token={TOKEN}"
    f"&url={urllib.parse.quote(TARGET_URL)}"
    f"&geoCode=us&super=true"
)

print(f"Fetching reviews for: {FEATURE_ID}")
response = requests.get(api_url, timeout=60)
text = response.text

# Google prepends )]}' as an anti-XSSI prefix. Strip it to get pure JSON.
if text.startswith(")]}'"):
    text = text[text.index("\n") + 1:]

data = json.loads(text)

# data[5] holds the rating distribution: [1-star, 2-star, 3-star, 4-star, 5-star]
dist = data[5] if data[5] else []
total_reviews = sum(dist) if dist else 0
overall_rating = (
    round(sum((i + 1) * c for i, c in enumerate(dist)) / total_reviews, 1)
    if total_reviews
    else None
)

# Each review is a nested array inside data[2]. We pull out the fields we
# care about: reviewer info, rating, time, text, language, and visit date.
raw_reviews = data[2] if data[2] else []
reviews = []

for rev in raw_reviews:
    author_info = rev[0] if rev[0] else []

    # The reviewer's badge (like "Local Guide · 25 reviews") is buried
    # deep in the nested structure.
    reviewer_badge = None
    if len(rev) > 12 and rev[12] and rev[12][1]:
        badge_list = rev[12][1]
        if len(badge_list) > 10 and badge_list[10]:
            reviewer_badge = badge_list[10]

    reviews.append({
        "reviewer": author_info[1] if len(author_info) > 1 else None,
        "reviewer_profile": author_info[0] if len(author_info) > 0 else None,
        "reviewer_photo": author_info[2] if len(author_info) > 2 else None,
        "reviewer_badge": reviewer_badge,
        "rating": rev[4],
        "time": rev[1],
        "text": rev[3],
        "language": rev[32] if len(rev) > 32 else None,
        "visited": rev[45] if len(rev) > 45 and rev[45] else None,
    })

output = {
    "feature_id": FEATURE_ID,
    "overall_rating": overall_rating,
    "total_reviews": total_reviews,
    "rating_distribution": {
        "1_star": dist[0] if len(dist) > 0 else 0,
        "2_star": dist[1] if len(dist) > 1 else 0,
        "3_star": dist[2] if len(dist) > 2 else 0,
        "4_star": dist[3] if len(dist) > 3 else 0,
        "5_star": dist[4] if len(dist) > 4 else 0,
    },
    "extracted_count": len(reviews),
    "reviews": reviews,
}

with open("maps_reviews.json", "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print(f"\nOverall: {overall_rating} ({total_reviews} reviews)")
print(f"Distribution: 5*={dist[4]} 4*={dist[3]} 3*={dist[2]} 2*={dist[1]} 1*={dist[0]}")
print(f"Extracted: {len(reviews)} reviews\n")

for i, rev in enumerate(reviews):
    stars = f"{rev['rating']}*" if rev["rating"] else "?"
    preview = (rev["text"] or "")[:80].replace("\n", " ")
    if len(rev["text"] or "") > 80:
        preview += "..."
    print(f"  [{i+1:2d}] {stars} {rev['time']} | {rev['reviewer']} | {preview}")

print(f"\nSaved to maps_reviews.json")
