# Cineworld Scraper

[Find extended technical guide here 📔](https://scrape.do/blog/cineworld-scraping/)

This repository provides Python scripts to extract movie screenings and ticket prices from Cineworld UK using [Scrape.do](https://scrape.do) to bypass Cineworld's anti-bot protection and handle JavaScript rendering.

The tools here let you:
- Scrape movie screenings for any Cineworld cinema across multiple dates
- Extract ticket prices for different ticket types (adult, child, student, etc.)
- Handle geo-restrictions and Cloudflare protection automatically
- Save results to JSON and CSV for easy analysis

All scripts use Python 3.7+, the `requests` library, and `BeautifulSoup` for HTML parsing.

---

## What's Included

### 1. `scrapeScreenings.py`
**Scrapes movie screenings from Cineworld for a specified date range.**

- Extracts movie names, showtimes, dates, and internal Vista session IDs
- Handles date validation and fallback detection
- Supports multiple-day scraping with automatic retry logic
- Saves comprehensive screening data to `screenings.json`
- Example usage:
  ```bash
  python scrapeScreenings.py
  # Output: screenings.json
  ```

### 2. `scrapePrices.py`
**Extracts ticket prices for all screenings from the `screenings.json` file.**

- Uses session IDs from `scrapeScreenings.py` to fetch ticket pricing
- Extracts different ticket types and their descriptions
- Converts prices from pence to pounds automatically
- Saves pricing data to `ticket_prices.csv`
- Example usage:
  ```bash
  python scrapePrices.py
  # Output: ticket_prices.csv
  ```

---

## Requirements

- Python 3.7+
- `requests`, `beautifulsoup4`, `csv`, and `json` libraries
  ```bash
  pip install requests beautifulsoup4
  ```
- A [Scrape.do API token](https://dashboard.scrape.do/signup) (free 1000 credits/month)

---

## Setup & Step-by-Step Usage

1. **Register for a Scrape.do API token** and replace `<your-token>` in both scripts.

2. **Configure cinema and date settings in `scrapeScreenings.py`:**
   ```python
   cinema_name = "aberdeen-union-square"  # Cinema URL name
   cinema_id = "074"                      # Cinema ID
   start_date = "2025-09-04"             # Start date (YYYY-MM-DD)
   end_date = "2025-09-08"               # End date (YYYY-MM-DD)
   ```

3. **Run the screenings scraper first:**
   ```bash
   python scrapeScreenings.py
   ```

4. **Then run the prices scraper:**
   ```bash
   python scrapePrices.py
   ```

5. **Check the output files:**
   - `screenings.json`: Complete screening data
   - `ticket_prices.csv`: Ticket prices for all screenings

---

## Finding Cinema Information

To scrape a different Cineworld cinema:

1. Visit the [Cineworld website](https://www.cineworld.co.uk/cinemas)
2. Navigate to your desired cinema page
3. Extract the cinema name and ID from the URL:
   ```
   https://www.cineworld.co.uk/cinemas/aberdeen-union-square/074
   
   cinema_name = "aberdeen-union-square"
   cinema_id = "074"
   ```

---

## Troubleshooting & Tips

- **403 or 429 errors:**
  - Make sure your Scrape.do token is valid and you have credits left
  - Double-check that the cinema ID and name are correct

- **Empty screening data:**
  - Ensure the date range includes days when the cinema is open
  - Some cinemas may not show listings far in advance

- **Missing price data:**
  - Run `scrapeScreenings.py` first to generate the required `screenings.json` file
  - Ensure all screenings have valid session IDs

---

## Legal & Ethical Notes

- Only scrape publicly accessible data and respect Cineworld's terms of service
- Do not automate excessive requests or use scraped data for commercial purposes without permission
- Scrape.do handles proxies, headers, and anti-bot solutions for you, but always use scraping responsibly

---

## Why Use Scrape.do?

- Rotating premium proxies & geo-targeting
- Built-in header spoofing and browser fingerprinting
- Handles redirects, CAPTCHAs, and JavaScript rendering
- 1000 free credits/month

[Get your free API token here](https://dashboard.scrape.do/signup)
