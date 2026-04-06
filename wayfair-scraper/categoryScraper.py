import json
import urllib.parse
import requests
from bs4 import BeautifulSoup
import time

TOKEN = "<your-token>"
BASE_URL = "https://www.wayfair.com/decor-pillows/sb0/full-length-mirrors-c1860918.html"
MAX_PAGES = 5

all_products = []

for page_num in range(1, MAX_PAGES + 1):
    print(f"Scraping page {page_num}/{MAX_PAGES}...")
    target_url = BASE_URL if page_num == 1 else f"{BASE_URL}?curpage={page_num}"

    api_url = f"http://api.scrape.do/?token={TOKEN}&url={urllib.parse.quote(target_url)}&super=true&render=true"
    response = requests.get(api_url, timeout=90)
    soup = BeautifulSoup(response.text, "html.parser")

    product_cards = soup.find_all(attrs={"data-test-id": "ListingCard"})

    for card in product_cards:
        name_elem = card.find(attrs={"data-name-id": "ListingCardName"})
        if not name_elem: continue
        product_name = name_elem.get_text(strip=True)

        price_elem = card.find(attrs={"data-test-id": "PriceDisplay"})
        price = price_elem.get_text(strip=True).replace("$", "").replace(",", "") if price_elem else None

        seller_elem = card.find(attrs={"data-name-id": "ListingCardManufacturer"})
        seller_name = seller_elem.get_text(strip=True).replace("By ", "") if seller_elem else "N/A"

        img_elem = card.find(attrs={"data-test-id": "ListingCard-ListingCardImageCarousel-LeadImage"})
        product_image = img_elem.get("src") if img_elem else None

        product_link = None
        for link in card.find_all("a"):
            href = link.get("href", "")
            if "/pdp/" in href:
                product_link = "https://www.wayfair.com" + href.split("?")[0] if href.startswith("/") else href.split("?")[0]
                break

        original_price = None
        discount_rate = None
        previous_container = card.find(attrs={"data-test-id": "StandardPricingPrice-PREVIOUS"})
        if previous_container:
            was_elem = previous_container.find(attrs={"data-test-id": "PriceDisplay"})
            if was_elem and price:
                original_price = was_elem.get_text(strip=True).replace("$", "").replace(",", "")
                try:
                    discount = ((float(original_price) - float(price)) / float(original_price)) * 100
                    discount_rate = f"{int(discount)}%"
                except (ValueError, ZeroDivisionError):
                    pass

        review_rating = None
        review_count = None
        review_label = card.find(attrs={"data-name-id": "ListingCardReviewStars-a11yLabel"})
        if review_label:
            label_text = review_label.get_text(strip=True)
            if "Rated " in label_text and " out of" in label_text:
                review_rating = label_text.split("Rated ")[1].split(" out of")[0]
            if "stars." in label_text and " total" in label_text:
                review_count = label_text.split("stars.")[1].split(" total")[0]

        if product_link and product_link not in [p["product_link"] for p in all_products]:
            all_products.append({
                "product_name": product_name,
                "seller_name": seller_name,
                "price": price,
                "original_price": original_price,
                "discount_rate": discount_rate,
                "review_rating": review_rating,
                "review_count": review_count,
                "product_image": product_image,
                "product_link": product_link
            })

    time.sleep(1)

with open("wayfair_category.json", "w", encoding="utf-8") as f:
    json.dump(all_products, f, indent=2, ensure_ascii=False)

print(f"Saved {len(all_products)} products to wayfair_category.json")
