import requests
import csv
import urllib.parse
from bs4 import BeautifulSoup

# Configuration
token = "<your-token>"
query = "iphone"
max_pages = 5

all_products = []
page = 1

print(f"Starting Bing Shopping scrape for: '{query}'")
print(f"Max pages: {max_pages}\n")

while page <= max_pages:
    # Build URL
    if page == 1:
        target_url = f"https://www.bing.com/shop?q={query}&FORM=SHOPTB"
    else:
        target_url = f"https://www.bing.com/shop?q={query}&FORM=SHOPTB&page={page}"
    
    encoded_url = urllib.parse.quote(target_url, safe='')
    api_url = f"http://api.scrape.do?token={token}&url={encoded_url}&geoCode=us&super=true"
    
    print(f"Page {page}...", end=" ")
    
    # Send request
    response = requests.get(api_url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Extract products
    page_products = []
    
    # Find all product cards
    for product_card in soup.find_all("div", class_="br-gOffCard"):
        try:
            # Extract product name
            name_tag = product_card.find("div", class_="br-offTtl")
            product_name = name_tag.get_text(strip=True)
            
            # Extract price (can be in different formats)
            price_tag = product_card.find("div", class_="l2vh_pr") or product_card.find("div", class_="br-price")
            product_price = price_tag.get_text(strip=True) if price_tag else ""
            
            # Extract seller
            seller_tag = product_card.find("span", class_="br-offSlrTxt")
            seller_name = seller_tag.get_text(strip=True) if seller_tag else ""
            
            # Extract product URL
            link_tag = product_card.find("a", class_="br-offLink")
            product_url = link_tag["href"] if link_tag and link_tag.get("href") else ""
            
            page_products.append({
                "product_name": product_name,
                "price": product_price,
                "seller": seller_name,
                "url": product_url
            })
        except:
            continue
    
    if not page_products:
        print("No products found")
        break
    
    all_products.extend(page_products)
    print(f"Found {len(page_products)} products (total: {len(all_products)})")
    
    page += 1

# Save to CSV
print(f"\nSaving {len(all_products)} products to CSV...")
with open("bing_shopping_results.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["product_name", "price", "seller", "url"])
    writer.writeheader()
    writer.writerows(all_products)

print(f"Done! Extracted {len(all_products)} products across {page - 1} pages -> bing_shopping_results.csv")
