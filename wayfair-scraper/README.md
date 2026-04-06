# Wayfair Scraper

This folder provides Python scripts to extract product data, category listings, and product variations from Wayfair using [Scrape.do](https://scrape.do) to bypass Wayfair's PerimeterX bot protection with residential proxies and JavaScript rendering.

The tools here let you:
- Scrape individual product pages for name, price, discount, reviews, description, and images
- Extract paginated category listings with deduplication and full product metadata
- Map all color and size variations of a product with per-variation pricing and stock status
- Save results to JSON for easy downstream processing

[Get full technical tutorial here 📕](https://scrape.do/blog/wayfair-scraping/)

All scripts use Python 3.7+, the `requests` library, and `BeautifulSoup` for HTML parsing.

---

## What's Included

### 1. `singleScraper.py`
**Scrapes a single Wayfair product detail page.**

- Extracts product name, SKU, seller/brand, price, original price, discount rate, review rating, review count, description, and up to 10 product images
- Uses `super=true&render=true` to bypass PerimeterX and execute JavaScript
- Prints all fields to the terminal
- Example usage:
  ```bash
  python singleScraper.py
  ```

### 2. `categoryScraper.py`
**Scrapes a Wayfair category page with automatic pagination.**

- Iterates pages via `?curpage=N` query parameter
- Extracts product name, seller, price, original price, discount rate, review rating, review count, image, and product link from each listing card
- Deduplicates results by product URL across pages
- Adds a 1-second delay between pages to avoid rate limiting
- Saves results to `wayfair_category.json`
- Example usage:
  ```bash
  python categoryScraper.py
  # Output: wayfair_category.json
  ```

### 3. `variationScraper.py`
**Maps all color and size variations of a Wayfair product with per-variation pricing and stock status.**

- Includes `fetch_with_retry()` helper with 3 retries for reliability
- Extracts color options from `[data-test-id="pdp-ch-selectableComponent"]` elements
- Builds an options map by regex-parsing `variantChoices` JSON embedded in script tags
- Visits each color URL (`?piid={color_id}`) to discover associated size piids
- Visits each color+size combination URL to extract price and stock status
- Saves all variations to `wayfair_variations.json`
- Example usage:
  ```bash
  python variationScraper.py
  # Output: wayfair_variations.json
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

## Setup & Configuration

1. **Register for a Scrape.do API token** and replace `<your-token>` in all scripts.

2. **Configure your target URL:**
   - For `singleScraper.py`: Set `TARGET_URL` to any Wayfair product page
   - For `categoryScraper.py`: Set `BASE_URL` to any Wayfair category page, and `MAX_PAGES` to control pagination depth
   - For `variationScraper.py`: Set `TARGET_URL` to a Wayfair product page with multiple color/size options

3. **Run the desired script:**
   ```bash
   python singleScraper.py      # Single product details
   python categoryScraper.py    # Category pages with pagination
   python variationScraper.py   # Full variation map with pricing
   ```

---

## Technical Details

### Anti-Bot Bypass
All scripts use `super=true&render=true` (25 credits per request) to handle Wayfair's dual protection:
- `super=true`: Routes through residential proxies to bypass IP-based blocks
- `render=true`: Executes JavaScript so PerimeterX challenge pages are resolved before returning HTML

```python
api_url = f"http://api.scrape.do/?token={TOKEN}&url={urllib.parse.quote(target_url)}&super=true&render=true"
```

### Variation Discovery
`variationScraper.py` uses a two-pass approach:
1. Parses `variantChoices` JSON embedded in script tags to build an `options_map` of `displayId → name`
2. Extracts color piids from the DOM, then visits each color URL to discover size piids from `piid=X,Y` patterns in the HTML

### Pagination
`categoryScraper.py` appends `?curpage=N` for pages 2 and beyond; page 1 uses the base URL without parameters.

---

## Legal & Ethical Notes

- Only scrape publicly accessible data and respect Wayfair's terms of service
- Do not automate excessive requests that may disrupt the service
- Scrape.do handles proxies, headers, and anti-bot solutions for you, but always use scraping responsibly
