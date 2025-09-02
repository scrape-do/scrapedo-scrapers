# Walmart Scraper

This folder provides Python scripts to extract product data, variants, categories, and track price changes from Walmart using [Scrape.do](https://scrape.do) to bypass Walmart's dual-firewall protection (Akamai + PerimeterX) and handle store-specific pricing with JavaScript rendering.

The tools here let you:
- Scrape individual product details from Walmart product pages with store-specific pricing
- Extract all product variations (sizes, colors, packs) from multi-variant products
- Scrape category pages with automatic pagination and duplicate filtering
- Track stock availability and price changes over time with automated alerts
- Save results to CSV for easy analysis

[Get full technical tutorial here 📕](https://scrape.do/blog/walmart-scraping/)

All scripts use Python 3.7+, the `requests` library, and `BeautifulSoup` for HTML parsing.

---

## What's Included

### 1. `singleProductScraper.py`
**Scrapes individual product details from a specific Walmart product page.**

- Uses Scrape.do's Walmart plugin to automatically handle store selection and session management
- Extracts product name, brand, price, stock availability, discounts, and product details
- Handles both AI-generated and traditional product descriptions
- Configured for Secaucus Supercenter (Store ID: 3520, Zip: 07094) by default
- Example usage:
  ```bash
  python singleProductScraper.py
  ```

### 2. `variantProductScraper.py`
**Extracts all product variations from Walmart products with multiple options.**

- Automatically discovers all variant URLs from the main product page
- Scrapes each variant individually to capture size/color/pack-specific pricing
- Handles stock availability and discounts for each variation
- Removes duplicate variants and exports comprehensive data
- Saves results to `variant_products.csv`
- Example usage:
  ```bash
  python variantProductScraper.py
  # Output: variant_products.csv
  ```

### 3. `categoryScraper.py`
**Scrapes Walmart category pages with automatic pagination and duplicate filtering.**

- Uses proper referer headers to avoid bot detection during pagination
- Extracts product tiles with name, price, image, rating, and review count
- Automatically handles pagination through multiple result pages
- Removes duplicate products across pages using image URLs as unique identifiers
- Saves results to `walmart_category.csv`
- Example usage:
  ```bash
  python categoryScraper.py
  # Output: walmart_category.csv
  ```

### 4. `priceTracker.py`
**Tracks stock availability and price changes across multiple categories over time.**

- Monitors multiple Walmart categories for price and stock changes
- Saves JSON snapshots for historical comparison between runs
- Generates CSV exports with the latest product data
- Prints console alerts when products change price or stock status
- Supports tracking multiple categories simultaneously
- Example usage:
  ```bash
  python priceTracker.py
  # Output: category_snapshot.json, category_latest.csv, console alerts
  ```

---

## Requirements

- Python 3.7+
- `requests`, `beautifulsoup4` libraries
  ```bash
  pip install requests beautifulsoup4
  ```
- A [Scrape.do API token](https://dashboard.scrape.do/signup) (free 1000 credits/month)

---

## Setup & Step-by-Step Usage

### Finding Your Store ID

To use the Walmart plugin, you need two pieces of information: your zip code (easy) and the store ID (requires a quick lookup).

Here's how to find the store ID:

1. Visit Walmart.com and click the "Pickup or delivery?" dropdown
2. Enter your zip code and select your preferred store
3. Click on "Store details" for your selected store
4. This takes you to a URL like `https://www.walmart.com/store/3520-secaucus-nj`
5. The store ID is the number at the beginning: `3520`

For our examples, we use the Secaucus Supercenter (Store ID: 3520, Zip: 07094).

### Configuration Steps

1. **Register for a Scrape.do API token** and replace `<your-token>` in all scripts.

2. **Configure store location (optional):**
   - All scripts are pre-configured for Secaucus Supercenter (Store ID: 3520, Zip: 07094)
   - To change store: Update `ZIPCODE` and `STORE_ID` variables in the scripts

3. **Configure target URLs as needed:**
   - For `singleProductScraper.py`: Set the `target_url` variable to any Walmart product page
   - For `variantProductScraper.py`: Set the `target_url` variable to a product with variants
   - For `categoryScraper.py`: Set the `target_url` variable to any Walmart category page
   - For `priceTracker.py`: Update the `CATEGORY_URLS` list with categories you want to monitor

4. **Run the desired script:**
   ```bash
   python singleProductScraper.py     # Individual product details
   python variantProductScraper.py    # All product variations
   python categoryScraper.py          # Category pages with pagination
   python priceTracker.py             # Price and stock monitoring
   ```

5. **Check the output CSV files and console output for your results.**

---

## Technical Details

### Store Selection & Session Management
All scripts use Scrape.do's Walmart plugin which automatically handles:
- Store selection with `zipcode` and `storeid` parameters
- Session cookie management (`ACID`, `locDataV3`, `locGuestData`)
- TLS fingerprinting to bypass Akamai protection
- CAPTCHA challenges from PerimeterX (HUMAN)

### Pagination & Anti-Bot Evasion
`categoryScraper.py` and `priceTracker.py` implement:
- **Referer headers**: Each page request includes the previous page URL as referer
- **Realistic delays**: Built-in delays between requests to avoid rate limiting
- **JavaScript rendering**: Full page rendering to load dynamic product tiles

### Data Extraction Methods
- **Product details**: Uses `itemprop="name"` and `data-seo-id` attributes for reliable extraction
- **Price handling**: Supports both regular prices and "Now $X.XX" discount formats
- **Stock detection**: Identifies availability through "Add to Cart" button presence
- **Variant discovery**: Extracts variant links from `div#item-page-variant-group-bg-div`

---

## Configuration Examples

### Monitor Different Categories
```python
# In priceTracker.py
CATEGORY_URLS = [
    "https://www.walmart.com/browse/food/snacks/976759_976787",
    "https://www.walmart.com/browse/electronics/tv-video/3944_77622",
    "https://www.walmart.com/browse/clothing/mens-clothing/5438_133197"
]
```

### Change Store Location
```python
# In any script
ZIPCODE = "90210"  # Beverly Hills
STORE_ID = "2027"  # Find your store ID from walmart.com store details
```

### Scrape Different Products
```python
# In singleProductScraper.py or variantProductScraper.py
target_url = "https://www.walmart.com/ip/Apple-iPhone-15-128GB-Blue/5031006091"
target_url = "https://www.walmart.com/ip/Great-Value-Whole-Milk-Gallon/10450114"
```

---

## Troubleshooting & Tips

- **403 or 429 errors:**
  - Make sure your Scrape.do token is valid and you have credits left
  - Double-check your target URLs are accessible and valid Walmart pages

- **Missing price or stock data:**
  - Ensure you've selected a valid store location (zipcode and storeid)
  - Some products may not be available in your selected store location

- **Empty variant data:**
  - Not all products have variants - check that the product page shows size/color options
  - Some products may use different HTML structures for variants

- **Pagination issues:**
  - Category pages may have different layouts - the script handles common structures
  - Very large categories may take time to scrape completely

---

## Legal & Ethical Notes

- Only scrape publicly accessible data and respect Walmart's terms of service
- Do not automate excessive requests or use scraped data for commercial purposes without permission
- Scrape.do handles proxies, headers, and anti-bot solutions for you, but always use scraping responsibly

---

## Why Use Scrape.do?

- Rotating premium proxies & geo-targeting
- Built-in header spoofing and TLS fingerprinting
- Handles Akamai firewalls and PerimeterX CAPTCHAs automatically
- JavaScript rendering for dynamic content
- Walmart-specific plugin for store selection
- 1000 free credits/month

[Get your free API token here](https://dashboard.scrape.do/signup)