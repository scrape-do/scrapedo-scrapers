import requests
import urllib.parse
from bs4 import BeautifulSoup
import json
import re

# Configuration
token = "<your-token>"
product_url = "https://www.etsy.com/listing/468670752/a-man-a-dog-the-original-original-wood"

# Make API request through Scrape.do
encoded_url = urllib.parse.quote_plus(product_url)
api_url = f"https://api.scrape.do?token={token}&url={encoded_url}&geoCode=us&super=true&extraHeaders=true"
headers = {"sd-x-detected-locale": "USD|en-US|US"}
response = requests.get(api_url, headers=headers)

soup = BeautifulSoup(response.text, "html.parser")

# Initialize product data
product = {"url": product_url}

# Extract listing ID from URL
listing_match = re.search(r"/listing/(\d+)", product_url)
if listing_match:
    product["listing_id"] = listing_match.group(1)

# Extract JSON-LD structured data from script tags
for script in soup.find_all("script", attrs={"type": "application/ld+json"}):
    try:
        data = json.loads(script.string)
        objs = data if isinstance(data, list) else [data]
        
        for obj in objs:
            product_type = obj.get("@type")
            if product_type == "Product" or (isinstance(product_type, list) and "Product" in product_type):
                # Extract basic product information
                product["name"] = obj.get("name")
                product["description"] = obj.get("description")
                product["category"] = obj.get("category")
                
                # Extract shop name from brand field
                brand = obj.get("brand")
                if isinstance(brand, dict):
                    product["shop"] = brand.get("name")
                elif isinstance(brand, str):
                    product["shop"] = brand
                
                # Extract product images
                image_data = obj.get("image")
                if isinstance(image_data, list):
                    product["images"] = image_data
                elif image_data:
                    product["images"] = [image_data]
                else:
                    product["images"] = []
                
                # Extract price and currency from offers
                offers = obj.get("offers")
                if isinstance(offers, list):
                    offers = offers[0] if offers else {}
                
                price = (offers or {}).get("price") or (offers or {}).get("lowPrice")
                product["price"] = float(price) if price else None
                product["currency"] = (offers or {}).get("priceCurrency")
                
                # Extract product availability status
                avail = (offers or {}).get("availability") or ""
                if "/" in avail:
                    product["availability"] = avail.split("/")[-1]
                elif avail:
                    product["availability"] = avail
                
                # Extract rating and review count
                agg = obj.get("aggregateRating") or {}
                product["rating"] = agg.get("ratingValue")
                product["review_count"] = agg.get("reviewCount")
                break
    except:
        continue

# Print results as formatted JSON
print(json.dumps(product, indent=2, sort_keys=True))

