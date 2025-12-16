import urllib.parse
import csv
import re
import requests
from bs4 import BeautifulSoup

# Configuration
token = "<SDO-token>"
asin = "B0CG84XR6N"  # Change this to any product ASIN with variations
geocode = "us"
zipcode = "10001"

# Build product URL from ASIN
target_url = f"https://www.amazon.com/dp/{asin}"

# Initial page scrape to find dimensions
targetUrl = urllib.parse.quote(target_url)
apiUrl = "https://api.scrape.do/plugin/amazon/?token={}&url={}&geocode={}&zipcode={}&output=html".format(token, targetUrl, geocode, zipcode)
response = requests.request("GET", apiUrl)

soup = BeautifulSoup(response.text, "html.parser")

# Extract available dimensions and options
dimensions = {}
for row in soup.find_all("div", {"id": re.compile(r"inline-twister-row-.*")}):
    dim_name = row.get("id", "").replace("inline-twister-row-", "").replace("_name", "")
    options = []
    for option in row.find_all("li", {"data-asin": True}):
        opt_asin = option.get("data-asin")
        if opt_asin and option.get("data-initiallyUnavailable") != "true":
            swatch = option.find("span", {"class": "swatch-title-text-display"})
            img = option.find("img")
            button = option.find("span", {"class": "a-button-text"})

            option_name = swatch.text.strip() if swatch else img.get("alt", "").strip() if img and img.get("alt") else button.get_text(strip=True) if button and button.get_text(strip=True) != "Select" else "Unknown"
            options.append({"name": option_name, "asin": opt_asin})

    if options:
        dimensions[dim_name] = options

print(f"Found dimensions: {list(dimensions.keys())}")
for dim_name, options in dimensions.items():
    print(f"  {dim_name}: {len(options)} options")

# Setup dimension traversal order and CSV headers
priority = ['color', 'size', 'style', 'pattern', 'material', 'fit']
dim_names = sorted(dimensions.keys(), key=lambda x: priority.index(x.lower()) if x.lower() in priority else len(priority))
headers = ["ASIN", "Product Name"] + dim_names + ["Price"]
results = []
scraped = set()

# Recursive function to scrape all product variations
def scrape_variations(variation_asin, dim_index=0, prefix=""):
    if variation_asin in scraped:
        return

    url = f"https://www.amazon.com/dp/{variation_asin}/?th=1&psc=1"
    targetUrl = urllib.parse.quote(url)
    apiUrl = "https://api.scrape.do/plugin/amazon/?token={}&url={}&geocode={}&zipcode={}&output=html".format(token, targetUrl, geocode, zipcode)
    response = requests.request("GET", apiUrl)

    soup = BeautifulSoup(response.text, "html.parser")

    title_elem = soup.find(id="productTitle")
    if not title_elem:
        print(f"{prefix}[SKIP] {variation_asin}: Product page not available")
        scraped.add(variation_asin)
        return
    name = title_elem.text.strip()

    try:
        price = "Out of Stock" if soup.find("div", id="outOfStockBuyBox_feature_div") else f"${soup.find(class_='a-price-whole').text}{soup.find(class_='a-price-fraction').text}"
    except:
        price = "N/A"

    page_dims = {}
    for row in soup.find_all("div", {"id": re.compile(r"inline-twister-row-.*")}):
        dim_name = row.get("id", "").replace("inline-twister-row-", "").replace("_name", "")
        options = []
        for option in row.find_all("li", {"data-asin": True}):
            opt_asin = option.get("data-asin")
            if opt_asin and option.get("data-initiallyUnavailable") != "true":
                swatch = option.find("span", {"class": "swatch-title-text-display"})
                img = option.find("img")
                button = option.find("span", {"class": "a-button-text"})

                option_name = swatch.text.strip() if swatch else img.get("alt", "").strip() if img and img.get("alt") else button.get_text(strip=True) if button and button.get_text(strip=True) != "Select" else "Unknown"
                options.append({"name": option_name, "asin": opt_asin})

        if options:
            page_dims[dim_name] = options

    # End of recursion - collect final data
    if dim_index >= len(dim_names) or not page_dims:
        scraped.add(variation_asin)
        selections = {}
        for dim_name in dim_names:
            for row_id in [f"inline-twister-row-{dim_name}_name", f"inline-twister-row-{dim_name}"]:
                row = soup.find("div", {"id": row_id})
                if row:
                    selected = row.find("span", {"class": re.compile(r".*a-button-selected.*")})
                    if selected:
                        swatch = selected.find("span", {"class": "swatch-title-text-display"})
                        img = selected.find("img")
                        selections[dim_name] = swatch.text.strip() if swatch else img.get("alt", "").strip() if img and img.get("alt") else selected.get_text(strip=True) if "Select" not in selected.get_text(strip=True) else "N/A"
                        break
                    else:
                        for option in row.find_all("li", {"data-asin": variation_asin}):
                            swatch = option.find("span", {"class": "swatch-title-text-display"})
                            button = option.find("span", {"class": "a-button-text"})
                            selections[dim_name] = swatch.text.strip() if swatch else button.get_text(strip=True) if button and "Select" not in button.get_text(strip=True) else "N/A"
                            break
                    break

        row = [variation_asin, name] + [selections.get(dim, "N/A") for dim in dim_names] + [price]
        results.append(row)

        sel_str = ", ".join([f"{k}:{v}" for k, v in selections.items()])
        print(f"{prefix}[OK] {variation_asin}: {price} | {sel_str}")
        return

    # Continue recursion through dimensions
    current_dim = dim_names[dim_index]
    if current_dim in page_dims:
        options = page_dims[current_dim]
        if dim_index == 0:
            print(f"{prefix}Found {len(options)} {current_dim} options")

        for i, option in enumerate(options):
            if dim_index == 0:
                print(f"{prefix}{current_dim} {i+1}/{len(options)}: {option['name']}")
            scrape_variations(option["asin"], dim_index + 1, prefix + "    ")
    else:
        scrape_variations(variation_asin, dim_index + 1, prefix)

# Start scraping process
print(f"\nDimension traversal order: {dim_names}")
print(f"\nStarting variation crawling...")

scrape_variations(asin)

# Export to CSV
csv_file = "productVariations.csv"

with open(csv_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    writer.writerows(results)

print(f"\nDone! Scraped {len(results)} unique variations")
print(f"Data exported to {csv_file}")
