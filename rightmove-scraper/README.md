# Rightmove Scraper

This folder provides Python scripts to extract property listings and detailed property data from Rightmove using [Scrape.do](https://scrape.do) to bypass bot detection and fetch server-rendered HTML reliably.

The tools here let you:
- Scrape paginated property listing results with address, price, type, bedrooms, agent, and phone
- Extract 15+ structured fields from individual property detail pages via embedded `window.PAGE_MODEL` JSON
- Save listing results to CSV for easy analysis

[Get full technical tutorial here 📕](https://scrape.do/blog/rightmove-scraping/)

All scripts use Python 3.7+, the `requests` library, and `BeautifulSoup` for HTML parsing.

---

## What's Included

### 1. `scrapeListings.py`
**Scrapes paginated property listing results from a Rightmove search.**

- Iterates through multiple pages using the `index` offset parameter (24 results per page)
- Extracts address, price, property type, bedrooms, agent name, and phone number from each card
- Deduplicates results across pages using a URL set
- Cleans price labels (removes "FEATURED", "PREMIUM LISTING", "Guide Price" prefixes)
- Saves results to `listings.csv`
- Example usage:
  ```bash
  python scrapeListings.py
  # Output: listings.csv
  ```

### 2. `scrapePropertyDetails.py`
**Extracts detailed data from a single Rightmove property page via embedded JSON.**

- Fetches the property page and locates the `window.PAGE_MODEL` JSON object in a script tag using a brace-depth parser
- Extracts 15 fields: id, address, postcode, price, price qualifier, price per sqft, property type, bedrooms, bathrooms, size (sqft), tenure, description, nearest station, station distance, and URL
- Prints all fields to the terminal
- Example usage:
  ```bash
  python scrapePropertyDetails.py
  ```

---

## Requirements

- Python 3.7+
- `requests`, `beautifulsoup4` libraries
  ```bash
  pip install requests beautifulsoup4
  ```
- A [Scrape.do API token](https://dashboard.scrape.do/signup) (free 1000 credits/month)

---

## Setup & Configuration

1. **Register for a Scrape.do API token** and replace `<your_token>` in all scripts.

2. **Configure your search (for `scrapeListings.py`):**
   - Update `params` with your desired `searchLocation` and `locationIdentifier`
   - Set `TOTAL_PAGES` to control how many pages to scrape (max 42 for a full run)

3. **Configure target property (for `scrapePropertyDetails.py`):**
   - Set `PROPERTY_URL` to any Rightmove property page URL

4. **Run the desired script:**
   ```bash
   python scrapeListings.py         # Paginated listing results
   python scrapePropertyDetails.py  # Single property detail extraction
   ```

---

## Technical Details

### Request Pattern
Both scripts use the basic Scrape.do endpoint (no `super` or `render` required — Rightmove serves server-rendered HTML):

```python
encoded_url = urllib.parse.quote(target_url, safe="")
api_url = f"http://api.scrape.do/?token={TOKEN}&url={encoded_url}"
```

### Pagination
`scrapeListings.py` calculates the page offset as `index = page * 24` and appends it to the query string. Rightmove returns up to 24 results per page with a maximum of ~1,000 results (42 pages).

### Embedded JSON Extraction
`scrapePropertyDetails.py` uses a brace-depth counter to extract the `window.PAGE_MODEL` JSON object from an inline script tag — no regex needed for the full object, just `json.loads()` on the extracted substring.

---

## Legal & Ethical Notes

- Only scrape publicly accessible data and respect Rightmove's terms of service
- Do not automate excessive requests that may disrupt the service
- Scrape.do handles proxies and headers for you, but always use scraping responsibly
