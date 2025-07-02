import requests
import urllib.parse
from bs4 import BeautifulSoup
import json

# Scrape.do token
token = "<your_token>"

# Zomato restaurant URL
target_url = urllib.parse.quote_plus("https://www.zomato.com/dubai/the-cheesecake-factory-dubai-festival-city")

# Scrape.do API URL
api_url = f"http://api.scrape.do/?token={token}&url={target_url}"

# Request and parse
response = requests.get(api_url)
soup = BeautifulSoup(response.text, "html.parser")
json_ld = soup.find_all("script", type="application/ld+json")[1].string
data = json.loads(json_ld)

# Extract fields
print("Name:", data["name"])
print("Address:", data["address"]["streetAddress"])
print("Price Range:", data["priceRange"])
print("Image URL:", data["image"])
print("Rating Value:", data["aggregateRating"]["ratingValue"])
print("Review Count:", data["aggregateRating"]["ratingCount"])
