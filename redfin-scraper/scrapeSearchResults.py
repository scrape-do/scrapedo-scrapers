import requests
import urllib.parse
from bs4 import BeautifulSoup
import csv

# Configuration
TOKEN = "<your_token>"
base_url = "https://www.redfin.com/city/30749/NY/New-York"
max_pages = 9 # max pages to scrape, 9 is the max number of pages for most cities

all_properties = []

for page in range(1, max_pages + 1):
    # Build URL for current page
    search_url = f"{base_url}/page-{page}"
    
    print(f"Scraping page {page}...")
    
    # Try to fetch page with retry logic
    for attempt in range(3):
        try:
            response = requests.get(f"https://api.scrape.do/?token={TOKEN}&url={urllib.parse.quote(search_url)}")
            soup = BeautifulSoup(response.text, "html.parser")
            break
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            continue
    
    # Find all home cards
    home_cards = soup.find_all("div", class_="bp-Homecard")
    
    if not home_cards:
        break
    
    page_properties = []
    
    for card in home_cards:
        # Skip empty cards - check if card has essential elements before parsing
        price_elem = card.find("span", class_="bp-Homecard__Price--value")
        address_elem = card.find("a", class_="bp-Homecard__Address")
        
        if not price_elem or not address_elem:
            continue
        
        property_data = {}
        
        # Price
        property_data['price'] = price_elem.get_text(strip=True)
        
        # Square feet
        sqft_elem = card.find("span", class_="bp-Homecard__LockedStat--value")
        property_data['square_feet'] = sqft_elem.get_text(strip=True) + " sq ft" if sqft_elem else ""
        
        # Address and URL
        property_data['full_address'] = address_elem.get_text(strip=True)
        property_data['url'] = "https://www.redfin.com" + address_elem.get("href", "")
        property_data['property_id'] = address_elem.get("href", "").split("/home/")[1]
        
        # Main image
        img_elem = card.find("img", class_="bp-Homecard__Photo--image")
        property_data['main_image'] = img_elem.get("src", "") if img_elem else ""
        
        # Broker
        broker_elem = card.find("div", class_="bp-Homecard__Attribution")
        broker_text = broker_elem.get_text(strip=True) if broker_elem else ""
        property_data['broker'] = broker_text.replace("Listing by ", "").replace("Listing by", "")
        
        page_properties.append(property_data)
    
    if not page_properties:
        break
    
    all_properties.extend(page_properties)
    print(f"Found {len(page_properties)} properties on page {page}")

# Remove duplicates based on property_id
seen_ids = set()
unique_properties = [prop for prop in all_properties if prop['property_id'] not in seen_ids and not seen_ids.add(prop['property_id'])]

# Save CSV
with open("redfin_search_results.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=unique_properties[0].keys())
    writer.writeheader()
    writer.writerows(unique_properties)

print(f"✓ {len(unique_properties)} unique properties saved to redfin_search_results.csv")