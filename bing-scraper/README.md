# Bing Scraper

This folder contains Python scripts to scrape **web search results**, **image search results**, and **shopping products** from Bing using [Scrape.do](https://scrape.do).

Scrape.do helps bypass Bing's anti-bot mechanisms, rate limits, and CAPTCHAs.

All scripts use publicly accessible HTML data and require no login or authentication.

[Find extended tutorial here 📘](https://scrape.do/blog/cineworld-scraping/)

---

## What's Included

* `bingSearchScraper.py`: Scrapes organic web search results with pagination support (title, URL, description).
* `bingImageScraper.py`: Scrapes image search results with optional download functionality (title, image URL, source URL, thumbnail).
* `bingShoppingScraper.py`: Scrapes shopping/product results (product name, price, seller, URL).
* `bingNewsScraper.py`: Scrapes news articles with infinite scroll pagination (title, URL, snippet, source, published time).

---

## Requirements

* Python 3.7+
* `requests` and `beautifulsoup4` libraries<br>Install with:

  ```bash
  pip install requests beautifulsoup4
  ```
* A [Scrape.do API token](https://dashboard.scrape.do/signup) (free 1000 API credits/month)

---

## How to Use: `bingSearchScraper.py`

**Scrapes organic web search results from Bing with automatic pagination.**

1. Replace the token and query:

   ```python
   token = "<your-token>"
   query = "when was coffee invented"
   max_pages = 10
   ```

2. Run:

   ```bash
   python bingSearchScraper.py
   ```

**Output:** A CSV file `bing_search_results.csv` with:
* **Title** - Search result title
* **URL** - Link to the page
* **Description** - Result snippet/description

**Features:**
* Automatic pagination through multiple pages
* Retry logic (sends 2 additional requests when 0 results found)
* Stops when no more results are available or max_pages is reached

---

## How to Use: `bingImageScraper.py`

**Scrapes image search results from Bing Images.**

1. Replace the token and query:

   ```python
   token = "<your-token>"
   query = "coffee"
   max_results = 100
   ```

2. Run:

   ```bash
   python bingImageScraper.py
   ```

**Output:** A CSV file `bing_image_results.csv` with:
* **Title** - Image description/title
* **Image URL** - Full-size image URL
* **Source URL** - Website where the image is from
* **Thumbnail URL** - Thumbnail image URL

**Optional: Download Images**

The script includes a commented-out section to download all scraped images. To enable:

1. Uncomment lines 74-105 (the entire `DOWNLOAD IMAGES SECTION` block)
2. Run the script

Images will be saved to a `downloaded_images/` folder with filenames like `coffee_1.jpg`, `coffee_2.jpg`, etc.

---

## How to Use: `bingShoppingScraper.py`

**Scrapes product listings from Bing Shopping.**

1. Replace the token and query:

   ```python
   token = "<your-token>"
   query = "iphone"
   ```

2. Run:

   ```bash
   python bingShoppingScraper.py
   ```

**Output:** A CSV file `bing_shopping_results.csv` with:
* **Product Name** - Name of the product
* **Price** - Product price
* **Seller** - Seller/store name
* **URL** - Link to the product page

**Note:** This scraper uses `super=true` parameter for better JavaScript rendering.

---

## How to Use: `bingNewsScraper.py`

**Scrapes news articles from Bing News with infinite scroll pagination.**

1. Replace the token and query:

   ```python
   token = "<your-token>"
   query = "tesla"
   max_results = 100
   ```

2. Run:

   ```bash
   python bingNewsScraper.py
   ```

**Output:** A CSV file `bing_news_results.csv` with:
* **Title** - Article headline
* **URL** - Link to the full article
* **Snippet** - Article summary/excerpt
* **Source** - Publisher name (e.g., BBC, Yahoo Finance)
* **Published Time** - When the article was published (e.g., "1d", "2h")

**Features:**
* Uses Bing's infinite scroll API endpoint for news
* Sorted by date (most recent first)
* Automatic pagination (increments by 10)
* Stops when no more articles are available or max_results is reached

---

## Common Notes

* **URL Encoding:** Image and shopping scrapers use `urllib.parse.quote()` to properly encode URLs with query parameters.
* **Geo-targeting:** All scrapers use `geoCode=us` for US-based results. Change this to target different regions (e.g., `geoCode=uk`, `geoCode=de`).
* **Error Handling:** All scrapers include try/except blocks to handle missing elements gracefully.
* **Super Mode:** If you're seeing results from a different country than what you've enabled in the `geoCode=` parameter, you might need to enable `super=true` to fetch results in your preferred country.

---

## Legal & Ethical Notes

Please ensure:

* You scrape only **public search results**
* You **do not automate excessive requests** or violate Bing's Terms of Service
* Scrape.do handles proxies, headers, and anti-bot solutions; always use scraping responsibly

---

## Why Use Scrape.do?

* Rotating premium proxies & geo-targeting
* Built-in header spoofing
* Handles redirects, CAPTCHAs, and JavaScript rendering
* 1000 free credits/month

👉 [Get your free API token here](https://dashboard.scrape.do/signup)

