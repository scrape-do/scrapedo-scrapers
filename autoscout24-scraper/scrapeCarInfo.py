from bs4 import BeautifulSoup
import requests
import urllib.parse
import re

# Our token provided by Scrape.do
token = "<your_token>"

# Target AutoScout24 listing URL
target_url = urllib.parse.quote_plus("<target_car_url>")  # Example: https://www.autoscout24.ch/de/d/porsche-911-coupe-38-turbo-pdk-12188643

# Optional parameters
render = "true"
geo_code = "ch"

# Scrape.do API endpoint
url = f"https://api.scrape.do/?token={token}&url={target_url}&geoCode={geo_code}&render={render}"

# Send the request
response = requests.request("GET", url)

# Parse the response using BeautifulSoup
soup = BeautifulSoup(response.text, "html.parser")

# Extract car name
title = soup.find("h1").text.strip()

# Search for the first occurrence of "CHF" followed by a number
match = re.search(r"CHF\s([\d'.,]+)", soup.get_text())

# Extract and clean the price if found
price = match.group(0).replace("\xa0", " ") if match else "Price not found"

print("Car Name:", title)
print("Car Price:", price)