import requests
import urllib.parse
import re

# Your Scrape.do token
token = "<your_token>"

# Naver product page URL
target_url = "<target_product_url>"
encoded_url = urllib.parse.quote_plus(target_url)

# Scrape.do API endpoint with premium proxy routing
api_url = f"https://api.scrape.do?token={token}&url={encoded_url}&super=true"

# Send the request
response = requests.get(api_url)

# Extract the page HTML
html = response.text

# Use regex to extract product name and price from the embedded JSON
try:
    product_name = re.search(r'"dispName":"([^"]+)"', html).group(1)
    discounted_price = int(re.search(r'"dispDiscountedSalePrice":([0-9]+)', html).group(1))

    # Output the result
    print("Product Name:", product_name)
    print("Price:", f"{discounted_price:,}₩")

except AttributeError:
    print("❗ Could not find product name or price. Make sure the token is valid and geo-restrictions are handled.")