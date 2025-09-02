import requests
import urllib.parse
from bs4 import BeautifulSoup
import csv
import time
import json
import os

# Scrape.do token
TOKEN = "<your-token>"

# Walmart categories to track
CATEGORY_URLS = [
    "https://www.walmart.com/browse/food/shop-all-deli-sliced-meats-cheeses/976759_976789_5428795_9084734",
    "https://www.walmart.com/browse/food/snacks/976759_976787"
]

# Store info for Secaucus Supercenter
ZIPCODE = "07094"
STORE_ID = "3520"

def fetch_page(url, previous_url):
    headers = {
        "sd-User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
        "sd-Referer": previous_url
    }

    encoded_url = urllib.parse.quote(url)
    api_url = f"https://api.scrape.do/plugin/walmart/store?token={TOKEN}&zipcode={ZIPCODE}&storeid={STORE_ID}&url={encoded_url}&super=true&geoCode=us&extraHeaders=true&render=true&customWait=5000&blockResources=false"

    response = requests.get(api_url, headers=headers)
    response.raise_for_status()
    return response.text

def parse_products(html):
    soup = BeautifulSoup(html, "html.parser")
    products = []
    for tile in soup.select("[data-dca-name='ui_product_tile:vertical_index']"):
        product = {}

        # Name
        name_tag = tile.select_one("span[data-automation-id='product-title']")
        product["Name"] = name_tag.get_text(strip=True) if name_tag else "N/A"

        # Link
        link_tag = tile.select_one("a[href]")
        href = link_tag["href"] if link_tag else ""
        href = "https://www.walmart.com" + href if href.startswith("/") else href
        product["Link"] = href

        # Image
        img_tag = tile.select_one("img[data-testid='productTileImage']")
        product["Image"] = img_tag["src"] if img_tag and img_tag.has_attr("src") else ""

        # Price
        price_tag = tile.find("div", {"data-automation-id": "product-price"})
        price_section = price_tag.find("span", {"class": "w_iUH7"}) if price_tag else None
        product["Price"] = price_section.get_text(strip=True) if price_section else "N/A"

        # Reviews & Rating
        review_count_tag = tile.select_one('span[data-testid="product-reviews"]')
        product["ReviewCount"] = review_count_tag.get("data-value") if review_count_tag else None
        product["Rating"] = ""
        if review_count_tag:
            next_span = review_count_tag.find_next_sibling("span")
            if next_span:
                product["Rating"] = next_span.get_text(strip=True).split(" ")[0]

        # Stock availability
        add_to_cart = tile.find("button", {"data-automation-id": "add-to-cart"})
        product["Stock"] = "In stock" if add_to_cart else "Out of stock"

        products.append(product)
    return products

def scrape_category(base_url, max_pages=5, delay=1.5):
    all_products = []
    page = 1
    while page <= max_pages:
        if page == 1:
            html = fetch_page(base_url, base_url)
        elif page == 2:
            html = fetch_page(f"{base_url}?page=2", base_url)
        else:
            html = fetch_page(f"{base_url}?page={page}", f"{base_url}?page={page-1}")

        products = parse_products(html)
        if not products:
            break

        all_products.extend(products)
        page += 1
        time.sleep(delay)
    return all_products

def save_snapshot(filename, rows):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)

def load_snapshot(filename):
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def compare_snapshots(old_data, new_data):
    alerts = []

    # Build quick lookup by product link
    old_map = {p["Link"]: p for p in old_data}
    for prod in new_data:
        link = prod["Link"]
        old_prod = old_map.get(link)

        if old_prod:
            # Check price change
            if prod["Price"] != old_prod.get("Price"):
                alerts.append(f"Price change for {prod['Name']}: {old_prod.get('Price')} -> {prod['Price']}")

            # Check stock change
            if prod["Stock"] != old_prod.get("Stock"):
                alerts.append(f"Stock change for {prod['Name']}: {old_prod.get('Stock')} -> {prod['Stock']}")

    return alerts

# Main tracking logic
print("Starting price tracking...")
print(f"Monitoring {len(CATEGORY_URLS)} categories")

for i, url in enumerate(CATEGORY_URLS, 1):
    category_name = url.split("/")[5]  # crude way to name file
    snapshot_file = f"{category_name}_snapshot.json"
    
    print(f"\n[{i}/{len(CATEGORY_URLS)}] Processing category: {category_name}")
    
    print("Loading previous snapshot...")
    old_snapshot = load_snapshot(snapshot_file)
    print(f"Previous snapshot: {len(old_snapshot)} products")
    
    print("Scraping current data...")
    new_snapshot = scrape_category(url, max_pages=20)
    print(f"Current data: {len(new_snapshot)} products")
    
    print("Saving snapshot...")
    save_snapshot(snapshot_file, new_snapshot)

    # Export latest data to CSV
    print("Exporting to CSV...")
    csv_file = f"{category_name}_latest.csv"
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["Name", "Price", "Link", "Image", "Rating", "ReviewCount", "Stock"])
        writer.writeheader()
        writer.writerows(new_snapshot)

    # Print alerts
    print("Checking for changes...")
    alerts = compare_snapshots(old_snapshot, new_snapshot)
    if alerts:
        print(f"🚨 {len(alerts)} changes detected for {category_name}:")
        for alert in alerts:
            print(f"  • {alert}")
    else:
        print(f"✓ No changes detected for {category_name}")

print(f"\n✓ Price tracking completed for all {len(CATEGORY_URLS)} categories")