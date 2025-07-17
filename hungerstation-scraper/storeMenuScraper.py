import requests
from bs4 import BeautifulSoup
import csv

# Scrape.do API token and store page URL
TOKEN = "<your-token>"
STORE_URL = "<store-url>"# e.g. https://hungerstation.com/sa-en/restaurant/al-khobar/al-jisr/13699
API_URL = f"https://api.scrape.do/?token={TOKEN}&url={STORE_URL}&geoCode=sa&super=true"

# Fetch the store menu page HTML
response = requests.get(API_URL)
soup = BeautifulSoup(response.text, "html.parser")

menu_items = []

# Loop through all menu categories (sections)
for section in soup.find_all("section", attrs={"data-role": "item-category"}):
    category = section.get("id") or ""
    # For each menu item in the category (button.card.p-6.menu-item)
    for item in section.find_all("button", class_="card p-6 menu-item"):
        # Extract the menu item name
        name_tag = item.find("h2", class_="menu-item-title")
        name = name_tag.get_text(strip=True) if name_tag else ""
        # Extract the menu item description
        desc_tag = item.find("p", class_="menu-item-description")
        description = desc_tag.get_text(strip=True) if desc_tag else ""
        # Extract the menu item price
        price_tag = item.find("p", class_="text-greenBadge text-base mx-2")
        price = price_tag.get_text(strip=True) if price_tag else ""
        # Extract the menu item calories
        cal_tag = item.find("p", class_="text-secondary text-base mx-2")
        calories = cal_tag.get_text(strip=True) if cal_tag else ""
        # Only add if name exists
        if name:
            menu_items.append({
                "Category": category,
                "Name": name,
                "Description": description,
                "Price": price,
                "Calories": calories
            })

# Write all menu items to CSV
with open("hungerstation_menu_items.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["Category", "Name", "Description", "Price", "Calories"])
    writer.writeheader()
    writer.writerows(menu_items)

print(f"Extracted {len(menu_items)} menu items to hungerstation_menu_items.csv")
