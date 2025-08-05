from bs4 import BeautifulSoup
import requests
import urllib.parse

# Scrape.do API Token
token = "<your_token>"

# Allegro Product URL
target_url = urllib.parse.quote_plus("<target_product_url>")  # Example: https://allegro.pl/oferta/macbook-air-m2-13-6-16gb-256gb-space-gray-16784193631

# Scrape.do Parameters
render = "false"
geo_code = "pl"
super_mode = "true"

# API Endpoint
url = f"http://api.scrape.do/?token={token}&url={target_url}&render={render}&geoCode={geo_code}&super={super_mode}"

# Send Request
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# Extract Data
product_name = soup.find("h1").text.strip()
product_price = soup.find("meta", attrs={"itemprop": "price"})["content"]
product_rating = soup.find("span", attrs={"data-testid": "aggregateRatingValue"}).text.strip()

# Print Results
print("Product Name:", product_name)
print("Product Price:", product_price)
print("Product Rating:", product_rating)