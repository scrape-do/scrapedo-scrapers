import csv
from bs4 import BeautifulSoup
import requests
import urllib.parse

# Our token provided by Scrape.do
token = "<your_token>"

# Target Chewy product URL
target_url = urllib.parse.quote_plus("<target_product_url>")  # Example: https://www.chewy.com/purina-pro-plan-shredded-blend-adult/dp/114030

# Optional parameters
render = "true"
geo_code = "us"
super_mode = "true"

# Scrape.do API endpoint
url = f"http://api.scrape.do/?token={token}&url={target_url}&render={render}&geoCode={geo_code}&super={super_mode}"

# Send the request
response = requests.request("GET", url)

# Parse the response using BeautifulSoup
soup = BeautifulSoup(response.text, "html.parser")

# Extract product title
title = soup.find("h1", attrs={"data-testid": "product-title-heading"}).text.strip()

# Extract product price
price = soup.find("div", attrs={"data-testid": "advertised-price"}).text.strip()

# Save extracted data to CSV
with open("chewy_product_data.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Product Name", "Price"])
    writer.writerow([title, price])

print("Data saved to chewy_product_data.csv")