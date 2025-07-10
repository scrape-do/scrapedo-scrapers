import requests
import urllib.parse
import csv

# Your Scrape.do token
token = "<your_token>"

# Product identifiers
channel_uid = "<product_channel_uid>"
product_id = "<product_id>"

# Build the Naver API URL
# 🔴 If you want to scrape smartstore domain instead, change URL structure to https://smartstore.naver.com/i/...
target_url = f"https://brand.naver.com/n/v2/channels/{channel_uid}/products/{product_id}?withWindow=false"
encoded_url = urllib.parse.quote_plus(target_url)

# Scrape.do API endpoint with premium proxy routing
api_url = f"https://api.scrape.do?token={token}&url={encoded_url}&super=true"

# Send the request
response = requests.get(api_url)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()

    # Extract relevant fields
    name = data.get("dispName", "N/A")
    price = data.get("discountedSalePrice", 0)
    discount = data.get("benefitsView", {}).get("discountedRatio", "0")
    image = data.get("representImage", {}).get("url", "")
    stock = data.get("stockQuantity", 0)

    # Export to CSV
    with open("naver_product_data.csv", "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["Product Name", "Price", "Discount", "Image URL", "Stock Quantity"])
        writer.writerow([name, price, f"{discount}%", image, stock])

    print("✅ Data saved to naver_product_data.csv")

else:
    print(f"❗ Request failed with status code {response.status_code}")
    print("Check if the channel_uid and product_id are correct, and verify that your token and region settings are valid.")
