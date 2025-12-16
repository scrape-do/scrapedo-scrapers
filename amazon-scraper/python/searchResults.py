import urllib.parse
import csv
import requests
from bs4 import BeautifulSoup

# Configuration
token = "<SDO-token>"
search_query = "laptop stands"  # Change this to any search term
geocode = "us"
zipcode = "10001"
max_pages = 4  # Number of result pages to scrape

all_products = []

# Loop through all result pages
for page in range(1, max_pages + 1):
    print(f"Scraping page {page}...")

    # Build search URL with page number
    target_url = f"https://www.amazon.com/s?k={urllib.parse.quote_plus(search_query)}&page={page}"

    # Make API request
    targetUrl = urllib.parse.quote(target_url)
    apiUrl = "https://api.scrape.do/plugin/amazon/?token={}&url={}&geocode={}&zipcode={}&output=html".format(token, targetUrl, geocode, zipcode)
    response = requests.request("GET", apiUrl)

    soup = BeautifulSoup(response.text, "html.parser")

    # Parse products on the current page
    product_elements = soup.find_all("div", {"class": "s-result-item"})
    page_count = 0

    for product in product_elements:
        try:
            # Extract product details
            name = product.select_one("h2 span").text
            try:
                price = str(product.select("span.a-price")).split('a-offscreen">')[1].split('</span>')[0]
            except:
                price = "N/A"
            link = product.select_one(".a-link-normal").get("href")
            image = product.select_one("img").get("src")

            if name:
                all_products.append({
                    "Name": name,
                    "Price": price,
                    "Link": link,
                    "Image": image
                })
                page_count += 1
        except:
            continue

    print(f"  Found {page_count} products on page {page}")

# Export to CSV
csv_file = "searchResults.csv"
headers = ["Name", "Price", "Link", "Image"]

with open(csv_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=headers)
    writer.writeheader()
    writer.writerows(all_products)

print(f"\nTotal products scraped: {len(all_products)}")
print(f"Data exported to {csv_file}")
