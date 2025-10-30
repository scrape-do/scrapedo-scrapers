# Etsy Scraper

This folder contains Python scripts to scrape **product listings**, **single product details**, and **product reviews** from Etsy using [Scrape.do](https://scrape.do).

Scrape.do helps bypass Etsy's anti-bot mechanisms including DataDome, rate limits, and CAPTCHAs.

All scripts use publicly accessible HTML data and require no login or authentication.

[Find extended tutorial here 📘](https://scrape.do/blog/etsy-scraping/)

---

## What's Included

* `categoryScraping.py`: Scrapes multiple product listings from Etsy category/search pages with pagination support (listing ID, name, shop, price, discount, rating, reviews).
* `singleProduct.py`: Scrapes detailed product information from individual Etsy product pages using JSON-LD structured data (name, description, price, images, rating).
* `reviewScraping.py`: Scrapes product reviews with pagination using Etsy's internal API (rating, text, author, date).

---

## Requirements

* Python 3.7+
* `requests` and `beautifulsoup4` libraries<br>Install with:

  ```bash
  pip install requests beautifulsoup4
  ```
* A [Scrape.do API token](https://dashboard.scrape.do/signup) (free 1000 API credits/month)

---

## How to Use: `categoryScraping.py`

**Scrapes product listings from Etsy category or search result pages with automatic pagination.**

1. Replace the token and category URL:

   ```python
   token = "<your-token>"
   base_url = "https://www.etsy.com/c/jewelry"
   max_pages = 3
   ```

2. Run:

   ```bash
   python categoryScraping.py
   ```

**Output:** A CSV file `etsy_collection.csv` with:
* **listing_id** - Unique product listing ID
* **name** - Product name/title
* **shop** - Shop/seller name
* **price** - Current price
* **original_price** - Original price (if discounted)
* **discount_rate** - Discount percentage
* **currency** - Currency symbol
* **rating** - Product rating (out of 5)
* **review_count** - Number of reviews
* **star_seller** - Star Seller badge (boolean)
* **free_shipping** - Free shipping available (boolean)
* **only_left** - Stock quantity remaining
* **image** - Product image URL
* **url** - Product page URL

**Features:**
* Automatic pagination through multiple pages
* Deduplication using listing IDs
* Extracts pricing, ratings, and seller information
* US geo-targeting with proper locale headers

---

## How to Use: `singleProduct.py`

**Scrapes detailed product information from a single Etsy product page.**

1. Replace the token and product URL:

   ```python
   token = "<your-token>"
   product_url = "https://www.etsy.com/listing/468670752/a-man-a-dog-the-original-original-wood"
   ```

2. Run:

   ```bash
   python singleProduct.py
   ```

**Output:** JSON formatted product data printed to console with:
* **listing_id** - Product listing ID
* **name** - Product name
* **description** - Product description
* **category** - Product category
* **shop** - Shop/seller name
* **images** - Array of product image URLs
* **price** - Product price
* **currency** - Currency code (e.g., USD)
* **availability** - Stock status (InStock, OutOfStock)
* **rating** - Average rating
* **review_count** - Total number of reviews

**Features:**
* Extracts JSON-LD structured data for reliable parsing
* Handles multiple image formats
* Supports both single and array offer formats
* US geo-targeting

---

## How to Use: `reviewScraping.py`

**Scrapes product reviews using Etsy's internal API with pagination and sorting options.**

1. Replace the token and product URL:

   ```python
   token = "<your-token>"
   product_url = "https://www.etsy.com/listing/468670752/a-man-a-dog-the-original-original-wood"
   max_pages = 5
   sort_option = "Relevancy"  # Options: "Relevancy", "MostRecent", "MostHelpful"
   ```

2. Run:

   ```bash
   python reviewScraping.py
   ```

**Output:** A CSV file `etsy_reviews.csv` with:
* **listing_id** - Product listing ID
* **review_id** - Unique review ID
* **rating** - Review rating (1-5)
* **text** - Review text/comment
* **author** - Reviewer username
* **created_at** - Review creation date

**Features:**
* Uses Etsy's internal GraphQL API for reviews
* Automatic extraction of listing ID and shop ID from product page
* CSRF token extraction for API authentication
* Multiple sort options (Relevancy, MostRecent, MostHelpful)
* Pagination support with configurable max pages
* Handles JSON responses wrapped in HTML

---

## Common Notes

* **Geo-targeting:** All scrapers use `geoCode=us` for US-based results. Change this to target different regions.
* **Super Mode:** All scrapers use `super=true` for enhanced anti-bot bypass capabilities.
* **Extra Headers:** Category and product scrapers use `extraHeaders=true` with custom locale headers (`sd-x-detected-locale: USD|en-US|US`) for proper currency and language targeting.
* **Error Handling:** All scrapers include try/except blocks to handle missing elements gracefully.
* **Rate Limiting:** Scripts include `time.sleep()` calls to avoid overwhelming the API.

---

## Legal & Ethical Notes

Please ensure:

* You scrape only **public product and review data**
* You **do not automate excessive requests** or violate Etsy's Terms of Service
* Scrape.do handles proxies, headers, and anti-bot solutions; always use scraping responsibly

---

## Why Use Scrape.do?

* Rotating premium proxies & geo-targeting
* Built-in header spoofing
* Handles redirects, CAPTCHAs, and JavaScript rendering
* 1000 free credits/month

👉 [Get your free API token here](https://dashboard.scrape.do/signup)

