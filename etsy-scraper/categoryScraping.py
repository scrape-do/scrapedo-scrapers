import requests
import urllib.parse
from bs4 import BeautifulSoup
import csv
import re
import time

# Configuration
token = "<your-token>"
base_url = "https://www.etsy.com/c/jewelry"
max_pages = 3

# Scrape all pages
all_products = []
seen = set()

for page_num in range(1, max_pages + 1):
    # Build paginated URL with page parameter
    url_parts = urllib.parse.urlsplit(base_url)
    params = urllib.parse.parse_qs(url_parts.query)
    params["page"] = [str(page_num)]
    target_url = urllib.parse.urlunsplit((
        url_parts.scheme, url_parts.netloc, url_parts.path,
        urllib.parse.urlencode({k: v[0] for k, v in params.items()}),
        url_parts.fragment
    ))
    
    # Make API request through Scrape.do
    encoded_url = urllib.parse.quote_plus(target_url)
    api_url = f"https://api.scrape.do?token={token}&url={encoded_url}&geoCode=us&super=true&extraHeaders=true"
    headers = {"sd-x-detected-locale": "USD|en-US|US"}
    response = requests.get(api_url, headers=headers)
    
    soup = BeautifulSoup(response.text, "html.parser")
    page_items = 0
    
    # Extract product cards from listing links
    for a_tag in soup.select('a[href*="/listing/"]'):
        try:
            # Extract listing ID from URL
            url = a_tag.get("href") or ""
            if url.startswith("/"): 
                url = "https://www.etsy.com" + url
            listing_match = re.search(r"/listing/(\d+)", url)
            listing_id = listing_match.group(1) if listing_match else None
            
            if not listing_id or listing_id in seen:
                continue
            seen.add(listing_id)
            
            # Navigate to parent card element
            card = a_tag
            for _ in range(3):
                if card.parent: 
                    card = card.parent
            
            text = card.get_text(" ", strip=True)
            
            # Extract product name
            name = a_tag.get("title") or a_tag.get_text(" ", strip=True) or "N/A"
            
            # Extract product image
            image_url = None
            img = card.select_one("img")
            if img:
                image_url = img.get("src") or img.get("data-src") or img.get("data-srcset")
                if image_url and " " in image_url and "http" in image_url:
                    image_url = [p for p in image_url.split() if p.startswith("http")][0]
            
            # Extract pricing information
            current_price = original_price = discount_rate = None
            currency = None
            
            currency_elem = card.select_one('span.currency-symbol')
            if currency_elem:
                currency = currency_elem.get_text(strip=True)
            
            price_elem = card.select_one('p.wt-text-title-01.lc-price span.currency-value')
            if price_elem:
                price_text = price_elem.get_text().replace("$", "").replace(",", "").strip()
                current_price = float(price_text) if price_text else None
            
            orig_price_elem = card.select_one('p.wt-text-caption.search-collage-promotion-price span.currency-value')
            if orig_price_elem:
                orig_text = orig_price_elem.get_text().replace("$", "").replace(",", "").strip()
                original_price = float(orig_text) if orig_text else None
            
            # Calculate discount rate if applicable
            if current_price and original_price and original_price > current_price:
                discount_rate = round(100 * (original_price - current_price) / original_price, 2)
            
            # Extract product rating
            rating = None
            aria_elem = card.select_one('[aria-label*="out of 5"]')
            if aria_elem:
                rating_match = re.search(r"([\d.]+)\s*out of 5", aria_elem.get("aria-label", ""))
                if rating_match:
                    rating = float(rating_match.group(1))
            
            # Extract review count
            review_count = None
            review_match = re.search(r"\((\d{1,5})\)", text)
            if review_match:
                review_count = int(review_match.group(1))
            
            # Extract shop name
            shop = None
            shop_elem = card.find('p', {'data-seller-name-container': True})
            if shop_elem:
                shop_spans = shop_elem.find_all('span')
                if len(shop_spans) > 4:
                    shop = shop_spans[4].get_text(strip=True)
            
            # Extract product flags
            star_seller = bool(re.search(r"\bStar Seller\b", text, re.I))
            free_shipping = bool(re.search(r"\bFree shipping\b", text, re.I))
            
            left_match = re.search(r"Only\s+(\d+)\s+left", text, re.I)
            only_left = int(left_match.group(1)) if left_match else None
            
            all_products.append({
                "listing_id": listing_id,
                "name": name,
                "shop": shop,
                "price": current_price,
                "original_price": original_price,
                "discount_rate": discount_rate,
                "currency": currency,
                "rating": rating,
                "review_count": review_count,
                "star_seller": star_seller,
                "free_shipping": free_shipping,
                "only_left": only_left,
                "image": image_url,
                "url": url
            })
            page_items += 1
        except:
            continue
    
    print(f"📄 Page {page_num}: {page_items} items | Total: {len(all_products)}")
    
    if page_num > 1 and page_items == 0:
        break
    
    time.sleep(1)

# Export to CSV
fields = ["listing_id", "name", "shop", "price", "original_price", "discount_rate", "currency",
          "rating", "review_count", "star_seller", "free_shipping", "only_left", "image", "url"]

with open("etsy_collection.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()
    for product in all_products:
        writer.writerow({k: product.get(k) for k in fields})

print(f"✅ Saved {len(all_products)} products to etsy_collection.csv")