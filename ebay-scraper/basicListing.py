import requests
import urllib.parse
from bs4 import BeautifulSoup
import csv


# Scrape.do API token
TOKEN = "<your-token"

# eBay product page
target_url = "<product-url>"
encoded_url = urllib.parse.quote_plus(target_url)

# Scrape.do API endpoint
api_url = f"https://api.scrape.do/?token={TOKEN}&url={encoded_url}&geocode=us&super=true"

response = requests.get(api_url)
product_id = 125575167955
print(response.status_code)

soup = BeautifulSoup(response.text, "html.parser")

# Product Name
try:
    title = soup.find("h1", class_="x-item-title__mainTitle").get_text(strip=True)
except Exception:
    title = None

# Price
try:
    price = soup.find("div", class_="x-price-primary").get_text(strip=True)
except Exception:
    price = None

# Product Image
try:
    image_url = soup.select_one('.ux-image-carousel-item.active').find("img")["src"]
except Exception:
    image_url = None


with open("ebay_product.csv", mode="w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["product_id", "title", "price", "image_url"])  # header row
    writer.writerow([product_id, title, price, image_url])          # data row