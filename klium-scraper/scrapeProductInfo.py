import requests
import urllib.parse
from bs4 import BeautifulSoup
import re

# Scrape.do config
token = "<your_token>"
target_url = "<target_product_url>"  # Example: https://www.klium.com/en/bosch-gbh-2-28-f-rotary-hammer-with-sds-plus-880-w-in-case-0611267600-121096
encoded_url = urllib.parse.quote_plus(target_url)

# Scrape.do API request with Cloudflare bypass
api_url = f"https://api.scrape.do?token={token}&url={encoded_url}"

# Send request and parse HTML
response = requests.get(api_url)
soup = BeautifulSoup(response.text, "html.parser")

# Extract product name
name = soup.find("h1").text.strip()

# Extract product price
price = soup.find("span", class_="current-price-value")["content"]

# Extract stock availability
text = soup.get_text().lower()
match = re.search(r"we have (\d+) products? in stock", text)
if match:
    stock = f"{match.group(1)} in stock"
elif "in stock" in text:
    stock = "In stock"
else:
    stock = "Out of stock"

# Output
print("Product Name:", name)
print("Price:", price)
print("Stock Availability:", stock)