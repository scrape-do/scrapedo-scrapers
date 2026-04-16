# Scrape a DigiKey product page via Scrape.do and export to JSON.
# Fields come from stable data-testid selectors; attributes are dynamic per product category.

import json
import urllib.parse

import requests
from bs4 import BeautifulSoup

TOKEN = "<your_token>"
PRODUCT_URL = "https://www.digikey.com/en/products/detail/industrial-fiber-optics/GH4001/1855656"
OUTPUT_JSON = "digikey-product.json"


def get_text(el, prefix=""):
    # Extract text from element, stripping an optional label prefix
    if not el:
        return ""
    text = el.get_text(" ", strip=True)
    return text.removeprefix(prefix).strip() if prefix else text


# Fetch product page
api_url = f"http://api.scrape.do/?token={TOKEN}&url={urllib.parse.quote(PRODUCT_URL)}&super=true"
response = requests.get(api_url, timeout=120)
if response.status_code != 200:
    raise SystemExit(f"HTTP {response.status_code}")

soup = BeautifulSoup(response.text, "html.parser")

# Core fields from data-testid selectors
mpn = get_text(soup.select_one('[data-testid="mfr-number"]'))
manufacturer = get_text(soup.select_one('[data-testid="overview-manufacturer"]'), "Manufacturer")
detailed_desc = get_text(soup.select_one('[data-testid="detailed-description"]'), "Detailed Description")
qty_available = get_text(soup.select_one('[data-testid="title-messages"]'), "In-Stock:")

# Datasheet link
ds_el = soup.select_one('[data-testid="datasheet-download"]')
datasheet_url = urllib.parse.urljoin(PRODUCT_URL, ds_el["href"]) if ds_el and ds_el.get("href") else ""

# Pricing tiers
pricing_tiers = []
for tr in soup.select('[data-testid="pricing-table-container"] tr'):
    cells = [c.get_text(strip=True) for c in tr.find_all(["td", "th"])]
    if len(cells) < 3 or cells[0].lower() == "quantity":
        continue
    pricing_tiers.append({"break_qty": cells[0], "unit_price": cells[1], "ext_price": cells[2]})

# Dynamic attributes (vary by product category)
attributes = {}
for tr in soup.select('[data-testid="product-attributes"] tr')[1:]:
    cells = [c.get_text(strip=True) for c in tr.find_all(["td", "th"])]
    if len(cells) < 2 or not cells[0] or not cells[1]:
        continue
    if cells[1] in ("-", "n/a", "N/A"):
        continue
    if cells[0] == "Manufacturer" and cells[1] == manufacturer:
        continue
    attributes[cells[0]] = cells[1]

product = {
    "url": PRODUCT_URL,
    "mpn": mpn,
    "manufacturer": manufacturer,
    "detailed_description": detailed_desc,
    "qty_available": qty_available,
    "datasheet_url": datasheet_url,
    "pricing_tiers": pricing_tiers,
    "attributes": attributes,
}

with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(product, f, indent=2, ensure_ascii=False)

print(f"Saved {OUTPUT_JSON} ({len(attributes)} attribute keys)")
