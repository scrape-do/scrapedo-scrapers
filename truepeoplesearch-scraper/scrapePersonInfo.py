import requests
import urllib.parse
from bs4 import BeautifulSoup
import json

token = "<your_token>"
target_url = "<target_person_url>"
encoded_url = urllib.parse.quote_plus(target_url)
api_url = f"https://api.scrape.do/?token={token}&url={encoded_url}&super=true&geoCode=us"

response = requests.get(api_url)
soup = BeautifulSoup(response.text, "html.parser")

# Name and age from data attributes
person = soup.find("div", id="personDetails")
name = f"{person['data-fn']} {person['data-ln']}"
age = person["data-age"]

# JSON-LD structured data
person_data = None
for script in soup.find_all("script", type="application/ld+json"):
    try:
        data = json.loads(script.string)
        if isinstance(data, dict) and data.get("@type") == "ProfilePage":
            person_data = data.get("mainEntity", {})
            break
    except (json.JSONDecodeError, TypeError):
        pass

address_data = person_data.get("address", {})
phones = person_data.get("telephone", [])
emails = person_data.get("email", [])
aliases = person_data.get("alternateName", [])
relatives = [rel.get("name", "") for rel in person_data.get("relatedTo", [])]

print(f"Name: {name}")
print(f"Age: {age}")
print(f"Address: {address_data.get('streetAddress', '')}")
print(f"City: {address_data.get('addressLocality', '')}")
print(f"State: {address_data.get('addressRegion', '')}")
print(f"ZIP: {address_data.get('postalCode', '')}")
print(f"Phone: {phones[0] if phones else ''}")
print(f"Email: {emails[0] if emails else ''}")
print(f"Aliases: {', '.join(aliases)}")
print(f"Relatives: {', '.join(relatives[:5])}")
