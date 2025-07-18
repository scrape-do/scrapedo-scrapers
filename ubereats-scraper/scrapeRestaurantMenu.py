import requests
import urllib.parse
import json
from bs4 import BeautifulSoup
import csv

# --- Scrape.do token and Uber Eats restaurant URL ---
scrape_token = "<your-token>"
ubereats_restaurant_url = "<store-url>" # e.g. https://www.ubereats.com/store/popeyes-east-harlem/H6RO8zvyQ1CxgJ7VH350pA?diningMode=DELIVERY&ps=1&surfaceName=

# --- Prepare Scrape.do API URL (with custom wait for JS rendering) ---
api_url = (
    f"https://api.scrape.do/?url={urllib.parse.quote_plus(ubereats_restaurant_url)}"
    f"&token={scrape_token}"
    f"&super=true"
    f"&render=true"
    f"&customWait=5000"
)

# --- Fetch the rendered Uber Eats restaurant page ---
response = requests.get(api_url)

# --- Save raw HTML for debugging/inspection ---
with open('ubereats_restaurant_raw.html', 'w', encoding='utf-8') as f:
    f.write(response.text)

# --- Parse the HTML with BeautifulSoup ---
with open('ubereats_restaurant_raw.html', 'r', encoding='utf-8') as f:
    html = f.read()
soup = BeautifulSoup(html, "html.parser")

# --- Extract menu items: category, name, price ---
results = []
for section in soup.find_all('div', {'data-testid': 'store-catalog-section-vertical-grid'}):
    cat_h3 = section.find('h3')
    category = cat_h3.get_text(strip=True) if cat_h3 else ''
    for item in section.find_all('li', {'data-testid': True}):
        if not item['data-testid'].startswith('store-item-'):
            continue
        rich_texts = item.find_all('span', {'data-testid': 'rich-text'})
        if len(rich_texts) < 2:
            continue
        name = rich_texts[0].get_text(strip=True)
        price = rich_texts[1].get_text(strip=True)
        results.append({
            'category': category,
            'name': name,
            'price': price
        })

# --- Write results to CSV ---
with open('ubereats_restaurant_menu.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['category', 'name', 'price']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for row in results:
        writer.writerow(row)
print(f"Wrote {len(results)} menu items to ubereats_restaurant_menu.csv")
