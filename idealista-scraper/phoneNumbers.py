# ⚠️ Phone numbers are considered personal data under GDPR, and is strictly prohibited from being used for business usage or public sharing. It can only be allowed for purely personal usage or household activity, so unless you're scraping for a personal non-commercial project, don't extract phone numbers at scale.

import requests
import json
import urllib.parse
from bs4 import BeautifulSoup

TOKEN = "<your-token>"
TARGET_URL = "<your-target-url>" # e.g. https://www.idealista.com/inmueble/108889120/

play_with_browser = [
    {
        "action": "WaitSelector",
        "timeout": 30000,
        "waitSelector": "#didomi-notice-agree-button"
    },
    {
        "action": "Click",
        "selector": "#didomi-notice-agree-button"
    },
    {
        "action": "Wait",
        "timeout": 2000
    },
    {
        "action": "Execute",
        "execute": f"location.href='{TARGET_URL}'"
    },
    {
        "action": "WaitSelector",
        "timeout": 30000,
        "waitSelector": ".see-phones-btn"
    },
    {
        "action": "Click",
        "selector": ".see-phones-btn:not(.show-phone):not(.loading) .hidden-contact-phones_text"
    },
    {
        "Action": "WaitForRequestCompletion",
        "UrlPattern": "*example.com/image*",
        "Timeout": 10000
    },
    {
        "action": "Wait",
        "timeout": 1000
    }
]

jsonData = urllib.parse.quote_plus(json.dumps(play_with_browser))
api_url = (
    "https://api.scrape.do/?"
    f"url={urllib.parse.quote_plus('https://www.idealista.com/')}"
    f"&token={TOKEN}"
    f"&super=true"
    f"&render=true"
    f"&returnJSON=true"
    f"&blockResources=false"
    f"&playWithBrowser={jsonData}"
    f"&geoCode=es"
)

response = requests.get(api_url)

# Parse JSON response
json_map = json.loads(response.text)

# Parse HTML content
soup = BeautifulSoup(json_map.get("content", ""), "html.parser")

# Extract property title
title_element = soup.find("span", class_="main-info__title-main")
property_title = title_element.text.strip() if title_element else "Not found"

# Extract price
price_element = soup.find("span", class_="info-data-price")
price = price_element.text.strip() if price_element else "Not found"

# Extract phone number - try tel: links first, then text spans
phone_number = "Not found"
for link in soup.find_all("a", href=True):
    href = link.get("href", "")
    if href.startswith("tel:+34"):
        phone_number = href.replace("tel:", "")
        break

if phone_number == "Not found":
    for span in soup.find_all("span", class_="hidden-contact-phones_text"):
        text = span.text.strip()
        if any(char.isdigit() for char in text) and len(text.replace(" ", "")) >= 9:
            phone_number = text
            break

print(f"Property Title: {property_title}")
print(f"Price: {price}")
print(f"Phone Number: {phone_number}")