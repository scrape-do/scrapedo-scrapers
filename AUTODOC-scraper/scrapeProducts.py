import requests
import urllib.parse
import json
import csv
from bs4 import BeautifulSoup

# Your Scrape.do token
token = "<your_token>"

# Target product URL - Example: https://www.autodoc.de/reifen/hankook-8808563543369-1029031
target_url = "<target_product_url>"

# Build Scrape.do API URL
api_url = f"https://api.scrape.do/?token={token}&url={urllib.parse.quote_plus(target_url)}&super=true"

# Request and parse
response = requests.get(api_url)
soup = BeautifulSoup(response.text, "html.parser")

# Extract JSON-LD structured data for product information
json_ld = next((tag.string for tag in soup.select('script[type="application/ld+json"]') 
                if tag.string and json.loads(tag.string).get("@type") == "Product"), None)
data = json.loads(json_ld)

# Extract product details
offers = data.get("offers", {})
availability = {"https://schema.org/InStock": "In stock"}.get(offers.get("availability"), "Unknown")
image_urls = "; ".join(data.get("image", [])) if isinstance(data.get("image"), list) else str(data.get("image", ""))

# Display results
print("MPN:                ", data.get("mpn", "N/A"))
print("SKU:                ", data.get("sku", "N/A"))
print("Product Name:       ", data.get("name", "N/A"))
print("Brand Name:         ", data.get("brand", {}).get("name", "N/A"))
print("Product Description:", data.get("description", "N/A"))
print("Price:              ", offers.get("price", "N/A"), offers.get("priceCurrency", "EUR"))
print("Image URLs:         ", image_urls)
print("Availability:       ", availability)
print("Seller Name:        ", offers.get("seller", {}).get("name", "N/A"))

# Save to CSV
with open("autodoc_product_data.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(["MPN", "SKU", "Product Name", "Brand", "Description", "Price", "Currency", "Image URLs", "Availability", "Seller"])
    writer.writerow([
        data.get("mpn", "N/A"),
        data.get("sku", "N/A"),
        data.get("name", "N/A"),
        data.get("brand", {}).get("name", "N/A"),
        data.get("description", "N/A"),
        offers.get("price", "N/A"),
        offers.get("priceCurrency", "EUR"),
        image_urls,
        availability,
        offers.get("seller", {}).get("name", "N/A")
    ])

print("✅ Data saved to autodoc_product_data.csv")