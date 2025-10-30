import requests
import urllib.parse
from bs4 import BeautifulSoup
import csv
import json
import re
import time

# Configuration
token = "<your-token>"
product_url = "https://www.etsy.com/listing/468670752/a-man-a-dog-the-original-original-wood"
max_pages = 5
sort_option = "Relevancy"  # Options: "Relevancy", "MostRecent", "MostHelpful"

# API endpoint for reviews
deep_url = "https://www.etsy.com/api/v3/ajax/bespoke/member/neu/specs/deep_dive_reviews"

# Fetch product page to extract IDs and CSRF token
encoded_url = urllib.parse.quote_plus(product_url)
api_url = f"https://api.scrape.do?token={token}&url={encoded_url}&geoCode=us&super=true&extraHeaders=true"
headers = {"sd-x-detected-locale": "USD|en-US|US"}
response = requests.get(api_url, headers=headers)
html = response.text

# Extract listing ID from URL or HTML
listing_id = None
listing_match = re.search(r"/listing/(\d+)", product_url)
if listing_match:
    listing_id = int(listing_match.group(1))
else:
    listing_match = re.search(r'/listing/(\d+)', html)
    if listing_match:
        listing_id = int(listing_match.group(1))

if not listing_id:
    print("❗ Could not find listing_id")
    exit()

# Extract shop ID from page HTML
shop_id = None
for pattern in [r'"shop_id"\s*:\s*(\d+)', r'"shopId"\s*:\s*(\d+)', r'\'shop_id\'\s*:\s*(\d+)']:
    shop_match = re.search(pattern, html)
    if shop_match:
        shop_id = int(shop_match.group(1))
        break

if not shop_id:
    print("❗ Could not find shop_id")
    exit()

# Extract CSRF token for API authentication
csrf = None
soup = BeautifulSoup(html, "html.parser")
for name in ["csrf_nonce", "csrf-token", "x-csrf-token"]:
    tag = soup.find("meta", attrs={"name": name})
    if tag and tag.get("content"):
        csrf = tag["content"]
        break

if not csrf:
    csrf_match = re.search(r'"csrf_nonce"\s*:\s*"([^"]+)"', html)
    if csrf_match:
        csrf = csrf_match.group(1)
    else:
        csrf_match = re.search(r'"csrf_token"\s*:\s*"([^"]+)"', html)
        if csrf_match:
            csrf = csrf_match.group(1)

if not csrf:
    print("⚠️  CSRF token not found, request may fail")

print(f"📋 Listing ID: {listing_id}, Shop ID: {shop_id}")

# Scrape reviews with pagination
all_reviews = []
page = 1

while page <= max_pages:
    # Build GraphQL payload for reviews API
    payload = {
        "log_performance_metrics": True,
        "specs": {
            "deep_dive_reviews": [
                "Etsy\\Modules\\ListingPage\\Reviews\\DeepDive\\AsyncApiSpec",
                {
                    "listing_id": listing_id,
                    "shop_id": shop_id,
                    "scope": "listingReviews",
                    "page": page,
                    "sort_option": sort_option,
                    "tag_filters": [],
                    "should_lazy_load_images": False,
                    "should_show_variations": False
                }
            ]
        },
        "runtime_analysis": False
    }
    
    # Make POST request through Scrape.do
    encoded_deep_url = urllib.parse.quote_plus(deep_url)
    api_url = f"https://api.scrape.do?token={token}&url={encoded_deep_url}&geoCode=us&super=true"
    
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "X-Requested-With": "XMLHttpRequest",
        "sd-x-detected-locale": "USD|en-US|US"
    }
    
    if csrf:
        headers["x-csrf-token"] = csrf
    
    response = requests.post(api_url, headers=headers, json=payload)
    
    if response.status_code != 200:
        print(f"❗ Request failed with status code {response.status_code}")
        break
    
    # Parse JSON response
    try:
        data = json.loads(response.text)
    except:
        soup_resp = BeautifulSoup(response.text, "html.parser")
        pre = soup_resp.find("pre")
        if pre:
            data = json.loads(pre.get_text())
        else:
            print(f"❗ Failed to parse JSON on page {page}")
            break
    
    # Extract reviews from HTML in response
    if not data.get("output", {}).get("deep_dive_reviews"):
        print(f"📄 Page {page}: No more reviews")
        break
    
    review_html = data["output"]["deep_dive_reviews"]
    review_soup = BeautifulSoup(review_html, "html.parser")
    review_cards = review_soup.find_all("div", class_="review-card")
    
    page_reviews = 0
    for card in review_cards:
        # Extract rating (out of 5 stars)
        rating = None
        rating_span = card.find("span", class_="wt-display-inline-block")
        if rating_span:
            rating_input = rating_span.find("input", attrs={"name": "rating"})
            if rating_input:
                rating = rating_input.get("value")
                if rating:
                    rating = float(rating)
        
        # Extract review text
        review_text_div = card.find("div", class_="wt-text-body")
        review_text = review_text_div.get_text(strip=True) if review_text_div else None
        
        # Extract author username
        author_link = card.find("a", attrs={"data-review-username": True})
        author = author_link.get_text(strip=True) if author_link else None
        
        # Extract review date
        created_at = None
        date_p = card.find("p", class_="wt-text-body-small")
        if date_p:
            date_text = date_p.get_text(strip=True)
            created_at = date_text.split("\n")[-1].strip()
        
        all_reviews.append({
            "listing_id": listing_id,
            "review_id": card.get("data-review-region"),
            "rating": rating,
            "text": review_text,
            "author": author,
            "created_at": created_at
        })
        page_reviews += 1
    
    print(f"📄 Page {page}: {page_reviews} reviews | Total: {len(all_reviews)}")
    
    if page_reviews == 0:
        break
    
    page += 1
    time.sleep(0.5)

# Export to CSV
fields = ["listing_id", "review_id", "rating", "text", "author", "created_at"]

with open("etsy_reviews.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()
    for review in all_reviews:
        writer.writerow({k: review.get(k) for k in fields})

print(f"✅ Saved {len(all_reviews)} reviews to etsy_reviews.csv")