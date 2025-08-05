import requests
import urllib.parse
from bs4 import BeautifulSoup

# Your Scrape.do API token
token = "<your_token>"

# Target URL
target_url = "<target_person_url>"  # Example: https://www.fastpeoplesearch.com/john-doe
encoded_url = urllib.parse.quote_plus(target_url)

# Scrape.do API endpoint - enabling "super=true" and "geoCode=us" for US-based residential proxies
api_url = f"https://api.scrape.do/?token={token}&url={encoded_url}&super=true&geoCode=us"

# Send the request and parse HTML
response = requests.get(api_url)
soup = BeautifulSoup(response.text, "html.parser")

# Extract name, city, state
header = soup.find("h1", id="details-header")
name, location = header.get_text(" ").strip().split(" in ", 1)
city, state = [part.strip() for part in location.split(",", 1)]

# Extract age
age = soup.find("h2", id="age-header").text.strip().replace("Age ", "")

# Extract address
addr = soup.find("div", id="current_address_section").find("a")
address = next(line for line in addr.stripped_strings)

# Print output
print("Name:", name)
print("Age:", age)
print("City:", city)
print("State:", state)
print("Address:", address)