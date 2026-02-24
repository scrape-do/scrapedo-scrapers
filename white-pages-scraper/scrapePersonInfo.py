import requests
import urllib.parse
from bs4 import BeautifulSoup
import json

token = "<your_token>"
target_url = "<target_person_url>"  # e.g. https://www.whitepages.com/name/John-Doe/New-York-NY/abc123
encoded_url = urllib.parse.quote_plus(target_url)
api_url = f"https://api.scrape.do/?token={token}&url={encoded_url}&super=true&geoCode=us"

response = requests.get(api_url)
soup = BeautifulSoup(response.text, "html.parser")

name_el = soup.find("div", class_="big-name")
name = name_el.get_text(strip=True) if name_el else ""

address_line1 = soup.find("div", class_="address-line1")
address_line2 = soup.find("div", class_="address-line2")
street = address_line1.get_text(strip=True) if address_line1 else ""
location = address_line2.get_text(strip=True) if address_line2 else ""
city, state, zipcode = "", "", ""
if location:
    parts = location.split(",")
    city = parts[0].strip()
    if len(parts) > 1:
        state_zip = parts[1].strip().split()
        state = state_zip[0] if state_zip else ""
        zipcode = state_zip[1] if len(state_zip) > 1 else ""

phone_el = soup.find("a", attrs={"data-qa-selector": "phone-number-link"})
phone = phone_el.get_text(strip=True) if phone_el else ""

age = ""
for script in soup.find_all("script", type="application/ld+json"):
    try:
        data = json.loads(script.string)
        if isinstance(data, dict) and data.get("@type") == "Person":
            desc = data.get("description", "")
            age = desc.split("is ")[1].split(".")[0] if "is " in desc else ""
            break
    except (json.JSONDecodeError, TypeError):
        pass

print(f"Name: {name}")
print(f"Age: {age}")
print(f"Address: {street}")
print(f"City: {city}")
print(f"State: {state}")
print(f"ZIP: {zipcode}")
print(f"Phone: {phone}")
