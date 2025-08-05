import requests
from bs4 import BeautifulSoup
import re
import urllib.parse

# Our token provided by Scrape.do
token = "<your_token>"

# Target Zoro product URL
target_url = urllib.parse.quote_plus("<target_product_url>")  # Example: https://www.zoro.com/gorilla-glue-30-yds-black-duct-tape-106718/i/G109908549/

# Scrape.do API endpoint
url = f"http://api.scrape.do/?token={token}&url={target_url}&render=false&geoCode=us&super=true"

# Send the request
response = requests.request("GET", url)

# Parse the response using BeautifulSoup
soup = BeautifulSoup(response.text, "html.parser")

# Extract product name
product_name = soup.find("h1").text.strip()

# Extract MFR number
identifiers_div = soup.find("div", class_="product-identifiers")
identifiers_text = identifiers_div.get_text(" ", strip=True) if identifiers_div else ""
mfr_match = re.search(r"Mfr\s*#\s*([\w\-/]+)", identifiers_text)
mfr_number = mfr_match.group(1) if mfr_match else "Not found"

# Extract product price
price_span = soup.find("span", class_="currency text-h2")
product_price = price_span.text.strip() if price_span else "Not found"

# Print results
print("Product Name:", product_name)
print("MFR #:", mfr_number)
print("Product Price:", product_price)