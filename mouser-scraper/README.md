# Mouser Scraper

This folder includes a scraper for Mouser.com electronic components using Python `requests` and [Scrape.do](https://scrape.do) for bypassing Mouser's Akamai protection with US geo-targeting and JavaScript rendering.

[Find extended technical guide here. 📘](https://scrape.do/blog/mouser-scraping/)

## What's Included

### Product Information Scraper
* `scrapeProductInfo.py`: Scrapes electronic component information from Mouser category pages including product names and pricing with US geo-targeting and full JavaScript rendering.

## Requirements

* Python 3.7+
* `requests` library<br>Install with:<br>`pip install requests`
* `beautifulsoup4` library<br>Install with:<br>`pip install beautifulsoup4`
* A [Scrape.do API token](https://dashboard.scrape.do/signup) for accessing Mouser bypassing Akamai protection (free 1000 credits/month)

## How to Use: `scrapeProductInfo.py`

1. Copy the full category URL from Mouser, example:<br>`https://www.mouser.com/c/optoelectronics/led-lighting/led-bulbs-modules/`

2. In the script, replace:

   ```python
   token = "<your_token>"
   target_url = urllib.parse.quote_plus("<target_category_url>")
   ```

3. Run the script:

   ```bash
   python scrapeProductInfo.py
   ```

The script will display product information in the console:

```yaml
Product Name: LED MODULE 3W WARM WHITE 3000K
Product Price: $12.45
```

## Technical Details

### Data Extraction Method
- **Product name**: Targets `td.column.desc-column.hide-xsmall span` element
- **Price extraction**: Uses specific ID `lblPrice_1_1` for first product pricing
- **US geo-targeting**: Uses `geoCode=us` parameter for regional access
- **Category page scraping**: Extracts first product from category listings

### API Configuration
- `render=true`: **JavaScript rendering required for Akamai bypass**
- `geoCode=us`: **US geo-targeting (REQUIRED)**

### Protection Bypass
Mouser uses **Akamai** protection that is automatically bypassed using Scrape.do's premium proxy network and JavaScript rendering capabilities for anti-bot detection evasion.

## Common Errors

**403 or 429:** Akamai protection triggered; JavaScript rendering via `render=true` required<br>**US geo-targeting needed:** Content only accessible from US via `geoCode=us`<br>**JavaScript rendering required:** Category pages need full rendering for dynamic content<br>**Element not found:** Product listings may vary or be dynamically loaded

## Why Use Scrape.do?

- Rotating premium proxies & geo-targeting
- Built-in header spoofing
- Handles redirects, CAPTCHAs, and JavaScript rendering
- **Bypasses Akamai protection**
- **US geo-targeting capabilities**
- **Electronics distributor expertise**
- 1000 free credits/month

[Get your free API token here](https://dashboard.scrape.do/signup)