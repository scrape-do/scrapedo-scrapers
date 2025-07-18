# Uber Eats Scraper

This folder provides a set of Python scripts to extract store listings, menu items, and catalog data from Uber Eats using [Scrape.do](https://scrape.do) to bypass anti-bot protection and session restrictions as well as render JavaScript.

The tools here let you:
- Scrape all available stores for a given location (API and frontend HTML)
- Scrape all menu items from a specific restaurant page
- Scrape all products in a specific section of a chain store (with pagination and robust handling)
- Save results to CSV for easy analysis

[For full technical guide, go here 📘](https://scrape.do/blog/ubereats-scraping/)

All scripts use Python 3, the `requests` library, and (where needed) `BeautifulSoup` for HTML parsing.

---

## What's Included

### 1. `backendStoreList.py`
**Scrapes all available stores for a given location using the Uber Eats backend API.**

- Sends POST requests to the Uber Eats `getFeedV1` API endpoint via Scrape.do.
- Paginates through all available stores for a location you specify.
- **You must set the `uev2.loc` cookie and `placeId` variables at the top of the script.**
  - `uev2.loc`: Extract from your browser cookies after you select an address on Uber Eats.
  - `placeId`: Extract from the payload in your browser's network tab (look for `placeId` in POST requests).
- Extracts all feed items and saves them to `feed_response.json`.
- Example usage:
  ```bash
  python backendStoreList.py
  # Output: feed_response.json
  ```

### 2. `frontendStoreList.py`
**Scrapes all available stores for a given location by rendering the Uber Eats frontend HTML.**

- Uses Scrape.do's browser automation to click "Show more" and load all stores.
- **You must set the `pl` parameter at the top of the script.**
  - `pl`: Extract from the Uber Eats URL after you select an address (it's the value after `pl=` in the URL).
- Parses the HTML with BeautifulSoup to extract store name, URL, promotion, rating, and review count.
- Saves the results to `ubereats_store_cards.csv`.
- Example usage:
  ```bash
  python frontendStoreList.py
  # Output: ubereats_store_cards.csv
  ```

### 3. `scrapeRestaurantMenu.py`
**Scrapes all menu items from a specific Uber Eats restaurant page.**

- Uses Scrape.do to render the restaurant page and save the HTML.
- **You must set the `ubereats_restaurant_url` at the top of the script.**
  - Extract the full restaurant URL from your browser.
- Parses the HTML with BeautifulSoup to extract each menu item's category, name, and price.
- Saves the results to `ubereats_restaurant_menu.csv`.
- Example usage:
  ```bash
  python scrapeRestaurantMenu.py
  # Output: ubereats_restaurant_menu.csv
  ```

### 4. `scrapeChainStoreCategories.py`
**Scrapes all products from a specific section of a chain store (e.g., grocery, convenience) with robust pagination.**

- Uses Scrape.do to send POST requests to the Uber Eats `getCatalogPresentationV2` API endpoint.
- **You must set the `store_uuid` and `section_uuids` variables at the top of the script.**
  - Extract these from the Uber Eats URL for the store/section you want to scrape.
- Handles pagination, trying both with and without the `sectionTypes` field for maximum compatibility.
- Extracts product UUID, title, description, price (in dollars), image URL, availability, and section/product UUIDs.
- Saves the results to `catalog_items.csv`.
- Example usage:
  ```bash
  python scrapeChainStoreCategories.py
  # Output: catalog_items.csv
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
2. **Configure location or store/section IDs as needed:**
   - For `backendStoreList.py`, set the `uev2.loc` cookie and `placeId` variables at the top of the script. See comments in the script for how to extract these from your browser.
   - For `frontendStoreList.py`, set the `pl` parameter at the top of the script. See comments in the script for how to extract this from the Uber Eats URL after selecting an address.
   - For `scrapeChainStoreCategories.py`, set `store_uuid` and `section_uuids` at the top of the script. See comments for how to extract these from the URL.
   - For `scrapeRestaurantMenu.py`, set the `ubereats_restaurant_url` at the top of the script. See comments for how to extract this from the URL.
3. **Run the desired script:**
   - `python backendStoreList.py` to get all stores via API.
   - `python frontendStoreList.py` to get all stores via HTML.
   - `python scrapeRestaurantMenu.py` to get all menu items from a restaurant.
   - `python scrapeChainStoreCategories.py` to get all products in a chain store section.
4. **Check the output CSV or JSON files for your results.**

---

## Troubleshooting & Tips

- **403 or 429 errors:**  
  - Make sure your Scrape.do token is valid and you have credits left.
  - Double-check your location, store, or section IDs.
- **Empty or missing fields:**  
  - Ensure the location or store/section you are scraping is available and has products.
  - Try both with and without `sectionTypes` in `scrapeChainStoreCategories.py` (the script does this automatically).
- **Session Expiry:**  
  - If you get unexpected results, try a different location or refresh your Scrape.do token.

---

## Legal & Ethical Notes

- Only scrape publicly accessible data and respect Uber Eats' terms of service.
- Do not automate excessive requests or use scraped data for commercial purposes without permission.
- Scrape.do handles proxies, headers, and anti-bot solutions for you, but always use scraping responsibly.

---

## Why Use Scrape.do?

- Rotating premium proxies & geo-targeting
- Built-in header spoofing
- Handles redirects, CAPTCHAs, and JavaScript rendering
- 1000 free credits/month

[Get your free API token here](https://dashboard.scrape.do/signup) 