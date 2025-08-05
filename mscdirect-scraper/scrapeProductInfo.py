import requests
import urllib.parse
from bs4 import BeautifulSoup

# Your Scrape.do API token and MSC#
token = "<your_token>"
msc_number = "<msc_product_number>"  # Example: 53546172

# Target MSC Direct product URL
target_url = f"https://www.mscdirect.com/product/details/{msc_number}"
encoded_url = urllib.parse.quote_plus(target_url)

# Scrape.do API endpoint - enabling "super=true" for residential proxies
api_url = f"https://api.scrape.do/?token={token}&url={encoded_url}&super=true"

# Send the request and parse the HTML with BeautifulSoup
response = requests.get(api_url)
soup = BeautifulSoup(response.text, "html.parser")

# Extract brand name and product name
brand = soup.find(id="brand-name").text.strip()
name = soup.find("h1").text.strip()

# Extract product price (and remove "ea." from it's end)
price = soup.find(id="webPriceId").text.strip().replace("ea.", "").strip()

# Detect stock status; default to "Out of Stock" if not present or different
availability_tag = soup.find(id="availabilityHtml")
if availability_tag and "In Stock" in availability_tag.text:
    stock_status = "In Stock"
else:
    stock_status = "Out of Stock"

# Print results
print("Brand:", brand)
print("Product Name:", name)
print("Price:", price)
print("Stock Status:", stock_status)