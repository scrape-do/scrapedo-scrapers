from bs4 import BeautifulSoup
import requests
import urllib.parse
import re

# Our token provided by Scrape.do
token = "<your_token>"

# Target Imovelweb listing URL
target_url = urllib.parse.quote_plus("<target_property_url>")  # Example: https://www.imovelweb.com.br/propriedades/casa-no-condominio-east-village-disponivel-para-venda-2986272608.html

# Optional parameters
render = "true"
geo_code = "br"

# Scrape.do API endpoint
url = f"https://api.scrape.do/?token={token}&url={target_url}&geoCode={geo_code}&render={render}"

# Send the request
response = requests.request("GET", url)

# Parse the response using BeautifulSoup
soup = BeautifulSoup(response.text, "html.parser")

# Extract listing name
listing_name = soup.find("h1").text.strip()

# Extract square meters from title-type-sup-property
title_content = soup.find("h2", class_="title-type-sup-property").text.strip()
square_meters = re.search(r"(\d+)\s*m²", title_content).group(1)

# Extract sale price and remove unwanted words
price_text = " ".join(soup.find("div", class_="price-value").stripped_strings)
price = re.search(r"R\$\s*[\d.,]+", price_text).group(0)

print("Listing Name:", listing_name)
print("Square Meters:", square_meters)
print("Sale Price:", price)