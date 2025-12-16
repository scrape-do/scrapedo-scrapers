import urllib.parse
import csv
import requests
from bs4 import BeautifulSoup

# Configuration
token = "<SDO-token>"
asins = ["B0BLRJ4R8F", "B081YXWDTQ", "B07D74DT3B"]  # Change these to any product ASINs
geocode = "us"
zipcode = "10001"

all_products = []

# Loop through all ASINs
for asin in asins:
    # Build product URL from ASIN
    target_url = f"https://www.amazon.com/dp/{asin}"

    # Make API request
    targetUrl = urllib.parse.quote(target_url)
    apiUrl = "https://api.scrape.do/plugin/amazon/?token={}&url={}&geocode={}&zipcode={}&output=html".format(token, targetUrl, geocode, zipcode)
    response = requests.request("GET", apiUrl)

    soup = BeautifulSoup(response.text, "html.parser")

    # Extract product details
    try:
        name = soup.find(id="productTitle").text.strip()

        # Extract price
        if soup.find("div", id="outOfStockBuyBox_feature_div"):
            price = "Out of Stock"
        else:
            whole = soup.find(class_="a-price-whole")
            fraction = soup.find(class_="a-price-fraction")
            price = f"${whole.text}{fraction.text}" if whole and fraction else "N/A"

        # Extract image
        image_elem = soup.find("img", {"id": "landingImage"})
        image = image_elem["src"] if image_elem else "N/A"

        # Extract rating
        rating_elem = soup.find(class_="AverageCustomerReviews")
        rating = rating_elem.text.strip().split(" out of")[0] if rating_elem else "N/A"

        all_products.append({
            "ASIN": asin,
            "Name": name,
            "Price": price,
            "Image": image,
            "Rating": rating
        })

        print(f"Scraped: {asin} - {name[:50]}...")
    except Exception as e:
        print(f"Error scraping {asin}: {e}")
        continue

# Export to CSV
csv_file = "singleProduct.csv"
headers = ["ASIN", "Name", "Price", "Image", "Rating"]

with open(csv_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=headers)
    writer.writeheader()
    writer.writerows(all_products)

print(f"\nScraped {len(all_products)} products")
print(f"Data exported to {csv_file}")
