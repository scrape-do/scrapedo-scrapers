import requests
import urllib.parse
from bs4 import BeautifulSoup
import csv
import time

# Scrape.do token
TOKEN = "<your-token>"

# Walmart category page (example: deli meats & cheeses)
target_url = "https://www.walmart.com/browse/food/shop-all-deli-sliced-meats-cheeses/976759_976789_5428795_9084734"

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
        name_tag = tile.select_one("span", {"data-automation-id": "product-title"}).get_text(strip=True)
        product["Name"] = name_tag.split("$")[0] if "$" in name_tag else name_tag

        # Link
        link_tag = tile.select_one("a", href=True)
        if link_tag:
            href = link_tag["href"]
            if href.startswith("/"):
                href = "https://www.walmart.com" + href
            product["Link"] = href
        else:
            product["Link"] = ""

        # Image
        img_tag = tile.select_one("img", {"data-testid": "productTileImage"})
        product["Image"] = img_tag["src"] if img_tag and img_tag.has_attr("src") else ""

        # Price
        price_tag = tile.find("div", {"data-automation-id": "product-price"})
        price_section = price_tag.find("span", {"class": "w_iUH7"}) if price_tag else None
        product["Price"] = "$" + price_section.get_text(strip=True).split("$")[1].split(" ")[0] if price_section else ""

        # Reviews & rating
        review_count_tag = tile.select_one('span[data-testid="product-reviews"]')
        product["ReviewCount"] = review_count_tag.get("data-value") if review_count_tag else None

        product["Rating"] = ""
        if review_count_tag:
            next_span = review_count_tag.find_next_sibling("span")
            if next_span:
                product["Rating"] = next_span.get_text(strip=True).split(" ")[0]

        products.append(product)

    return products

def scrape_category(base_url, max_pages=50, delay=1.5):
    all_products = []
    seen_images = set()  # track unique product images across pages
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
            print(f"No products found on page {page}. Stopping.")
            break

        new_count = 0
        for prod in products:
            img = prod.get("Image")
            if img and img not in seen_images:
                seen_images.add(img)
                all_products.append(prod)
                new_count += 1
            else:
                print(f"Duplicate skipped: {prod.get('Name')}")

        print(f"Page {page}: extracted {new_count} new products (total {len(all_products)})")

        page += 1
        time.sleep(delay)  # polite delay
    return all_products

# Run scraper and save output
print("Starting category scraping...")
rows = scrape_category(target_url, max_pages=20)

print("Saving results to CSV...")
with open("walmart_category.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["Name", "Price", "Link", "Image", "Rating", "ReviewCount"])
    writer.writeheader()
    writer.writerows(rows)

print(f"✓ Successfully extracted {len(rows)} products to walmart_category.csv")