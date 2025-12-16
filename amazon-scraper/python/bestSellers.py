import urllib.parse
import json
import csv
import requests
from bs4 import BeautifulSoup

# Configuration
token = "<SDO-token>"
category = "electronics"  # Change this to any best sellers category
geocode = "us"
max_pages = 2  # Best sellers shows 50 products per page

# Build base URL
base_url = f"https://www.amazon.com/Best-Sellers-Electronics/zgbs/{category}/"

# playWithBrowser actions: scroll to pagination to load all products
play_actions = [
    {"Action": "ScrollTo", "Selector": ".a-pagination"},
    {"Action": "Wait", "Timeout": 3000}
]
encoded_actions = urllib.parse.quote(json.dumps(play_actions))

all_products = []

# Loop through pages
for page in range(1, max_pages + 1):
    print(f"Scraping page {page}...")

    # Build URL for current page
    if page == 1:
        target_url = base_url
    else:
        target_url = f"{base_url}ref=zg_bs_pg_{page}_{category}?_encoding=UTF8&pg={page}"

    # Make API request
    targetUrl = urllib.parse.quote(target_url)
    apiUrl = "https://api.scrape.do/?token={}&url={}&geoCode={}&render=true&playWithBrowser={}".format(token, targetUrl, geocode, encoded_actions)
    response = requests.request("GET", apiUrl)

    soup = BeautifulSoup(response.text, "html.parser")

    # Find all product items
    product_items = soup.find_all(class_="zg-no-numbers")

    for index, item in enumerate(product_items, start=1):
        try:
            # Ranking
            ranking = str(index + (page - 1) * 50)

            # ASIN
            asin_elem = item.find(attrs={"data-asin": True})
            asin = asin_elem.get("data-asin", "") if asin_elem else ""

            # Image
            img_tag = item.find("img")
            image = img_tag.get("src", "") if img_tag else ""

            # Name & Link
            name = ""
            link = ""
            for a_tag in item.find_all("a", class_="a-link-normal"):
                href = a_tag.get("href", "")
                text = a_tag.get_text(strip=True)
                if "/dp/" in href and text and not text.startswith("EUR") and not text.startswith("$"):
                    link = "https://www.amazon.com" + href if not href.startswith("http") else href
                    name = text
                    break

            # Price
            price_tag = item.find("span", class_=lambda x: x and "p13n-sc-price" in str(x))
            price = price_tag.get_text(strip=True) if price_tag else "N/A"

            # Rating & Review Count
            rating = ""
            review_count = ""
            star_icon = item.find("i", class_=lambda x: x and "a-icon-star" in str(x))
            if star_icon:
                parent_link = star_icon.find_parent("a")
                if parent_link:
                    aria_label = parent_link.get("aria-label", "")
                    if aria_label and "stars" in aria_label:
                        parts = aria_label.split("stars")
                        rating = parts[0].strip() + " stars" if parts[0] else ""
                        if len(parts) > 1:
                            review_part = parts[1].strip().lstrip(",").strip()
                            review_count = review_part.replace(" ratings", "")

            if name:
                all_products.append({
                    "Ranking": ranking,
                    "ASIN": asin,
                    "Name": name,
                    "Price": price,
                    "Rating": rating,
                    "Review Count": review_count,
                    "Link": link,
                    "Image": image
                })
        except:
            continue

    print(f"  Found {len(product_items)} products on page {page}")

# Export to CSV
csv_file = "bestSellers.csv"
headers = ["Ranking", "ASIN", "Name", "Price", "Rating", "Review Count", "Link", "Image"]

with open(csv_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=headers)
    writer.writeheader()
    writer.writerows(all_products)

print(f"\nTotal products scraped: {len(all_products)}")
print(f"Data exported to {csv_file}")
