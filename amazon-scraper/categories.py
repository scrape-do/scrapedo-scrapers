import urllib.parse
import csv
import requests
from bs4 import BeautifulSoup

# Our token provided by 'Scrape.do'
token = "<your-token>"

current_result_page = 1
max_result_page = 20

# Initialize list to store product data
all_products = []


# Loop through all result pages
while True:

    targetUrl = urllib.parse.quote("https://www.amazon.com/s?k=laptop+stands&page={}".format(current_result_page))
    apiUrl = "https://api.scrape.do?token={}&url={}".format(token, targetUrl)
    response = requests.request("GET", apiUrl)

    soup = BeautifulSoup(response.text, "html.parser")

    # Parse products on the current page
    product_elements = soup.find_all("div", {"class": "s-result-item"})
    if current_result_page > max_result_page:
        break
    for product in product_elements:
        try:
            # Extract product details
            name = product.select_one("h2 span").text
            try:
                price = str(product.select("span.a-price")).split('a-offscreen">')[1].split('</span>')[0]
            except:
                price = "Price not available"
            link = product.select_one(".a-link-normal").get("href")
            image = product.select_one("img").get("src")
            # Append data to the list
            if name:
                all_products.append({"Name": name, "Price": price, "Link": link, "Image": image})
        except:
            continue
    current_result_page += 1

# Export the data to a CSV file
csv_file = "amazon_search_results.csv"
headers = ["Name", "Price", "Link", "Image"]

with open(csv_file, "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=headers)
    writer.writeheader()
    writer.writerows(all_products)

print(f"Data successfully exported to {csv_file}")
