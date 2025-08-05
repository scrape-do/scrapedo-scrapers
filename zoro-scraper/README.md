# Zoro Scraper

This folder includes a scraper for Zoro.com industrial and business supplies using Python `requests` and [Scrape.do](https://scrape.do) for bypassing Zoro's protection systems using premium US proxies and geo-targeting.

[Find extended technical guide here. 📘](https://scrape.do/blog/zoro-scraping/)

## What's Included

### Product Information Scraper
* `scrapeProductInfo.py`: Scrapes detailed product information from Zoro product pages including name, manufacturer number, and pricing with US geo-targeting.

## Requirements

* Python 3.7+
* `requests` library<br>Install with:<br>`pip install requests`
* `beautifulsoup4` library<br>Install with:<br>`pip install beautifulsoup4`
* A [Scrape.do API token](https://dashboard.scrape.do/signup) for accessing Zoro bypassing geo-restrictions (free 1000 credits/month)

## How to Use: `scrapeProductInfo.py`

1. Copy the full product URL from Zoro, example:<br>`https://www.zoro.com/gorilla-glue-30-yds-black-duct-tape-106718/i/G109908549/`

2. In the script, replace:

   ```python
   token = "<your_token>"
   target_url = urllib.parse.quote_plus("<target_product_url>")
   ```

3. Run the script:

   ```bash
   python scrapeProductInfo.py
   ```

The script will display product information in the console:

```yaml
Product Name: Gorilla Glue 30 yds. Black Duct Tape
MFR #: 106718
Product Price: $8.99
```

## Technical Details

### Data Extraction Method
The scraper uses HTML selectors and regex patterns to extract product information from Zoro product pages:

- **Product name**: Targets `h1` header element
- **MFR number extraction**: Uses regex pattern `Mfr\s*#\s*([\w\-/]+)` on product identifiers
- **Price extraction**: Uses `span.currency.text-h2` selector
- **US geo-targeting**: Uses `geoCode=us` parameter for accessing US-restricted content

### Element Selectors Used
- Product title: `h1`
- Product identifiers: `div.product-identifiers`
- Price: `span.currency.text-h2`

### API Configuration
The script uses specific Scrape.do parameters:
- `render=false`: Static HTML parsing (faster performance)
- `geoCode=us`: US geo-targeting for regional access
- `super=true`: Premium proxy routing for reliability

### Protection Bypass
Zoro uses **DataDome WAF** (Web Application Firewall) protection and has **geo-restrictions** that are automatically bypassed using Scrape.do's premium proxy network and anti-bot detection evasion.

### MFR Number Extraction
Uses intelligent regex pattern to extract manufacturer numbers from product identifier text, handling various formats like:
- "Mfr # 106718"
- "Mfr# ABC-123"
- "Mfr #XYZ/456"

## Common Errors

**403 or 429:** DataDome WAF protection triggered; Scrape.do uses premium proxies to bypass this<br>**Geo-restrictions:** Script uses US geo-targeting via `geoCode=us` for regional access<br>**Element not found:** Product may not exist or page structure changed<br>**MFR number not found:** Regex pattern may need adjustment for new identifier formats<br>**Price parsing issues:** Currency formatting may vary for different products

## Output Format

The script outputs key product information directly to console for quick industrial supply sourcing and manufacturer verification.

## Supported Product Types

This scraper works with all Zoro product categories including:
- Industrial tools and equipment
- Safety and security products
- Electrical and lighting supplies
- Plumbing and HVAC materials
- Office and facility supplies
- Cleaning and maintenance products
- Material handling equipment

## Product URL Format

Zoro uses structured URLs with product identifiers:
- Format: `/product-name-mfr/i/internal-id/`
- Example: `/gorilla-glue-30-yds-black-duct-tape-106718/i/G109908549/`
- Contains both MFR number and internal Zoro ID

---

## Why Use Scrape.do?

- Rotating premium proxies & geo-targeting
- Built-in header spoofing
- Handles redirects, CAPTCHAs, and JavaScript rendering
- **Bypasses DataDome WAF protection**
- **US geo-targeting for regional restrictions**
- **Business supply website expertise**
- 1000 free credits/month

[Get your free API token here](https://dashboard.scrape.do/signup)