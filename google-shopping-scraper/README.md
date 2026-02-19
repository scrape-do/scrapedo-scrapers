# Google Shopping Scraper

This folder provides Python scripts to scrape **search results**, **product details**, **seller comparisons**, and **customer reviews** from Google Shopping using [Scrape.do](https://scrape.do).

Scrape.do handles proxy rotation, header spoofing, and TLS fingerprinting so Google doesn't flag your requests as automated.

The tools here let you:
- Scrape product listings from Google Shopping search results with async pagination
- Extract detailed product information via Google's hidden `/async/oapv` endpoint
- Collect seller offers, customer reviews, forum discussions, and product descriptions
- Handle Google's dynamic AJAX loading and session token extraction
- Export results to CSV or JSON

[Find the full technical guide here. 📘](https://scrape.do/blog/google-shopping-scraping/)

All scripts use Python 3, the `requests` library, and `BeautifulSoup` for HTML parsing.

---

## What's Included

### 1. `searchResults.py`
**Scrapes basic product listings from Google Shopping search results with automatic pagination.**

- Extracts product title, price, image URL, seller name, rating, and review count from search cards.
- Uses Google's async pagination endpoint to load all product batches beyond the initial page.
- Extracts session tokens (`ei`, `basejs`, `basecss`, `basecomb`) from the initial page response to build valid pagination URLs.
- Deduplicates products by `(title, price)` to avoid repeated entries across pages.
- Stops automatically after 3 consecutive empty pages.
- Saves results to `google_shopping_search.csv`.
- Example usage:
  ```bash
  python searchResults.py
  # Output: google_shopping_search.csv
  ```

### 2. `singleProductDetail.py`
**Fetches detailed product information from Google's `/async/oapv` detail endpoint.**

- Parses Google's JSPB (JSON Serialized Protocol Buffer) response format.
- Extracts brand, rating, review count, and product description.
- Collects up to 5 product image URLs from the detail payload.
- Extracts customer reviews with text, author, rating, date, and source.
- Extracts forum discussions with title, URL, source, and rating.
- Extracts seller offers with price, original price, currency, seller name, and URL.
- Deduplicates offers by URL.
- Also used as a module by `consistentScraper.py` (imports `parse_product_details`).
- Example usage:
  ```bash
  python singleProductDetail.py
  # Output: Prints parsed product details as JSON to console
  ```

### 3. `consistentScraper.py`
**Full-featured scraper that combines search results with detailed product data into a single JSON export.**

- Runs multi-pass extraction: keeps running extraction passes until no new products are found.
- Collects hidden `data-*` attributes (`catalogid`, `gpcid`, `headlineOfferDocid`, `imageDocid`, `mid`) from product cards to construct detail URLs.
- For products with complete detail parameters: fetches extended data (brand, description, reviews, offers, forums) via the `/async/oapv` endpoint.
- For products without detail parameters: keeps card-level data (title, price, image, seller, rating).
- Ensures uniform JSON schema across all products regardless of detail availability.
- Saves results to `google_shopping_results.json`.
- Example usage:
  ```bash
  python consistentScraper.py
  # Output: google_shopping_results.json
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

## How to Use: `searchResults.py`

**Scrapes product listings from Google Shopping search results.**

1. Replace the token and search query:

   ```python
   TOKEN = "<your-token>"
   QUERY = "wireless gaming headset"
   ```

2. Run:

   ```bash
   python searchResults.py
   ```

**Output:** A CSV file `google_shopping_search.csv` with:
* **title** - Product name
* **price** - Product price
* **image_url** - Product image URL
* **seller_name** - Seller/store name
* **rating** - Product rating
* **review_count** - Number of reviews

---

## How to Use: `singleProductDetail.py`

**Fetches extended product details from a single Google Shopping product.**

1. Copy a `/async/oapv` URL from Chrome DevTools:
   - Open Google Shopping and search for a product
   - Open DevTools (`F12`) → Network tab
   - Click on a product card to open the detail overlay
   - Find the `/async/oapv` request in the Network tab
   - Copy the full request URL

2. Paste the URL and replace the token:

   ```python
   TOKEN = "<your-token>"
   DETAIL_URL = "https://www.google.com/async/oapv?..."
   ```

3. Run:

   ```bash
   python singleProductDetail.py
   ```

**Output:** JSON printed to console with:
* **brand** - Product brand
* **rating** - Average rating
* **review_count** - Total review count
* **description** - Product description
* **detail_images** - Up to 5 product image URLs
* **reviews** - Customer reviews (text, author, rating, date, source)
* **forums** - Forum discussions (title, URL, source, rating)
* **offers** - Seller offers (price, original price, seller name, URL)

---

## How to Use: `consistentScraper.py`

**Full pipeline: search results + product details in one run.**

1. Replace the token and query:

   ```python
   TOKEN = "<your-token>"
   QUERY = "pc wireless gaming headset"
   ```

2. Run:

   ```bash
   python consistentScraper.py
   ```

**Output:** A JSON file `google_shopping_results.json` where each product contains:
* Card-level fields: **title**, **price**, **image_url**, **seller_name**, **rating**, **review_count**, **link**
* Detail fields (when available): **brand**, **description**, **detail_images**, **reviews**, **forums**, **offers**

---

## Technical Details

### Google Shopping URL Structure
Google Shopping uses `udm=28` (Universal Design Mode 28) to return results in Shopping format. The initial page loads a skeleton with minimal products, then fires async requests to populate the rest.

### Async Pagination
Products load through `/search?async=...` endpoints that require session tokens extracted from the initial page:
- **`ei`** (Event Identifier): Session-specific token found in the `kEI` JavaScript variable
- **`basejs`**, **`basecss`**, **`basecomb`**: Asset identifiers from `google.xjs` script blocks

The `start` parameter controls pagination offset (0, 10, 20, etc.).

### Product Detail Endpoint (`/async/oapv`)
Detailed product data (brand, description, reviews, offers) is fetched from Google's OAPV (Open Async Product View) endpoint. This requires hidden parameters from product card `data-*` attributes:
- `catalogid`, `gpcid`, `headlineOfferDocid`, `imageDocid`, `mid`

Not all product cards include these parameters. When missing, card-level data is still available.

### Response Parsing
- Async pagination responses are JSON-wrapped HTML snippets with hex-encoded characters (`\x3d`, `\x22`, etc.) that need unescaping
- Product detail responses use JSPB (JSON Serialized Protocol Buffer) format accessed via `ProductDetailsResult`

---

## Troubleshooting & Tips

- **Empty results from initial page:**
  Google Shopping loads products via async requests, not in the initial HTML. The scripts handle this automatically by extracting tokens and building async URLs.

- **403 or 429 errors:**
  Make sure your Scrape.do token is valid and you have credits remaining. Add delays between requests using the `PAUSE_SECONDS` setting.

- **Missing detail parameters:**
  Google doesn't always include complete `data-*` attributes on every product card. Promoted listings and aggregated offers often lack required parameters. Card-level data (title, price, image) is still extracted.

- **Expired `/async/oapv` URLs:**
  The `ei` token is session-specific and expires. Don't hardcode detail URLs; use `consistentScraper.py` which builds them programmatically from fresh parameters.

- **Fewer products than expected:**
  Try reducing `PAGE_SIZE` to `1` in the script to surface more product slices, as each async page loads a slightly different set of results.

---

## Legal & Ethical Notes

- Only scrape publicly accessible data and respect Google's Terms of Service.
- Do not automate excessive requests or use scraped data for commercial purposes without permission.
- Scrape.do handles proxies, headers, and anti-bot solutions for you, but always use scraping responsibly.

---

## Why Use Scrape.do?

- Rotating premium proxies & geo-targeting
- Built-in header spoofing and TLS fingerprinting
- Handles CAPTCHAs, rate limits, and bot detection automatically
- 1000 free credits/month

👉 [Get your free API token here](https://dashboard.scrape.do/signup)
