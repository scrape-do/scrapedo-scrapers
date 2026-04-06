import requests
from bs4 import BeautifulSoup
import urllib.parse
import csv
import re

TOKEN = "<your-token>"
BASE_URL = "https://www.rightmove.co.uk/property-for-sale/find.html"
RESULTS_PER_PAGE = 24
TOTAL_PAGES = 5  # set to 42 for full scrape

params = {
    "searchLocation": "Central+London",
    "useLocationIdentifier": "true",
    "locationIdentifier": "REGION^92824",
    "sortType": "2",
    "channel": "BUY",
    "transactionType": "BUY",
}

all_listings = []
seen_urls = set()

for page in range(TOTAL_PAGES):
    index = page * RESULTS_PER_PAGE
    page_params = {**params, "index": str(index)}
    target_url = f"{BASE_URL}?{urllib.parse.urlencode(page_params)}"
    encoded_url = urllib.parse.quote(target_url, safe="")
    api_url = f"http://api.scrape.do/?token={TOKEN}&url={encoded_url}"

    response = requests.get(api_url)
    if response.status_code != 200:
        print(f"Page {page + 1}: failed with status {response.status_code}")
        continue

    soup = BeautifulSoup(response.text, "html.parser")
    cards = soup.select("[data-testid^='propertyCard-']")
    page_count = 0

    for card in cards:
        link_el = card.select_one("a[href*='properties']")
        if not link_el:
            continue

        prop_url = f"https://www.rightmove.co.uk{link_el['href']}"
        if prop_url in seen_urls:
            continue
        seen_urls.add(prop_url)

        address_el = card.select_one("address")
        price_el = card.select_one("[class*='Price']")
        type_el = card.select_one("[class*='propertyType']")
        beds_el = card.select_one("[class*='edroom']")

        agent_text = ""
        for span in card.select("span"):
            text = span.get_text(strip=True)
            if " by " in text:
                match = re.search(r"by (.+)", text)
                if match:
                    agent_text = match.group(1)
                    agent_text = re.sub(r"(Added|Reduced) on \d{2}/\d{2}/\d{4}$", "", agent_text).strip()
                break

        phone_el = card.select_one("a[class*='phoneLinkDesktop']")
        phone_text = ""
        if phone_el:
            phone_text = phone_el.get_text(strip=True).replace("Local call rate", "").strip()

        price_text = price_el.get_text(strip=True) if price_el else ""
        price_text = re.sub(r"(FEATURED[A-Z\s\-]*|PREMIUM LISTING|Premium Listing|Guide Price|NEW HOME)", "", price_text).strip()

        listing = {
            "address": address_el.get_text(strip=True) if address_el else "",
            "price": price_text,
            "property_type": type_el.get_text(strip=True) if type_el else "",
            "bedrooms": beds_el.get_text(strip=True) if beds_el else "",
            "agent": agent_text,
            "phone": phone_text,
            "url": prop_url,
        }
        all_listings.append(listing)
        page_count += 1

    print(f"Page {page + 1}: scraped {page_count} unique listings")

with open("listings.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["address", "price", "property_type", "bedrooms", "agent", "phone", "url"])
    writer.writeheader()
    writer.writerows(all_listings)

print(f"\nTotal: {len(all_listings)} listings saved to listings.csv")
