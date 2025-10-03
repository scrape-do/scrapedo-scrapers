# Redfin Scraper

This folder provides Python scripts to extract property details and search results from Redfin using [Scrape.do](https://scrape.do) to bypass anti-bot protection and handle JavaScript rendering.

The tools here let you:
- Scrape individual property details from Redfin property pages
- Extract property listings from Redfin search results with automatic pagination
- Get comprehensive property data including price, square footage, address, and broker information
- Save results to CSV for easy analysis

All scripts use Python 3.7+, the `requests` library, and `BeautifulSoup` for HTML parsing.

[Find extended technical guide here. 📘](https://scrape.do/blog/redfin-scraping/)

> ⚠️ **IMPORTANT**: Personal information scraping (phone numbers, agent names) is commented out for ethical reasons. Scraping personal information at scale can be illegal and unethical in many jurisdictions.

---

## What's Included

### 1. `scrapePropertyDetails.py`
**Scrapes detailed information from individual Redfin property pages.**

- Uses Scrape.do to render property pages and extract comprehensive details
- Extracts full address, price, property ID, property type, square feet, city, state, zip code
- Gets main image link, listing agent info, and listing last updated date
- Supports multiple property URLs in a single run
- Saves results to `redfin_property_details.csv`
- Example usage:
  ```bash
  python scrapePropertyDetails.py
  # Output: redfin_property_details.csv
  ```

### 2. `scrapeSearchResults.py`
**Scrapes property listings from Redfin search results with automatic pagination.**

- Scrapes multiple pages of search results (configurable max_pages, default: 9)
- Extracts property ID, URL, main image, square feet, price, full address, and broker
- Handles pagination automatically through all available result pages
- Removes duplicate listings based on property ID
- Saves results to `redfin_search_results.csv`
- Example usage:
  ```bash
  python scrapeSearchResults.py
  # Output: redfin_search_results.csv
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

1. **Register for a Scrape.do API token** and replace the `TOKEN` variable in both scripts.

2. **Configure target URLs as needed:**
   - For `scrapePropertyDetails.py`: Update the `target_urls` list with specific property URLs
   - For `scrapeSearchResults.py`: Change the `base_url` variable to any Redfin search URL

3. **Run the desired script:**
   ```bash
   python scrapePropertyDetails.py    # Individual property details
   python scrapeSearchResults.py      # Search results with pagination
   ```

4. **Check the output CSV files for your results.**


---

## Troubleshooting & Tips

- **403 or 429 errors:**
  - Make sure your Scrape.do token is valid and you have credits left
  - Double-check your target URLs are accessible Redfin pages

- **Missing property data:**
  - Some properties may not have all fields (e.g., square footage, agent info)
  - The scripts handle missing data gracefully with empty strings

- **Empty search results:**
  - Ensure the search URL is valid and returns results
  - Check that the area has properties available for sale

- **Pagination issues:**
  - Most Redfin search results have a maximum of 9 pages
  - Adjust `max_pages` if you need to scrape fewer pages

---

## Legal & Ethical Notes

- Only scrape publicly accessible data and respect Redfin's terms of service
- Do not automate excessive requests or use scraped data for commercial purposes without permission
- Scrape.do handles proxies, headers, and anti-bot solutions for you, but always use scraping responsibly
- Avoid scraping phone numbers and personal information of brokers for commercial projects as it may be subject to legal penalties in most regions.

---

## Why Use Scrape.do?

- Rotating premium proxies & geo-targeting
- Built-in header spoofing and browser fingerprinting
- Handles redirects, CAPTCHAs, and JavaScript rendering
- 1000 free credits/month

[Get your free API token here](https://dashboard.scrape.do/signup)