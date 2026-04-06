import requests
from bs4 import BeautifulSoup
import urllib.parse
import json

TOKEN = "<your-token>"
PROPERTY_URL = "https://www.rightmove.co.uk/properties/171185315#/"

encoded_url = urllib.parse.quote(PROPERTY_URL, safe="")
api_url = f"http://api.scrape.do/?token={TOKEN}&url={encoded_url}"

response = requests.get(api_url)
if response.status_code != 200:
    print(f"Request failed with status {response.status_code}")
    exit()

soup = BeautifulSoup(response.text, "html.parser")

page_model = None
for script in soup.find_all("script"):
    text = script.string or ""
    if "window.PAGE_MODEL" not in text:
        continue

    start = text.find("window.PAGE_MODEL = ") + len("window.PAGE_MODEL = ")
    depth = 0
    i = start
    while i < len(text):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
        if depth == 0:
            break
        i += 1
    page_model = json.loads(text[start : i + 1])
    break

if not page_model:
    print("Could not find PAGE_MODEL data")
    exit()

pd = page_model["propertyData"]

price_info = pd.get("prices", {})
address_info = pd.get("address", {})
sizings = pd.get("sizings", [])
tenure_info = pd.get("tenure", {})
stations = pd.get("nearestStations", [])

sqft = ""
for s in sizings:
    if s.get("unit") == "sqft":
        sqft = s.get("minimumSize", "")

nearest_station = ""
station_distance = ""
if stations:
    nearest_station = stations[0].get("name", "")
    station_distance = stations[0].get("distance", "")

property_data = {
    "id": pd.get("id", ""),
    "address": address_info.get("displayAddress", ""),
    "postcode": f"{address_info.get('outcode', '')} {address_info.get('incode', '')}".strip(),
    "price": price_info.get("primaryPrice", ""),
    "price_qualifier": price_info.get("displayPriceQualifier", ""),
    "price_per_sqft": price_info.get("pricePerSqFt", ""),
    "property_type": pd.get("propertySubType", ""),
    "bedrooms": pd.get("bedrooms", ""),
    "bathrooms": pd.get("bathrooms", ""),
    "size_sqft": sqft,
    "tenure": tenure_info.get("tenureType", ""),
    "description": pd.get("text", {}).get("description", ""),
    "nearest_station": nearest_station,
    "station_distance": f"{station_distance} miles" if station_distance else "",
    "url": PROPERTY_URL,
}

for key, value in property_data.items():
    print(f"{key}: {value}")
