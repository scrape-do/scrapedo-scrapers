import urllib.parse
import csv
import requests
from bs4 import BeautifulSoup

# Configuration
token = "<your-token>"
base_url = "https://www.amazon.com/s?k=laptop+stands"  # Change this to any search or category URL
max_result_page = 4

current_result_page = 1
all_products = []

# Loop through all result pages
while True:
    # Handle URLs with existing page parameter or add new one
    if "&page=" in base_url or "?page=" in base_url:
        target_url = base_url.replace("&page=1", "").replace("?page=1", "") + f"&page={current_result_page}"
    else:
        separator = "&" if "?" in base_url else "?"
        target_url = f"{base_url}{separator}page={current_result_page}"
    
    targetUrl = urllib.parse.quote(target_url)
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