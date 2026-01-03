import requests
import urllib.parse
from bs4 import BeautifulSoup

# Your Scrape.do API token
token = "<your_token>"

# Target URL
target_url = "<target_person_url>"  # Example: https://www.peoplesearchnow.com/person/john-doe
encoded_url = urllib.parse.quote_plus(target_url)

# Scrape.do API endpoint - enabling "super=true" and "geoCode=us" for US-based residential proxies
api_url = f"https://api.scrape.do/?token={token}&url={encoded_url}&super=true&geoCode=us"

# Send the request and parse HTML
response = requests.get(api_url)
soup = BeautifulSoup(response.text, "html.parser")

# Extract name
name_elem = soup.find("h1", class_="name")
name = name_elem.text.strip() if name_elem else ""

# Extract age
age_elem = soup.find("div", class_="age")
age = age_elem.text.strip().replace("Age: ", "").replace("Age ", "") if age_elem else ""

# Extract address information
address_elem = soup.find("div", class_="address")
if address_elem:
    address_parts = address_elem.find_all("span")
    address = address_parts[0].text.strip() if len(address_parts) > 0 else ""
    city_state = address_parts[1].text.strip() if len(address_parts) > 1 else ""
    
    # Parse city and state from "City, State" format
    if city_state and "," in city_state:
        city, state = [part.strip() for part in city_state.split(",", 1)]
    else:
        city = city_state
        state = ""
else:
    address = ""
    city = ""
    state = ""

# Print output
print("Name:", name)
print("Age:", age)
print("Address:", address)
print("City:", city)
print("State:", state)
