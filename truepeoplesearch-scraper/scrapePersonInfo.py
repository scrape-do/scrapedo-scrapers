import requests
import urllib.parse
from bs4 import BeautifulSoup

# Your Scrape.do API token
token = "<your_token>"

# Target URL
target_url = "<target_person_url>"  # Example: https://www.truepeoplesearch.com/find/person/jane-doe
encoded_url = urllib.parse.quote_plus(target_url)

# Scrape.do API endpoint - enabling "super=true" and "geoCode=us" for US-based residential proxies
api_url = f"https://api.scrape.do/?token={token}&url={encoded_url}&super=true&geoCode=us"

# Send the request and parse HTML
response = requests.get(api_url)
soup = BeautifulSoup(response.text, "html.parser")

# Extract name and age
person = soup.find("div", id="personDetails")
name = f"{person['data-fn']} {person['data-ln']}"
age = person["data-age"]

# Extract address, city, state
addr = soup.find("a", {"data-link-to-more": "address"})
address = addr.find("span", itemprop="streetAddress").text.strip()
city = addr.find("span", itemprop="addressLocality").text.strip()
state = addr.find("span", itemprop="addressRegion").text.strip()

# Extract phone number
phone = soup.find("a", {"data-link-to-more": "phone"}).find("span", itemprop="telephone").text.strip()

# Print output
print("Name:", name)
print("Age:", age)
print("Address:", address)
print("City:", city)
print("State:", state)
print("Phone Number:", phone)