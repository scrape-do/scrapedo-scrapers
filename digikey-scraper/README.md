# DigiKey Scraper

This folder provides Python scripts to extract product listings and product detail data from DigiKey using [Scrape.do](https://scrape.do) with residential proxies to bypass bot detection.

The tools here let you:
- Scrape paginated category listings using DigiKey's LZ-String compressed cursor-based pagination
- Extract full product detail (MPN, manufacturer, pricing tiers, specs, datasheet) via stable `data-testid` selectors
- Save results to CSV and JSON for downstream use

[Get full technical tutorial here 📕](https://scrape.do/blog/digikey-scraping/)

All scripts use Python 3.8+, the `requests` and `beautifulsoup4` libraries, and the `lzstring` package for cursor encoding.

---

## What's Included

### 1. `scrapeDigikeyCategory.py`
**Scrapes paginated product listings from a DigiKey category page.**

- Encodes each page cursor as an LZ-String compressed JSON object appended as `?s=` — DigiKey does not use `?page=` parameters
- Detects and stops on duplicate pages (DigiKey serves page 1 again when the cursor overflows the category)
- Extracts product name, serial number, stock availability (DigiKey + Marketplace split), unit price, package type, and product status
- Saves results to `digikey-category.csv`
- Example usage:
  ```bash
  python scrapeDigikeyCategory.py
  # Output: digikey-category.csv
  ```

### 2. `scrapeDigikeyProduct.py`
**Extracts full product details from a single DigiKey product page.**

- Uses stable `data-testid` selectors throughout — more resilient to layout changes than class-based selectors
- Extracts MPN, manufacturer, detailed description, quantity available, datasheet URL, pricing tiers, and all dynamic product attributes
- Attributes are scraped from the spec table and vary by product category
- Saves results to `digikey-product.json`
- Example usage:
  ```bash
  python scrapeDigikeyProduct.py
  # Output: digikey-product.json
  ```

---

## Requirements

- Python 3.8+
- `requests`, `beautifulsoup4`, `lzstring` libraries
  ```bash
  pip install requests beautifulsoup4 lzstring
  ```
- A [Scrape.do API token](https://dashboard.scrape.do/signup) (free 1000 credits/month)

---

## Setup & Configuration

1. **Register for a Scrape.do API token** and replace `<your_token>` in all scripts.

2. **Configure target URLs:**
   - For `scrapeDigikeyCategory.py`: set `CATEGORY_URL` to any DigiKey category page and `MAX_LISTING_PAGES` to control depth; `LISTING_PAGE_SIZE` and `FILTER_STATE_KEY` can be left as defaults
   - For `scrapeDigikeyProduct.py`: set `PRODUCT_URL` to any DigiKey product detail page

3. **Run the desired script:**
   ```bash
   python scrapeDigikeyCategory.py   # Category listings with pagination
   python scrapeDigikeyProduct.py    # Single product details
   ```

---

## Technical Details

### Request Pattern
Both scripts use `super=true` — residential proxy rotation without JavaScript rendering (DigiKey serves fully rendered HTML server-side):

```python
api_url = f"http://api.scrape.do/?token={TOKEN}&url={urllib.parse.quote(page_url)}&super=true"
```

### LZ-String Cursor Pagination
DigiKey's pagination is driven by a `?s=` query parameter containing an LZ-String compressed JSON object. The cursor structure is `{"5": {"p": page_number, "pp": page_size}}` where `"5"` is DigiKey's internal filter state key for pagination. The `lzstring` package replicates the browser-side compression.

### Duplicate Page Detection
DigiKey silently returns page 1 again when a page cursor exceeds the available results instead of returning an empty page. The script detects this by comparing the first 5 product identifiers across pages.

### Dynamic Attributes
Product attributes in `scrapeDigikeyProduct.py` are scraped from the spec table and will vary by product category — a fiber optic cable will have different attributes than a microcontroller. The script collects all non-empty, non-N/A attribute rows automatically.

---

## Legal & Ethical Notes

- Only scrape publicly accessible data and respect DigiKey's terms of service
- Do not automate excessive requests that may disrupt the service
- Scrape.do handles proxies and headers for you, but always use scraping responsibly
