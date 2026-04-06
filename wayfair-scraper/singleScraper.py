import urllib.parse
import requests
from bs4 import BeautifulSoup

# Wayfair's mirrors are the perfect test case for our extraction logic.
TOKEN = "<your-token>"
TARGET_URL = "https://www.wayfair.com/decor-pillows/pdp/mercer41-dronfield-accent-mirror-w100133415.html"

api_url = f"http://api.scrape.do/?token={TOKEN}&url={urllib.parse.quote(TARGET_URL)}&super=true&render=true"
response = requests.get(api_url, timeout=90)
soup = BeautifulSoup(response.text, "html.parser")

product_name = soup.find("h1").get_text(strip=True) if soup.find("h1") else None

# The SKU is tucked away in the breadcrumbs. We'll target the first crumb for precision.
sku_elem = soup.find(attrs={"data-test-id": "breadcrumbs-crumb-1"})
sku = sku_elem.get_text(strip=True).replace("SKU:", "").strip() if sku_elem else None

seller_elem = soup.find(attrs={"data-rtl-id": "listingManufacturerName"})
seller_name = seller_elem.get_text(strip=True).replace("By", "").strip() if seller_elem else None

price_elem = soup.find(attrs={"data-test-id": "PriceDisplay"})
price = price_elem.get_text(strip=True).replace("$", "").replace(",", "") if price_elem else None

original_price = None
discount_rate = None
previous_container = soup.find(attrs={"data-test-id": "StandardPricingPrice-PREVIOUS"})
if previous_container:
    was_elem = previous_container.find(attrs={"data-test-id": "PriceDisplay"})
    if was_elem:
        original_price = was_elem.get_text(strip=True).replace("$", "").replace(",", "")
        if price and original_price:
            discount = ((float(original_price) - float(price)) / float(original_price)) * 100
            discount_rate = f"{int(discount)}%"

review_rating = soup.find(attrs={"data-rtl-id": "reviewsHeaderReviewsAverage"}).get_text(strip=True) if soup.find(attrs={"data-rtl-id": "reviewsHeaderReviewsAverage"}) else None
review_count = soup.find(attrs={"data-rtl-id": "reviewsHeaderReviewsLink"}).get_text(strip=True).split()[0] if soup.find(attrs={"data-rtl-id": "reviewsHeaderReviewsLink"}) else None
description = soup.find("meta", attrs={"name": "description"}).get("content") if soup.find("meta", attrs={"name": "description"}) else None
image = soup.find("meta", property="og:image").get("content") if soup.find("meta", property="og:image") else None

images = []
for img in soup.find_all(attrs={"data-hb-id": "FluidImage"}):
    src = img.get("src", "")
    if src and "default_name" not in src and src not in images:
        images.append(src)
images = images[:10]

print(f"Product Name: {product_name}")
print(f"SKU: {sku}")
print(f"Seller/Brand: {seller_name}")
print(f"Price: ${price}")
print(f"Original Price: ${original_price}")
print(f"Discount Rate: {discount_rate}")
print(f"Review Rating: {review_rating}")
print(f"Review Count: {review_count}")
print(f"Description: {description}")
print(f"Images: {images}")
