import requests
import urllib.parse
from bs4 import BeautifulSoup

# Scrape.do API token
TOKEN = "<your-token>"

# Target Walmart product URL
target_url = "https://www.walmart.com/ip/17221971947"
encoded_url = urllib.parse.quote(target_url)

# Scrape.do Walmart plugin API endpoint with Secaucus Supercenter
api_url = f"https://api.scrape.do/plugin/walmart/store?token={TOKEN}&zipcode=07094&storeid=3520&url={encoded_url}&super=true&geoCode=us&render=true"

print("Fetching product page...")
response = requests.get(api_url)
if response.status_code != requests.codes.ok:
    response.raise_for_status()
print("✓ Product page fetched successfully")

print("Parsing product data...")
soup = BeautifulSoup(response.text, "html.parser")

# Product name
name_tag = soup.find("h1", {"itemprop": "name"})
name = name_tag.get_text(strip=True) if name_tag else "N/A"

# Brand (two different possible selectors)
brand_tag = soup.find("a", {"class": "prod-brandName"})
if not brand_tag:
    brand_tag = soup.find("a", {"data-seo-id": "brand-name"})
brand = brand_tag.get_text(strip=True) if brand_tag else "N/A"

# Price
price_tag = soup.find("span", {"data-seo-id": "hero-price"})
if price_tag:
    price = price_tag.get_text(strip=True)
    if "Now" in price:
        price = "$" + price.split("$")[1]
else:
    price = "N/A"

# Stock availability
stock = soup.find("button", {"data-dca-name": "ItemBuyBoxAddToCartButton"})
stock = "In stock" if stock else "Out of stock"

# Discount
discount = soup.find("div", {"data-testid": "dollar-saving"})
discount = "$" + discount.get_text(strip=True).split("$")[1] if discount else "N/A"

# Additional product details (AI or regular)
additional_info = []

# First attempt: AI generated details
for li in soup.select("div#product-smart-summary div.mt0 li"):
    additional_info.append(li.get_text(strip=True))

# Fallback: regular details
if not len(additional_info):
    for li in soup.select("span#product-description-atf li"):
        additional_info.append(li.get_text(strip=True))

# Image URL
img_tag = soup.find("img", {"data-seo-id": "hero-image"})
image = img_tag["src"] if img_tag and img_tag.has_attr("src") else "N/A"

print("✓ Product data extracted successfully")

# Print results
print("\n--- Product Details ---")
print("Product Name:", name)
print("Brand:", brand)
print("Price:", price)
print("Stock:", stock)
print("Discount:", discount)
print("Additional Info:", additional_info)
print("Image:", image)
