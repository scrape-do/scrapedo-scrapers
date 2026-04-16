# Scrape DigiKey category listings via Scrape.do and export to CSV.
# Pagination uses ?s= with an LZ-String compressed JSON cursor (not ?page=).

import csv
import json
import re
import time
import urllib.parse

import requests
from bs4 import BeautifulSoup
from lzstring import LZString

TOKEN = "<your_token>"
CATEGORY_URL = "https://www.digikey.com/en/products/filter/fiber-optic-cables/471"
LISTING_PAGE_SIZE = 25
FILTER_STATE_KEY = "5"
MAX_LISTING_PAGES = 5


def encode_cursor(page_num):
    # LZ-String compressed JSON cursor for DigiKey's ?s= parameter
    payload = json.dumps({FILTER_STATE_KEY: {"p": page_num, "pp": LISTING_PAGE_SIZE}}, separators=(",", ":"))
    return LZString.compressToEncodedURIComponent(payload)


def normalize_stock(raw):
    # DigiKey mixes "In Stock" and "Marketplace" in the same cell with lead-time text
    if not raw:
        return ""
    text = re.sub(r"\s+", " ", raw.strip())
    text = re.sub(r"(?i)\s*check\s+lead\s*time\s*", "", text).strip()

    dk = mp = None
    for m in re.finditer(r"([\d,]+)\s+(In Stock|Marketplace)\b", text, re.IGNORECASE):
        qty = m.group(1).replace(",", "")
        if m.group(2).lower() == "in stock":
            dk = qty
        else:
            mp = qty

    if dk and mp:
        return f"DK:{dk}, MP:{mp}"
    return dk or (f"MP:{mp}" if mp else text)


# Strip query params from category URL; we attach our own ?s= cursor
parsed = urllib.parse.urlparse(CATEGORY_URL)
category_base = urllib.parse.urlunparse((parsed.scheme, parsed.netloc, parsed.path, "", "", ""))

all_rows = []
prev_signature = None

for page_num in range(1, MAX_LISTING_PAGES + 1):
    cursor = encode_cursor(page_num)
    page_url = f"{category_base}?s={urllib.parse.quote(cursor, safe='')}"
    print(f"Scraping page {page_num}/{MAX_LISTING_PAGES}...")

    api_url = f"http://api.scrape.do/?token={TOKEN}&url={urllib.parse.quote(page_url)}&super=true"
    r = requests.get(api_url, timeout=120)
    if r.status_code != 200:
        print(f"  HTTP {r.status_code}")
        break

    soup = BeautifulSoup(r.text, "html.parser")
    table = soup.select_one('table:has(td[data-testid="draggable-cell--100"])')
    if not table:
        print("  No product table found.")
        break

    page_rows = []
    for tr in table.select("tbody tr"):
        part_cell = tr.select_one('td[data-testid="draggable-cell--100"]')
        if not part_cell:
            continue
        link = part_cell.select_one('a[href*="/en/products/detail/"]')
        if not link or not link.get("href"):
            continue

        href = urllib.parse.urljoin("https://www.digikey.com", link["href"])
        serial = link.get_text(strip=True)
        name = part_cell.get_text(" ", strip=True)
        if serial and name.startswith(serial):
            name = name[len(serial):].strip()

        stock_cell = tr.select_one('td[data-testid="draggable-cell--102"]')
        stock = normalize_stock(stock_cell.get_text(" ", strip=True) if stock_cell else "")

        price_cell = tr.select_one('td[data-testid="draggable-cell--101"]')
        price_raw = price_cell.get_text(" ", strip=True) if price_cell else ""
        dollar = re.search(r"\$[\d,.]+", price_raw)
        price = dollar.group(0) if dollar else price_raw

        pkg_cell = tr.select_one('td[data-testid="draggable-cell--5"]')
        status_cell = tr.select_one('td[data-testid="draggable-cell-1989"]')

        page_rows.append({
            "name": name,
            "serial_number": serial,
            "stock": stock,
            "price": price,
            "package_type": pkg_cell.get_text(" ", strip=True) if pkg_cell else "",
            "product_status": status_cell.get_text(" ", strip=True) if status_cell else "",
            "product_url": href,
        })

    if not page_rows:
        break

    # DigiKey serves page 1 again when the cursor overflows
    sig = tuple(r["serial_number"] + "|" + r["product_url"] for r in page_rows[:5])
    if sig == prev_signature:
        print("  Duplicate page detected, stopping.")
        break
    prev_signature = sig

    all_rows.extend(page_rows)
    print(f"  {len(page_rows)} rows")
    time.sleep(1)


out_path = "digikey-category.csv"
with open(out_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["name", "serial_number", "stock", "price", "package_type", "product_status", "product_url"])
    writer.writeheader()
    writer.writerows(all_rows)

print(f"Saved {len(all_rows)} rows to {out_path}")
