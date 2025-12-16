import urllib.parse
import csv
import re
import requests
from bs4 import BeautifulSoup

# Configuration
token = "<SDO-token>"
asin = "B0DZDBWM5B"  # Change this to any product ASIN
geocode = "us"

# Build seller offers URL from ASIN
target_url = f"https://www.amazon.com/gp/product/ajax/aodAjaxMain/?asin={asin}"

# Make API request
targetUrl = urllib.parse.quote(target_url, safe="")
apiUrl = "https://api.scrape.do/?token={}&url={}&geoCode={}".format(token, targetUrl, geocode)
response = requests.request("GET", apiUrl)

soup = BeautifulSoup(response.text, "html.parser")

offers = []

for sold_by in soup.find_all("div", id="aod-offer-soldBy"):
    # Find parent container with price
    container = sold_by.parent
    while container and not container.find("span", class_="a-price-whole"):
        container = container.parent
    if not container:
        continue

    # Price
    whole = container.find("span", class_="a-price-whole")
    frac = container.find("span", class_="a-price-fraction")
    price = f"${whole.text.strip('.')}.{frac.text.strip()}" if whole else "N/A"

    # Seller
    seller_link = sold_by.find("a", href=lambda x: x and "/gp/aag/main" in x)
    seller = seller_link.text.strip() if seller_link else "Amazon.com"

    # Seller rating
    rating_div = sold_by.find("div", id="aod-offer-seller-rating")
    rating_text = " ".join(rating_div.find("span", class_="a-icon-alt").get_text().split()) if rating_div and rating_div.find("span", class_="a-icon-alt") else ""
    count_elem = rating_div.find("span", id=lambda x: x and "seller-rating-count" in str(x)) if rating_div else None
    count_text = " ".join(count_elem.get_text().split()) if count_elem else ""

    # Extract rating value
    rating_match = re.search(r"(\d+\.?\d*) out of 5", rating_text)
    seller_rating = rating_match.group(1) if rating_match else "N/A"

    # Extract rating count
    count_match = re.search(r"\((\d[\d,]*)\s*ratings\)", count_text)
    rating_count = count_match.group(1) if count_match else "N/A"

    # Extract positive percentage
    positive_match = re.search(r"(\d+)%\s*positive", count_text)
    positive_pct = f"{positive_match.group(1)}%" if positive_match else "N/A"

    # Ships from
    ships_div = container.find("div", id="aod-offer-shipsFrom")
    ships_elem = ships_div.find("span", class_="a-color-base") if ships_div else None
    ships_from = " ".join(ships_elem.get_text().split()) if ships_elem else "N/A"

    # Condition
    condition_div = container.find("div", id="aod-offer-heading")
    condition = " ".join(condition_div.get_text().split()) if condition_div else "New"

    # Delivery
    delivery_div = container.find("div", id=lambda x: x and "DELIVERY" in str(x).upper())
    delivery = " ".join(delivery_div.get_text().split())[:80] if delivery_div else "N/A"

    offers.append({
        "ASIN": asin,
        "Price": price,
        "Condition": condition,
        "Seller": seller,
        "Seller Rating": seller_rating,
        "Rating Count": rating_count,
        "Positive": positive_pct,
        "Ships From": ships_from,
        "Delivery": delivery
    })

print(f"Found {len(offers)} seller offers for ASIN: {asin}")

# Export to CSV
csv_file = "sellerOffers.csv"
headers = ["ASIN", "Price", "Condition", "Seller", "Seller Rating", "Rating Count", "Positive", "Ships From", "Delivery"]

with open(csv_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=headers)
    writer.writeheader()
    writer.writerows(offers)

print(f"Data exported to {csv_file}")
