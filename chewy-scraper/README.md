# Chewy Scraper

This folder includes a scraper for Chewy.com pet products using Python `requests` and [Scrape.do](https://scrape.do) for bypassing Chewy's Akamai protection with US geo-targeting, JavaScript rendering, and CSV export functionality.

[Find extended technical guide here. 📘](https://scrape.do/blog/chewy-scraping/)

## What's Included

### Product Information Scraper
* `scrapeProductInfo.py`: Scrapes pet product information from Chewy including product names and pricing with US geo-targeting, full JavaScript rendering, and automatic CSV export.

## Requirements

* Python 3.7+
* `requests` library<br>Install with:<br>`pip install requests`
* `beautifulsoup4` library<br>Install with:<br>`pip install beautifulsoup4`
* A [Scrape.do API token](https://dashboard.scrape.do/signup) for accessing Chewy bypassing Akamai protection (free 1000 credits/month)

## How to Use: `scrapeProductInfo.py`

1. Copy the full product URL from Chewy, example:<br>`https://www.chewy.com/purina-pro-plan-shredded-blend-adult/dp/114030`

2. In the script, replace:

   ```python
   token = "<your_token>"
   target_url = urllib.parse.quote_plus("<target_product_url>")
   ```

3. Run the script:

   ```bash
   python scrapeProductInfo.py
   ```

The script will display results and save data to CSV:

```yaml
Data saved to chewy_product_data.csv
```

A file called `chewy_product_data.csv` will be created with:

* **Product Name**
* **Price**

## Technical Details

### Data Extraction Method
- **Product name**: Targets `h1[data-testid="product-title-heading"]` element
- **Price extraction**: Uses `div[data-testid="advertised-price"]` selector
- **US geo-targeting**: Uses `geoCode=us` parameter for regional access
- **CSV export**: Automatic data export with UTF-8 encoding

### API Configuration
- `render=true`: **JavaScript rendering required for Akamai bypass**
- `geoCode=us`: **US geo-targeting (REQUIRED)**
- `super=true`: **Premium routing for enhanced protection bypass**

### Protection Bypass
Chewy uses **Akamai** protection that is automatically bypassed using Scrape.do's premium proxy network and JavaScript rendering capabilities for anti-bot detection evasion.

## Common Errors

**403 or 429:** Akamai protection triggered; JavaScript rendering and premium routing required<br>**US geo-targeting needed:** Content only accessible from US via `geoCode=us`<br>**JavaScript rendering required:** Product pages need full rendering for dynamic content<br>**Element not found:** Product may not exist or data-testid attributes changed

## Supported Product Categories

This scraper works with all Chewy pet product categories including:
- Dog food and treats
- Cat food and supplies
- Fish and aquarium supplies
- Bird and small animal products
- Reptile and farm animal supplies
- Pet health and wellness products

---

## Why Use Scrape.do?

- Rotating premium proxies & geo-targeting
- Built-in header spoofing
- Handles redirects, CAPTCHAs, and JavaScript rendering
- **Bypasses Akamai protection**
- **US geo-targeting capabilities**
- **Pet products marketplace expertise**
- 1000 free credits/month

[Get your free API token here](https://dashboard.scrape.do/signup)