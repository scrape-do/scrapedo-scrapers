import requests
import urllib.parse
from bs4 import BeautifulSoup
import json

def clean_text(text):
    return (text
            .replace("Â®", "®")
            .replace("â¢", "™")
            .replace("â", "'")
            .replace("Â", "")
            .replace("Whatâs", "What's")
            .replace("Ã", "A")
            .strip())

# Your Scrape.do token
token = "<your-token>"

# Target URL
target_url = urllib.parse.quote_plus("https://www.zomato.com/ncr/mcdonalds-janpath-new-delhi/order")
api_url = f"http://api.scrape.do/?token={token}&url={target_url}"

# Fetch and parse
response = requests.get(api_url)
soup = BeautifulSoup(response.text, "html.parser")
script = soup.find("script", string=lambda s: s and "window.__PRELOADED_STATE__" in s)

# Extract JSON from window.__PRELOADED_STATE__
json_text = script.string.split('JSON.parse("')[1].split('")')[0]
data = json.loads(json_text.encode().decode('unicode_escape'))

# Restaurant Info
restaurant = data["pages"]["restaurant"]["182"]
info = restaurant["sections"]["SECTION_BASIC_INFO"]
contact = restaurant["sections"]["SECTION_RES_CONTACT"]

name = info["name"]
location = contact["address"]  # <-- full address here
rating_data = info["rating_new"]["ratings"]["DELIVERY"]
rating = rating_data["rating"]
review_count = rating_data["reviewCount"]

print(f"Restaurant: {name}")
print(f"Address   : {location}")
print(f"Delivery Rating: {rating} ({review_count} reviews)\n")

# Menu Extraction
menus = restaurant["order"]["menuList"]["menus"]
for menu in menus:
    category = clean_text(menu["menu"]["name"])
    for cat in menu["menu"]["categories"]:
        for item in cat["category"]["items"]:
            item_name = clean_text(item["item"]["name"])
            item_price = item["item"]["price"]
            print(f"{category} - {item_name}: ₹{item_price}")
