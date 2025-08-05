from bs4 import BeautifulSoup
import requests
import urllib.parse

# Our token provided by Scrape.do
token = "<your_token>"

# Target Fnac product URL
target_url = urllib.parse.quote_plus("<target_product_url>")  # Example: https://www.fnac.com/Apple-iPhone-16-Pro-Max-6-9-5G-256-Go-Double-SIM-Noir-Titane/a17312773/w-4

# Optional parameters
render = "true"
geo_code = "fr"
super_mode = "true"

# Scrape.do API endpoint
url = f"https://api.scrape.do/?token={token}&url={target_url}&geoCode={geo_code}&super={super_mode}"

# Send the request
response = requests.request("GET", url)

# Parse the response using BeautifulSoup
soup = BeautifulSoup(response.text, "html.parser")

# Extract product title
title = soup.find("h1").text.strip()

# Extract product price
price = soup.find("span", class_="f-faPriceBox__price userPrice checked").text.strip()

print("Product Name:", title)
print("Product Price:", price)