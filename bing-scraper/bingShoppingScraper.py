import requests
import csv
import urllib.parse
from bs4 import BeautifulSoup

# Configuration
token = "<your-token>"
query = "iphone"

# Build URL
target_url = f"https://www.bing.com/shop?q={query}&FORM=SHOPTB"
encoded_url = urllib.parse.quote(target_url, safe='')
api_url = f"http://api.scrape.do?token={token}&url={encoded_url}&geoCode=us&super=true"

print(f"Starting Bing Shopping scrape for: '{query}'\n")

# Send request
print("Fetching products...")
response = requests.get(api_url)
soup = BeautifulSoup(response.text, "html.parser")

# Extract products
products = []

# Find all product cards
for product_card in soup.find_all("div", class_="br-gOffCard"):
    try:
        # Extract product name
        name_tag = product_card.find("div", class_="br-offTtl")
        product_name = name_tag.get_text(strip=True)
        
        # Extract price
        price_tag = product_card.find("div", class_="br-price")
        product_price = price_tag.get_text(strip=True) if price_tag else ""
        
        # Extract seller
        seller_tag = product_card.find("span", class_="br-offSlrTxt")
        seller_name = seller_tag.get_text(strip=True) if seller_tag else ""
        
        # Extract product URL
        link_tag = product_card.find("a", class_="br-offLink")
        product_url = link_tag["href"] if link_tag and link_tag.get("href") else ""
        
        products.append({
            "product_name": product_name,
            "price": product_price,
            "seller": seller_name,
            "url": product_url
        })
    except:
        continue

print(f"Found {len(products)} products")

# Save to CSV
print(f"\nSaving products to CSV...")
with open("bing_shopping_results.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["product_name", "price", "seller", "url"])
    writer.writeheader()
    writer.writerows(products)

print(f"Done! Extracted {len(products)} products -> bing_shopping_results.csv")
