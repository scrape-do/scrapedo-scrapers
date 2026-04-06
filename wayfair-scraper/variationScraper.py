import json
import sys
import time
import urllib.parse
import requests
from bs4 import BeautifulSoup
import re

TOKEN = "<your-token>"
TARGET_URL = "https://www.wayfair.com/decor-pillows/pdp/winston-porter-sevan-solid-thermal-grommet-curtain-panels-wnpo9085.html"
MAX_COLORS = 2  # set to None for a full run

def fetch_with_retry(url, max_retries=2):
    """Fetch with retry logic for Scrape.do API requests."""
    for attempt in range(max_retries):
        try:
            api_url = f"http://api.scrape.do/?token={TOKEN}&url={urllib.parse.quote(url)}&super=true&render=true"
            t0 = time.time()
            response = requests.get(api_url, timeout=(10, 45))
            elapsed = time.time() - t0
            if response.status_code == 200:
                print(f"  -> OK ({elapsed:.1f}s)", flush=True)
                return response.text
            else:
                print(f"  -> HTTP {response.status_code} on attempt {attempt + 1}", flush=True)
        except requests.exceptions.Timeout:
            print(f"  -> Timeout on attempt {attempt + 1}", flush=True)
        except Exception as e:
            print(f"  -> Error on attempt {attempt + 1}: {e}", flush=True)
    return None

print("Fetching base page...", flush=True)
html_text = fetch_with_retry(TARGET_URL)
if not html_text:
    raise SystemExit("Failed to fetch base page")
soup = BeautifulSoup(html_text, "html.parser")

options_map = {}
for script in soup.find_all("script"):
    if script.string and "variantChoices" in script.string:
        pattern = r'\\?"displayId\\?":\s*(\d+).*?\\?"name\\?":\s*\\?"((?:\\\\\\"|[^"\\])+)\\?"'
        matches = re.findall(pattern, script.string)
        for disp_id, name in matches:
            clean_name = name.replace('\\\\\\"', '"').replace('\\"', '"')
            if disp_id not in options_map:
                options_map[disp_id] = clean_name

colors = {}
selectable_components = soup.find_all(attrs={"data-test-id": "pdp-ch-selectableComponent"})
for comp in selectable_components:
    option_id = comp.get("data-optionid-id")
    img = comp.find("img")
    if option_id and img:
        alt_text = img.get("alt", "")
        clean_name = alt_text.replace(" selected", "").replace(" is unavailable", "").replace(" is out of stock", "").strip()
        if option_id not in colors:
            colors[option_id] = clean_name

base_url = TARGET_URL.split("?")[0]
all_variations = []

color_items = sorted(colors.items())
if MAX_COLORS:
    color_items = color_items[:MAX_COLORS]

print(f"Found {len(colors)} colors total. Processing {len(color_items)}...", flush=True)

for color_id, color_name in color_items:
    print(f"\nProcessing color: {color_name} (id={color_id})...", flush=True)

    color_url = f"{base_url}?piid={color_id}"
    html_text = fetch_with_retry(color_url)
    if not html_text:
        print(f"  Skipping {color_name} — fetch failed", flush=True)
        continue

    size_piids = set()
    piid_refs = re.findall(r'piid=([^\"& \']+)', html_text)
    for p in piid_refs:
        decoded = urllib.parse.unquote(p).strip('\\')
        if "," in decoded:
            parts = decoded.split(",")
            if len(parts) == 2:
                size_piids.add(parts[1] if parts[0] == color_id else parts[0])

    print(f"  Found {len(size_piids)} sizes", flush=True)

    for size_id in sorted(size_piids):
        size_name = options_map.get(size_id, "Standard")
        if size_name == "Curtain Color":
            continue

        piid_combo = f"{color_id},{size_id}"
        var_url = f"{base_url}?piid={piid_combo}"
        print(f"  Fetching {color_name} / {size_name}...", end=" ", flush=True)
        var_html = fetch_with_retry(var_url)
        if not var_html:
            continue
        var_soup = BeautifulSoup(var_html, "html.parser")

        price_elem = var_soup.find(attrs={"data-test-id": "PriceDisplay"})
        price = price_elem.get_text(strip=True).replace("$", "").replace(",", "") if price_elem else None

        stock_status = "out_of_stock" if "out of stock" in var_html.lower() else "in_stock"

        all_variations.append({
            "color": color_name,
            "size": size_name,
            "price": price,
            "stock_status": stock_status,
            "piid": piid_combo,
            "url": var_url
        })

with open("wayfair_variations.json", "w", encoding="utf-8") as f:
    json.dump(all_variations, f, indent=2, ensure_ascii=False)

print(f"\nScraping completed. Saved {len(all_variations)} variations to wayfair_variations.json")
