import requests
import urllib.parse
from bs4 import BeautifulSoup
import csv

# Scrape.do API token
TOKEN = "<your-token>"

# Walmart product page with variants
target_url = "https://www.walmart.com/ip/17221971947"
encoded_url = urllib.parse.quote(target_url)

# Scrape.do Walmart plugin API endpoint with Secaucus Supercenter
api_url = f"https://api.scrape.do/plugin/walmart/store?token={TOKEN}&zipcode=07094&storeid=3520&url={encoded_url}&super=true&geoCode=us&render=true"

# Step 1: collect variant URLs
print("Fetching main product page...")
response = requests.get(api_url)
response.raise_for_status()
soup = BeautifulSoup(response.text, "html.parser")

print("Discovering product variants...")
variant_urls = []
for variant in soup.select("div#item-page-variant-group-bg-div a"):
    variant_urls.append("https://www.walmart.com" + variant.get("href"))

# Remove duplicates
variant_urls = list(set(variant_urls))
print(f"✓ Found {len(variant_urls)} variants")

# Step 2: loop through variants and extract data
print("Scraping variant details...")
variant_products = []

for i, url in enumerate(variant_urls, 1):
    print(f"Processing variant {i}/{len(variant_urls)}...")
    encoded_url = urllib.parse.quote(url)
    api_url = f"https://api.scrape.do/plugin/walmart/store?token={TOKEN}&zipcode=07094&storeid=3520&url={encoded_url}&super=true&geoCode=us&render=true"

    response = requests.get(api_url)
    if response.status_code != requests.codes.ok:
        response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # Product name
    name_tag = soup.find("h1", {"itemprop": "name"})
    name = name_tag.get_text(strip=True) if name_tag else "N/A"

    # Brand
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

    # Stock
    stock = soup.find("button", {"data-dca-name": "ItemBuyBoxAddToCartButton"})
    stock = "In stock" if stock else "Out of stock"

    # Discount
    discount = soup.find("div", {"data-testid": "dollar-saving"})
    discount = "$" + discount.get_text(strip=True).split("$")[1] if discount else "N/A"

    # Additional product details
    additional_info = []
    for li in soup.select("div#product-smart-summary div.mt0 li"):
        additional_info.append(li.get_text(strip=True))
    if not len(additional_info):
        for li in soup.select("span#product-description-atf li"):
            additional_info.append(li.get_text(strip=True))

    # Image
    img_tag = soup.find("img", {"data-seo-id": "hero-image"})
    image = img_tag["src"] if img_tag and img_tag.has_attr("src") else "N/A"

    variant_products.append({
        "Product Name": name,
        "Brand": brand,
        "Price": price,
        "Stock": stock,
        "Discount": discount,
        "Additional Info": additional_info,
        "Image": image
    })

# Step 3: save results to CSV
print("Saving results to CSV...")
with open("variant_products.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, variant_products[0].keys())
    writer.writeheader()
    writer.writerows(variant_products)
print(f"✓ Successfully saved {len(variant_products)} variants to variant_products.csv")
