import requests
import urllib.parse
from bs4 import BeautifulSoup
import re

# Your Scrape.do API token
token = "<your-token>"

# Target URL
target_url = "<target-url>" # Example: https://www.zillow.com/homedetails/8926-Silver-City-San-Antonio-TX-78254/124393863_zpid/
encoded_url = urllib.parse.quote_plus(target_url)

# Scrape.do API endpoint - enabling super=true for premium proxies
api_url = f"https://api.scrape.do/?token={token}&url={encoded_url}&super=true"

# Get and parse HTML
response = requests.get(api_url)
soup = BeautifulSoup(response.text, "html.parser")
html_text = soup.get_text()

# Extract price
price = (soup.find("span", {"data-testid": "price"})).get_text().strip()

# Extract address, city, and state
address_match = re.search(r'(\d+\s+[^,]+),\s*([^,]+),\s*(\w{2})\s+\d{5}', html_text)
street, city, state = address_match.groups()

# Extract "days on Zillow" - look for exact phrase with flexible spacing
days_match = re.search(r'(\d+)\s+days?\s*on\s+Zillow', html_text, re.IGNORECASE)
days_on = days_match.group(1)

# Extract Zestimate
zestimate_match = re.search(r'\$[\d,]+(?=\s*Zestimate)', html_text)
zestimate = zestimate_match.group()

# Print results
print("Price:", price)
print("Address:", street)
print("City:", city)
print("State:", state)
print("Days on Zillow:", days_on)
print("Zestimate:", zestimate)