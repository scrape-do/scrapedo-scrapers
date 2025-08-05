from bs4 import BeautifulSoup
import requests
import urllib.parse

# Our token provided by Scrape.do
token = "<your_token>"

# Target Mouser category URL
target_url = urllib.parse.quote_plus("<target_category_url>")  # Example: https://www.mouser.com/c/optoelectronics/led-lighting/led-bulbs-modules/

# Optional parameters
render = "true"
geo_code = "us"

# Scrape.do API endpoint
url = f"https://api.scrape.do/?token={token}&url={target_url}&geoCode={geo_code}&render={render}"

# Send the request
response = requests.request("GET", url)

# Parse the response using BeautifulSoup
soup = BeautifulSoup(response.text, "html.parser")

# Extract product name
name = soup.find("td", class_="column desc-column hide-xsmall").find("span").text.strip()

# Extract product price using span id
price = soup.find("span", id="lblPrice_1_1").text.strip()

print("Product Name:", name)
print("Product Price:", price)