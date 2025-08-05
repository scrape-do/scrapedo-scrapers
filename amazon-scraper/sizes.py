import csv
import requests
from bs4 import BeautifulSoup
import urllib.parse

# Our token provided by Scrape.do
token = "<your-token>"

targetUrl = urllib.parse.quote_plus("https://us.amazon.com/Calvin-Klein-Classics-Multipack-T-Shirts/dp/B08SM3QZJG/")

jsonData = '[{"Action": "Click","Selector":"#dropdown_selected_size_name"},' \
           '{ "Action": "Wait", "Timeout": 5000 }]'
encodedJsonData = urllib.parse.quote_plus(jsonData)
render = "true"
url = f"http://api.scrape.do?token={token}&url={targetUrl}&render={render}&playWithBrowser={encodedJsonData}&geoCode=us"
response = requests.request("GET", url)

# Parse the request using BS
soup = BeautifulSoup(response.text, "html.parser")
size_options = soup.find_all("a", {"class": "a-dropdown-link"})

size_options_list = []

for size_option in size_options:
    if size_option.text != "    Select     ":
        size_options_list.append([size_option.text, size_option.get("data-value").split(",")[1][:-2]])

prices = {}

for option in size_options_list:
    targetUrl = urllib.parse.quote_plus(f"https://us.amazon.com/Calvin-Klein-Classics-Multipack-T-Shirts/dp/"
                                        f"{option[1]}/?th=1&psc=1")
    urlOptions = f"http://api.scrape.do?token={token}&url={targetUrl}&geoCode=us"
    responseOptions = requests.request("GET", urlOptions)
    soupOptions = BeautifulSoup(responseOptions.text, "html.parser")
    price = soupOptions.find(class_="priceToPay").text.strip()

    size = option[0].strip()
    prices[size] = price

# Scrape product details
product_name = soup.find(id="productTitle").text.strip()

# Export to CSV
header = ["Name"] + [f"{size} Price" for size in prices.keys()]
row = [product_name] + [price for price in prices.values()]

with open('out.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows([header, row])

