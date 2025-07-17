import requests
from bs4 import BeautifulSoup
import csv

# Scrape.do API token and base URL for the region's restaurant listings
TOKEN = "<your-token>"
BASE_URL = "<region-url>"# e.g. https://hungerstation.com/sa-en/restaurants/al-khobar/al-jisr
API_URL_BASE = f"https://api.scrape.do/?token={TOKEN}&geoCode=sa&super=true&url="

restaurants = []
page = 1

# Loop through all paginated result pages
while True:
    url = f"{BASE_URL}?page={page}"
    api_url = API_URL_BASE + url
    response = requests.get(api_url)
    soup = BeautifulSoup(response.text, "html.parser")
    found = False
    # For each <li> that contains a restaurant listing
    for li in soup.select("ul > li"):
        name_tag = li.find("h1", class_="text-base text-typography font-medium")
        if not name_tag:
            continue
        found = True
        a = li.find("a", href=True)
        store_link = "https://hungerstation.com" + a["href"] if a else ""
        store_name = name_tag.get_text(strip=True)
        category_tag = li.find("p")
        category = category_tag.get_text(strip=True) if category_tag else ""
        rating_tag = li.find("span")
        review_rating = rating_tag.get_text(strip=True) if rating_tag else ""
        restaurants.append({
            "store_link": store_link,
            "store_name": store_name,
            "category": category,
            "review_rating": review_rating
        })
    # Stop if no more restaurant listings are found
    if not found:
        break
    print(f"Extracted page {page}")
    page += 1

# Write all restaurant listings to CSV
with open("hungerstation_restaurants.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["store_link", "store_name", "category", "review_rating"])
    writer.writeheader()
    writer.writerows(restaurants)

print(f"Extracted {len(restaurants)} restaurants to hungerstation_restaurants.csv")