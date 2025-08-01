# eBay Scraper

This folder provides a set of Python scripts to extract product listings, reviews, and variant data from eBay using [Scrape.do](https://scrape.do) to bypass anti-bot protection and handle JavaScript rendering.

The tools here let you:
- Scrape individual product details from eBay product pages
- Extract all reviews from product review pages with pagination
- Scrape search results with support for multiple eBay layout structures
- Extract variant data (size, color, etc.) from product pages with hidden JavaScript data
- Save results to CSV for easy analysis

[Find extended technical guide here. 📘](https://scrape.do/blog/ebay-scraping/)

All scripts use Python 3, the `requests` library, and `BeautifulSoup` for HTML parsing.

---

## What's Included

### 1. `basicListing.py`
**Scrapes individual product details from a specific eBay product page.**

- Uses Scrape.do to render the product page and extract key information.
- Extracts product title, price, and main product image.
- Requires you to set the `target_url` and `product_id` variables at the top of the script.
- Saves the results to `ebay_product.csv`.
- Example usage:
  ```bash
  python basicListing.py
  # Output: ebay_product.csv
  ```

### 2. `productReviews.py`
**Scrapes all product reviews from eBay review pages with automatic pagination.**

- Uses Scrape.do to render review pages and handle pagination automatically.
- Extracts reviewer name, rating, review title, date, and comment text.
- Automatically follows "next page" links until all reviews are collected.
- Saves the results to `ebay_paginated_reviews.csv`.
- Example usage:
  ```bash
  python productReviews.py
  # Output: ebay_paginated_reviews.csv
  ```

### 3. `searchResults.py`
**Scrapes eBay search results with support for multiple HTML layout structures.**

- **Handles two different eBay layouts automatically:**
  - `s-card` layout: Modern card-based layout
  - `s-item` layout: Traditional list-based layout
- Uses Scrape.do to render pages and handle JavaScript lazy-loading.
- Extracts product title, price, image URL, and product link.
- Automatically follows pagination to collect all search results.
- Saves the results to `ebay_search_results.csv`.
- Example usage:
  ```bash
  python searchResults.py
  # Output: ebay_search_results.csv
  ```

### 4. `variantListing.py`
**Extracts variant data (size, color, etc.) from eBay product pages using hidden JavaScript data.**

- Uses Scrape.do to render the product page and extract hidden MSKU (Merchant SKU) data.
- **Extracts variant information from embedded JavaScript:**
  - Product variations (size, color, style, etc.)
  - Price for each variant combination
  - Stock status for each variant
  - Dynamic menu structures
- Parses complex nested JSON structures to extract all possible variant combinations.
- Saves the results to `product_data.csv` with dynamic headers based on available variants.
- Example usage:
  ```bash
  python variantListing.py
  # Output: product_data.csv
  ```

---

## Requirements

- Python 3.7+
- `requests` and `beautifulsoup4` libraries
  ```bash
  pip install requests beautifulsoup4
  ```
- A [Scrape.do API token](https://dashboard.scrape.do/signup) (free 1000 credits/month)

---

## Setup & Step-by-Step Usage

1. **Register for a Scrape.do API token** and replace `<your-token>` in all scripts.
2. **Configure target URLs as needed:**
   - For `basicListing.py`, set the `target_url` and `product_id` variables at the top.
   - For `productReviews.py`, set the `start_url` variable to the first review page URL.
   - For `searchResults.py`, set the `current_url` variable to your eBay search URL.
   - For `variantListing.py`, set the `TARGET_URL` variable to the product page URL.
3. **Run the desired script:**
   - `python basicListing.py` to get individual product details.
   - `python productReviews.py` to get all product reviews.
   - `python searchResults.py` to get all search results.
   - `python variantListing.py` to get all product variants.
4. **Check the output CSV files for your results.**

---

## Technical Details

### Search Results Layout Detection
`searchResults.py` automatically detects which eBay layout is being used:
- **s-card layout**: Modern card-based design with `.s-card` selectors
- **s-item layout**: Traditional list design with `.s-item` selectors

The script adapts its selectors accordingly to extract data from either layout structure.

### Variant Data Extraction
`variantListing.py` extracts hidden JavaScript data containing:
- **variationsMap**: Maps variation combinations to data
- **menuItemMap**: Contains individual menu item values
- **variationCombinations**: All possible variant combinations
- **selectMenus**: Dynamic menu structures (size, color, etc.)

This allows extraction of complete variant information that isn't visible in the rendered HTML.

---

## Troubleshooting & Tips

- **403 or 429 errors:**  
  - Make sure your Scrape.do token is valid and you have credits left.
  - Double-check your target URLs are accessible.
- **Empty or missing fields:**  
  - Ensure the eBay pages you're scraping are public and available.
  - Some products may not have reviews or variants.
- **Layout detection issues:**  
  - If `searchResults.py` doesn't find items, eBay may have changed their HTML structure.
  - Check the rendered HTML to see which selectors are being used.

---

## Legal & Ethical Notes

- Only scrape publicly accessible data and respect eBay's terms of service.
- Do not automate excessive requests or use scraped data for commercial purposes without permission.
- Scrape.do handles proxies, headers, and anti-bot solutions for you, but always use scraping responsibly.

---

## Why Use Scrape.do?

- Rotating premium proxies & geo-targeting
- Built-in header spoofing
- Handles redirects, CAPTCHAs, and JavaScript rendering
- 1000 free credits/month

[Get your free API token here](https://dashboard.scrape.do/signup) 