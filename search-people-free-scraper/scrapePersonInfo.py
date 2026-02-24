import requests
import urllib.parse
from bs4 import BeautifulSoup
import json
import re

token = "<your_token>"
target_url = "<target_person_url>"  # e.g. https://www.searchpeoplefree.com/find/john-smith/abc123
encoded_url = urllib.parse.quote_plus(target_url)
api_url = f"https://api.scrape.do/?token={token}&url={encoded_url}&super=true&geoCode=us"

response = requests.get(api_url)
soup = BeautifulSoup(response.text, "html.parser")

person = None
for script in soup.find_all("script", type="application/ld+json"):
    try:
        data = json.loads(script.string)
        if isinstance(data, dict) and data.get("@type") == "Person":
            person = data
            break
    except (json.JSONDecodeError, TypeError):
        pass

if person:
    name = person.get("name", "")
    phones = person.get("telephone", [])
    emails = person.get("email", [])

    address_data = person.get("contentLocation", {}).get("address", {})
    street = address_data.get("streetAddress", "")
    city = address_data.get("addressLocality", "")
    state = address_data.get("addressRegion", "")
    zipcode = address_data.get("postalCode", "")

    current = soup.find("article", class_="current-bg")
    age_match = re.search(r"Age\s+(\d+)", current.get_text()) if current else None
    age = age_match.group(1) if age_match else ""

    family = [rel.get("name", "") for rel in person.get("relatedTo", [])]
    spouse = [s.get("name", "") for s in person.get("spouse", [])]

    print(f"Name: {name}")
    print(f"Age: {age}")
    print(f"Address: {street}")
    print(f"City: {city}")
    print(f"State: {state}")
    print(f"ZIP: {zipcode}")
    print(f"Phone: {phones[0] if phones else ''}")
    print(f"Email: {emails[0] if emails else ''}")
    print(f"Spouse: {', '.join(spouse)}")
    print(f"Family: {', '.join(family[:5])}")
