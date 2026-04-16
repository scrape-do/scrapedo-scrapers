# Alibaba Scraper

This folder provides Python scripts to extract product listings, product details, and reviews from Alibaba using [Scrape.do](https://scrape.do) with residential proxies and US geo-targeting to reliably access Alibaba's data.

The tools here let you:
- Scrape paginated category listings from embedded `window._PAGE_DATA_` JSON — no DOM parsing required
- Extract full product detail (images, price tiers, MOQ, attributes) from `window.detailData` JSON
- Scrape paginated reviews by signing MTOP API requests with session cookies obtained via Scrape.do

[Get full technical tutorial here 📕](https://scrape.do/blog/alibaba-scraping/)

All scripts use Python 3.8+, the `requests` library, and standard library modules only.

---

## What's Included

### 1. `scrapeAlibabaCategory.py`
**Scrapes paginated product listings from an Alibaba category page.**

- Extracts listing data from `window._PAGE_DATA_` JSON embedded in the HTML — more reliable than DOM selectors
- Reads the `urlRule` from the first page's pagination object to build subsequent page URLs
- Skips ads and store cards (filters on `/product-detail/` in the product URL)
- Extracts name, price, image, min order, review count, review rating, and supplier order count
- Saves results to `alibaba-category-products.csv`
- Example usage:
  ```bash
  python scrapeAlibabaCategory.py
  # Output: alibaba-category-products.csv
  ```

### 2. `scrapeAlibabaProduct.py`
**Extracts full product details from a single Alibaba product page.**

- Parses `window.detailData` JSON using a brace-depth walker (same pattern as Rightmove's PAGE_MODEL)
- Extracts title, gallery images, price tiers (MOQ bands), MOQ, quantity unit, store review rating/count, sales volume, and all dynamic product attributes
- Saves results to `alibaba-product.json`
- Example usage:
  ```bash
  python scrapeAlibabaProduct.py
  # Output: alibaba-product.json
  ```

### 3. `scrapeAlibabaReviews.py`
**Scrapes paginated product reviews via Alibaba's signed MTOP API.**

- Fetches the product page first to extract `companyId`, `sellerAliId`, and `productId`
- Hits the MTOP gateway with a dummy request to obtain `_m_h5_tk` session cookies via the `Scrape.do-Cookies` response header
- Signs each paginated MTOP request with an MD5 hash of `token + timestamp + appKey + payload`
- Extracts review text, reviewer name, rating, date, and attached image URLs
- Saves reviews to `alibaba-reviews.csv` and context metadata to `alibaba-reviews-context.json`
- Example usage:
  ```bash
  python scrapeAlibabaReviews.py
  # Output: alibaba-reviews.csv, alibaba-reviews-context.json
  ```

---

## Requirements

- Python 3.8+
- `requests` library
  ```bash
  pip install requests
  ```
- A [Scrape.do API token](https://dashboard.scrape.do/signup) (free 1000 credits/month)

---

## Setup & Configuration

1. **Register for a Scrape.do API token** and replace `<your_token>` in all scripts.

2. **Configure target URLs:**
   - For `scrapeAlibabaCategory.py`: set `CATEGORY_URL` to any Alibaba category page and `MAX_PAGES` for pagination depth
   - For `scrapeAlibabaProduct.py`: set `PRODUCT_URL` to any Alibaba product detail page
   - For `scrapeAlibabaReviews.py`: set `PRODUCT_URL` to the product page you want reviews for; adjust `MTOP_MAX_PAGES` and `MTOP_PAGE_SIZE` as needed

3. **Run the desired script:**
   ```bash
   python scrapeAlibabaCategory.py   # Category listings
   python scrapeAlibabaProduct.py    # Single product details
   python scrapeAlibabaReviews.py    # Product reviews
   ```

---

## Technical Details

### Request Pattern
All scripts use `super=true&geoCode=us` — residential proxies with US geo-targeting, which is required for Alibaba to serve English-language results with full data:

```python
api_url = "http://api.scrape.do/?" + urllib.parse.urlencode(
    {"token": TOKEN, "url": target_url, "super": "true", "geoCode": "us"},
    quote_via=urllib.parse.quote,
)
```

### Embedded JSON Extraction
Both `scrapeAlibabaCategory.py` and `scrapeAlibabaProduct.py` use a brace-depth walker to extract large JSON blobs from inline script tags rather than regex, which avoids issues with nested objects and special characters.

### MTOP Review API
`scrapeAlibabaReviews.py` uses Alibaba's internal MTOP gateway (`acs.h.alibaba.com`). Each request must be signed with an MD5 hash: `md5(h5_token + "&" + timestamp + "&" + appKey + "&" + payload)`. The session token is obtained by making a dummy MTOP call first and reading the `_m_h5_tk` value from the `Scrape.do-Cookies` response header.

---

## Legal & Ethical Notes

- Only scrape publicly accessible data and respect Alibaba's terms of service
- Do not automate excessive requests that may disrupt the service
- Scrape.do handles proxies and headers for you, but always use scraping responsibly
