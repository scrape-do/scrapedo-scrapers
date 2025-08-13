# Amazon Scraper

This folder provides Python scripts to extract product data, reviews, and search results from Amazon using [Scrape.do](https://scrape.do) to bypass Amazon's anti-bot protection and handle JavaScript rendering.

The tools here let you:
- Scrape individual product details from Amazon product pages
- Extract product reviews with ratings, dates, and helpful vote counts
- Scrape search results and category pages with automatic pagination
- Extract product variations (size, color, etc.) from complex multi-variant products
- Save results to CSV for easy analysis

[Find extended technical guide here](https://scrape.do/blog/amazon-scraping/) and [here 📘](https://scrape.do/blog/scrape-amazon-reviews/).

All scripts use Python 3.7+, the `requests` library, and `BeautifulSoup` for HTML parsing.

---

## What's Included

### 1. `singleVariationProduct.py`
**Scrapes individual product details from a specific Amazon product page.**

- Uses Scrape.do to render the product page and extract key information
- Extracts product title, price, main image, and basic product details
- Handles out-of-stock products and price variations
- Simple single-page scraping for standard products
- Example usage:
  ```bash
  python singleVariationProduct.py
  ```

### 2. `multipleVariationProduct.py`
**Extracts all product variations from complex multi-variant Amazon products.**

- **Recursive scraping** through all product dimensions (color, size, style, etc.)
- Automatically discovers available variation options from product pages
- Extracts complete variation matrix with prices for each combination
- Prioritizes dimension traversal order for optimal scraping efficiency
- Saves comprehensive variation data to `amazon_variations.csv`
- Example usage:
  ```bash
  python multipleVariationProduct.py
  # Output: amazon_variations.csv
  ```

### 3. `reviews.py`
**Scrapes Amazon product reviews with detailed metadata.**

- Extracts star ratings, review dates, review content, and helpful vote counts
- Handles reviews from any country (automatically extracts clean dates)
- Extracts numeric helpful vote counts from text (e.g., "2" from "2 people found this helpful")
- Uses robust selectors to ensure all reviews have star ratings
- Saves results to `amazon_reviews.csv`
- Example usage:
  ```bash
  python reviews.py
  # Output: amazon_reviews.csv
  ```

### 4. `category&SearchResults.py`
**Scrapes Amazon search results and category pages with configurable URLs.**

- **Easy URL configuration** - just change the `base_url` variable
- Automatic pagination handling for search results and category pages
- Smart URL parameter management (handles existing page parameters)
- Works with any Amazon search query or category URL
- Extracts product names, prices, links, and images
- Saves results to `amazon_search_results.csv`
- Example usage:
  ```bash
  python category&SearchResults.py
  # Output: amazon_search_results.csv
  ```

---

## Requirements

- Python 3.7+
- `requests`, `beautifulsoup4`, and `csv` libraries
  ```bash
  pip install requests beautifulsoup4
  ```
- A [Scrape.do API token](https://dashboard.scrape.do/signup) (free 1000 credits/month)

---

## Setup & Step-by-Step Usage

1. **Register for a Scrape.do API token** and replace `<your-token>` in all scripts.

2. **Configure target URLs as needed:**
   - For `singleVariationProduct.py`: Set the `PRODUCT_URL` variable
   - For `multipleVariationProduct.py`: Set the `PRODUCT_URL` variable  
   - For `reviews.py`: Set the `url` variable to any Amazon product page
   - For `category&SearchResults.py`: Set the `base_url` variable to any search or category URL

3. **Run the desired script:**
   ```bash
   python singleVariationProduct.py     # Individual product details
   python multipleVariationProduct.py   # All product variations
   python reviews.py                    # Product reviews
   python category&SearchResults.py     # Search results/categories
   ```

4. **Check the output CSV files for your results.**

---

## Technical Details

### Multi-Variation Scraping
`multipleVariationProduct.py` uses recursive dimension traversal:
- **Dimension discovery**: Automatically finds available variations (color, size, etc.)
- **Priority ordering**: Optimizes scraping order based on common variation types
- **Recursive extraction**: Systematically explores all variation combinations
- **Selection detection**: Identifies currently selected variations on each page

### URL Configuration
`category&SearchResults.py` handles flexible URL input:
- **Search URLs**: `"https://www.amazon.com/s?k=wireless+headphones"`
- **Category URLs**: `"https://www.amazon.com/Electronics/b?node=172282"`
- **Filtered URLs**: Automatically handles existing parameters and filters
- **Pagination**: Smart page parameter injection for any URL structure

### Review Data Extraction
`reviews.py` uses robust parsing techniques:
- **Multi-country support**: Handles "Reviewed in [Country] on [Date]" formats
- **Fallback selectors**: Multiple star rating detection methods
- **Clean data output**: Numeric helpful votes and clean date formats

---

## Configuration Examples

### Search Different Products
```python
# In category&SearchResults.py
base_url = "https://www.amazon.com/s?k=laptop+stands"        # Search query
base_url = "https://www.amazon.com/Electronics/b?node=172282" # Category page
base_url = "https://www.amazon.com/s?k=books&rh=p_36%3A-1000" # With price filter
```

### Scrape Different Product Pages
```python
# In reviews.py or variation scripts
url = "https://us.amazon.com/Apple-iPhone-Plus-128GB-Blue/dp/B0CG84XR6N/"
url = "https://us.amazon.com/Calvin-Klein-Underwear-Classics/dp/B07TCJS1NS"
```

---

## Troubleshooting & Tips

- **403 or 429 errors:**
  - Make sure your Scrape.do token is valid and you have credits left
  - Double-check your target URLs are accessible

- **Missing variation data:**
  - Some products may not have variations or may use different HTML structures
  - Check that the product page has size/color/style options

- **Empty review data:**
  - Ensure the product has reviews and the review section is publicly accessible
  - Some new products may not have reviews yet

---

## Legal & Ethical Notes

- Only scrape publicly accessible data and respect Amazon's terms of service
- Do not automate excessive requests or use scraped data for commercial purposes without permission
- Scrape.do handles proxies, headers, and anti-bot solutions for you, but always use scraping responsibly

---

## Why Use Scrape.do?

- Rotating premium proxies & geo-targeting
- Built-in header spoofing and browser fingerprinting
- Handles redirects, CAPTCHAs, and JavaScript rendering
- 1000 free credits/month

[Get your free API token here](https://dashboard.scrape.do/signup)