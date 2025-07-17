# HungerStation Scraper

[Find full technical guide here 📘](https://scrape.do/blog/hunger-station-scraping/)

This folder provides Python scripts to extract restaurant listings and menu data from HungerStation using [Scrape.do](https://scrape.do) to bypass Cloudflare anti-bot protections and session geo-restrictions.

The tools here let you:
- Scrape all available restaurants in a given region (with pagination)
- Scrape all menu items from a specific restaurant/store page

All scripts use Python 3, the `requests` library, and `BeautifulSoup` for HTML parsing.

---

## What's Included

### 1. `storeListScraper.py`
**Scrapes all restaurant listings for a given region (with pagination).**

- Uses Scrape.do to fetch the HTML for a region's restaurant listings page.
- Loops through all paginated result pages by incrementing the `?page=` parameter.
- For each restaurant, extracts:
  - Store link (full URL)
  - Store name
  - Category
  - Review rating
- Saves all results to `hungerstation_restaurants.csv`.
- Example usage:
  ```bash
  python storeListScraper.py
  # Output: hungerstation_restaurants.csv
  ```

### 2. `storeMenuScraper.py`
**Scrapes all menu items from a specific restaurant/store page.**

- Uses Scrape.do to fetch the HTML for a store's menu page.
- For each menu category, extracts all menu items, including:
  - Category (section id)
  - Name
  - Description
  - Price
  - Calories
- Saves all results to `hungerstation_menu_items.csv`.
- Example usage:
  ```bash
  python storeMenuScraper.py
  # Output: hungerstation_menu_items.csv
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
2. **Scrape all restaurants in a region:**
   - Set `BASE_URL` in `storeListScraper.py` to your target region URL, e.g.:
     ```python
     BASE_URL = "https://hungerstation.com/sa-en/restaurants/al-khobar/al-jisr"
     ```
   - Run the script:
     ```bash
     python storeListScraper.py
     # Output: hungerstation_restaurants.csv
     ```
3. **Scrape all menu items from a store:**
   - Set `STORE_URL` in `storeMenuScraper.py` to your target store URL, e.g.:
     ```python
     STORE_URL = "https://hungerstation.com/sa-en/restaurant/al-khobar/al-jisr/13699"
     ```
   - Run the script:
     ```bash
     python storeMenuScraper.py
     # Output: hungerstation_menu_items.csv
     ```

---

## Troubleshooting & Tips

- **403 or 429 errors:**
  - Make sure your Scrape.do token is valid and you have credits left.
  - Double-check your URLs and that the region/store is public and available.
- **Empty or missing fields:**
  - The HTML structure may have changed; inspect the page and update the parsing logic if needed.
  - Ensure the store or region page is not restricted or empty.
- **Encoding issues:**
  - The scripts write CSV files with UTF-8 encoding for compatibility.

---

## Legal & Ethical Notes

- Only scrape publicly accessible data and respect HungerStation's terms of service.
- Do not automate excessive requests or use scraped data for commercial purposes without permission.
- Scrape.do handles proxies, headers, and anti-bot solutions for you, but always use scraping responsibly.

---

## Why Use Scrape.do?

- Rotating premium proxies & geo-targeting
- Built-in header spoofing
- Handles redirects, CAPTCHAs, and JavaScript rendering
- 1000 free credits/month

[Get your free API token here](https://dashboard.scrape.do/signup) 