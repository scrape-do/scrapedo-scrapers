import json
import re
import csv
import requests
import urllib.parse

# Configuration
TOKEN = "<your-token>"
TARGET_URL = "<product-url>"

# Scrape the page using scrape.do
response = requests.get(f"https://api.scrape.do/?url={urllib.parse.quote_plus(TARGET_URL)}&token={TOKEN}&super=true")
html_content = response.text

# Extract and parse MSKU data from HTML
msku_data = json.loads(re.search(r'"MSKU":({.+?}),"QUANTITY"', html_content).group(1))

# Get core data structures
variations = msku_data.get('variationsMap', {})
menu_items = msku_data.get('menuItemMap', {})
variation_combinations = msku_data.get('variationCombinations', {})

# Create CSV headers
headers = [menu['displayLabel'] for menu in msku_data.get('selectMenus', [])] + ['Price', 'OutOfStock']

# Process each variation combination
rows = []
for combo_key, combo_data_id in variation_combinations.items():
    variation_data = variations.get(str(combo_data_id))
    if not variation_data:
        continue

    row = {}
    menu_ids = [int(i) for i in combo_key.split('_')]

    # Extract menu values (size, color, etc.)
    for menu_id in menu_ids:
        menu_item = menu_items.get(str(menu_id))
        if menu_item:
            for menu in msku_data.get('selectMenus', []):
                if menu_item['valueId'] in menu['menuItemValueIds']:
                    row[menu['displayLabel']] = menu_item['displayName']
                    break

    # Extract price and stock status
    price_spans = variation_data.get('binModel', {}).get('price', {}).get('textSpans', [])
    row['Price'] = price_spans[0].get('text') if price_spans else None
    row['OutOfStock'] = variation_data.get('quantity', {}).get('outOfStock', False)

    rows.append(row)

# Write to CSV
with open('product_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=headers)
    writer.writeheader()
    writer.writerows(rows)

print("Written to product_data.csv")