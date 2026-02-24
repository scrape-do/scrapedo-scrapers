import requests
import urllib.parse
from bs4 import BeautifulSoup
import json
import re

token = "<your_token>"
target_url = "<target_person_url>"
encoded_url = urllib.parse.quote_plus(target_url)
api_url = f"https://api.scrape.do/?token={token}&url={encoded_url}&super=true&geoCode=us"

response = requests.get(api_url)
soup = BeautifulSoup(response.text, "html.parser")

# Name, city, state from header
header = soup.find("h1", id="details-header")
name, location = header.get_text(" ").strip().split(" in ", 1)
city, state = [part.strip() for part in location.split(",", 1)]

# Age from header
age = soup.find("h2", id="age-header").text.strip().replace("Age ", "")

# Address from HTML
addr = soup.find("div", id="current_address_section").find("a")
address = next(line for line in addr.stripped_strings)

# JSON-LD Person data
person_data = None
for script in soup.find_all("script", type="application/ld+json"):
    try:
        data = json.loads(script.string)
        if isinstance(data, dict) and data.get("@type") == "Person":
            person_data = data
            break
    except (json.JSONDecodeError, TypeError):
        pass

zipcode = person_data.get("homeLocation", {}).get("address", {}).get("postalCode", "")
phones = person_data.get("telephone", [])
aliases = person_data.get("additionalName", [])
relatives = [rel.get("name", "") for rel in person_data.get("relatedTo", [])]

# Emails from FAQ JSON-LD
emails = []
for script in soup.find_all("script", type="application/ld+json"):
    try:
        data = json.loads(script.string)
        if isinstance(data, dict) and data.get("@type") == "FAQPage":
            for q in data.get("mainEntity", []):
                if "email" in q.get("name", "").lower():
                    answer = q.get("acceptedAnswer", {}).get("text", "")
                    emails.extend(re.findall(r"[\w.+-]+@[\w-]+\.[\w.-]+", answer))
    except (json.JSONDecodeError, TypeError):
        pass
emails = list(dict.fromkeys(emails))

print(f"Name: {name}")
print(f"Age: {age}")
print(f"Address: {address}")
print(f"City: {city}")
print(f"State: {state}")
print(f"ZIP: {zipcode}")
print(f"Phone: {phones[0] if phones else ''}")
print(f"Email: {emails[0] if emails else ''}")
print(f"Aliases: {', '.join(aliases[:5])}")
print(f"Relatives: {', '.join(relatives[:5])}")