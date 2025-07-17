# DoorDash Scraper

[Find extended technical guide here. 📘](https://scrape.do/blog/doordash-scraping/)

This folder provides a set of Python scripts to extract restaurant, grocery, and product data from DoorDash using [Scrape.do](https://scrape.do) to bypass heavy Clouflare anti-bot protection and session restriction.

The tools here let you:
- Register a delivery address and generate a session for personalized listings
- Scrape all available restaurants and grocery stores for a given address
- Scrape all products in a specific category of a specific store (convenience, grocery, etc.)
- Scrape the full menu of a local store or restaurant (no session required)

All scripts use Python 3, the `requests` library, and (where needed) `BeautifulSoup` for HTML parsing.

---

## What's Included

### 1. `addConsumerAddress.py`
**Registers a delivery address and generates a Scrape.do Session ID.**

- Sends a GraphQL mutation to DoorDash to add a consumer address.
- The response includes a session ID (see the `scrape.do-rid` header in the response).
- **The last 6 digits of this session ID must be used as the `SESSION_ID` in the other scripts** to ensure all requests are for the same address.
- This is required for scraping personalized store and product listings.
- Example usage:
  ```bash
  python addConsumerAddress.py
  # Look for the scrape.do-rid header in the output
  ```

### 2. `scrapeStoreRestaurantListings.py`
**Scrapes all restaurants and grocery stores available for the address set in `addConsumerAddress.py`.**

- Uses the session ID from `addConsumerAddress.py` to fetch listings for the registered address.
- Paginates through all available stores and restaurants.
- Extracts details such as name, description, delivery fee, ETA, open status, rating, price range, distance, store ID, and link.
- Saves the results to `doordash_restaurant_listings.csv`.
- Example usage:
  ```bash
  python scrapeStoreRestaurantListings.py
  # Output: doordash_restaurant_listings.csv
  ```

### 3. `scrapeChainStoreCategories.py`
**Scrapes all available products from a specific category of a specific store (e.g., convenience, grocery) for the registered address.**

- Requires both a store ID and a category ID, which can be found in the DoorDash URL structure, e.g.:
  `https://www.doordash.com/convenience/store/1235954/category/drinks-751`  
  Here, `storeId` is `1235954` and `categoryId` is `drinks-751`.
- Uses the same session ID as above to ensure the product list matches the registered address.
- Paginates through all products in the category.
- Extracts product name, price, review count, average rating, stock, image URL, and description.
- Saves the results to `doordash_category_products.csv`.
- Example usage:
  ```bash
  python scrapeChainStoreCategories.py
  # Output: doordash_category_products.csv
  ```

### 4. `scrapeStoreMenuCatalog.py`
**Scrapes all menu items from a local store or restaurant.**

- Does **not** require a session ID or registered address.
- Works for any DoorDash store or restaurant page.
- Extracts all menu items, including name, description, price, rating, review count, and image URL.
- Saves the results to `menu_items.csv`.
- Example usage:
  ```bash
  python scrapeStoreMenuCatalog.py
  # Output: menu_items.csv
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
2. **Register an address:**
   - Run `addConsumerAddress.py` and note the `scrape.do-rid` header in the response.
   - Use the last 6 digits of this value as `SESSION_ID` in `scrapeStoreRestaurantListings.py` and `scrapeChainStoreCategories.py`.
3. **Scrape listings or products:**
   - Run `scrapeStoreRestaurantListings.py` to get all available stores for your address.
   - Run `scrapeChainStoreCategories.py` to get all products in a category for a specific store and address.
   - Run `scrapeStoreMenuCatalog.py` to get all menu items from any store or restaurant (no sessionId required).
4. **Find Store and Category IDs:**
   - For chain/grocery/convenience stores, extract these from the DoorDash URL as shown above.

---

## Troubleshooting & Tips

- **403 or 429 errors:**
  - Make sure your Scrape.do token is valid and you have credits left.
  - Double-check your session ID and that it matches the address you registered.
- **Empty or missing fields:**
  - Ensure the address you registered is serviceable by DoorDash.
  - Make sure the store/category IDs are correct and available for your address.
- **Session Expiry:**
  - If you get unexpected results, re-run `addConsumerAddress.py` to generate a new session and update the session ID in the other scripts.
- **Menu script not found:**
  - For `scrapeStoreMenuCatalog.py`, make sure the store page is public and available.

---

## Legal & Ethical Notes

- Only scrape publicly accessible data and respect DoorDash's terms of service.
- Do not automate excessive requests or use scraped data for commercial purposes without permission.
- Scrape.do handles proxies, headers, and anti-bot solutions for you, but always use scraping responsibly.

---

## Why Use Scrape.do?

- Rotating premium proxies & geo-targeting
- Built-in header spoofing
- Handles redirects, CAPTCHAs, and JavaScript rendering
- 1000 free credits/month

[Get your free API token here](https://dashboard.scrape.do/signup) 