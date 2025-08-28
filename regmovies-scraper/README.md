# Regmovies Scraper

[Find extended technical guide here 📔](https://scrape.do/blog/regmovies-com-scraping/)

This repository provides Python scripts to extract movie screenings and ticket prices from regmovies.com (Regal Cinemas) using [Scrape.do](https://scrape.do) to bypass heavy Cloudflare protection and geo-restrictions.

The tools here let you:
- Scrape movie screenings from any Regal cinema across multiple dates
- Extract ticket prices for different ticket types (adult, child, senior, etc.)
- Handle US geo-restrictions and Cloudflare challenges automatically
- Save results to JSON and CSV for easy analysis

All scripts use Python 3.7+, the `requests` library, and direct API access to Regal's backend endpoints.

---

## What's Included

### 1. `scrapeScreenings.py`
**Scrapes movie screenings from Regal Cinemas for a specified date range.**

- Accesses Regal's backend API directly to extract screening data
- Extracts movie names, showtimes, dates, and internal performance IDs
- Supports multiple-day scraping with MM-DD-YYYY date format
- Saves comprehensive screening data to `screenings.json`
- Example usage:
  ```bash
  python scrapeScreenings.py
  # Output: screenings.json
  ```

### 2. `scrapePrices.py`
**Extracts ticket prices for all screenings from the `screenings.json` file.**

- Creates order sessions for each screening to access pricing data
- Uses performance IDs from `scrapeScreenings.py` to fetch ticket pricing
- Extracts different ticket types and their descriptions
- Converts prices from cents to USD automatically
- Saves pricing data to `ticket_prices.csv`
- Example usage:
  ```bash
  python scrapePrices.py
  # Output: ticket_prices.csv
  ```

---

## Requirements

- Python 3.7+
- `requests`, `csv`, and `json` libraries
  ```bash
  pip install requests
  ```
- A [Scrape.do API token](https://dashboard.scrape.do/signup) (free 1000 credits/month)

---

## Setup & Step-by-Step Usage

1. **Register for a Scrape.do API token** and replace `<your-token>` in both scripts.

2. **Configure cinema and date settings in `scrapeScreenings.py`:**
   ```python
   cinema_id = "0147"                    # Regal cinema ID
   cinema_name = "Regal Village Park"    # Cinema name
   start_date = "10-07-2025"            # Start date (MM-DD-YYYY)
   end_date = "10-09-2025"              # End date (MM-DD-YYYY)
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

To scrape a different Regal cinema:

1. Visit the [Regal Cinemas website](https://www.regmovies.com/theatres)
2. Navigate to your desired cinema page
3. Extract the cinema ID from the URL:
   ```
   https://www.regmovies.com/theatres/regal-village-park-0147
   
   cinema_id = "0147"  # Last 4 digits
   cinema_name = "Regal Village Park"
   ```

---

## Troubleshooting & Tips

- **403 or 429 errors:**
  - Make sure your Scrape.do token is valid and you have credits left
  - Ensure you're using `geoCode=us` for US-based requests

- **Empty screening data:**
  - Verify the cinema ID is correct (last 4 digits from the cinema URL)
  - Check that the date range includes days when the cinema is open

- **Missing price data:**
  - Run `scrapeScreenings.py` first to generate the required `screenings.json` file
  - Ensure all screenings have valid performance IDs

- **Geo-restriction errors:**
  - Scrape.do automatically handles US geo-restrictions
  - Double-check that `geoCode=us` is included in your API calls

---

## Legal & Ethical Notes

- Only scrape publicly accessible data and respect Regal's terms of service
- Do not automate excessive requests or use scraped data for commercial purposes without permission
- Scrape.do handles proxies, headers, and anti-bot solutions for you, but always use scraping responsibly

---

## Why Use Scrape.do?

- Rotating premium proxies & geo-targeting
- Built-in header spoofing and browser fingerprinting
- Handles redirects, CAPTCHAs, and JavaScript rendering
- 1000 free credits/month

[Get your free API token here](https://dashboard.scrape.do/signup)
