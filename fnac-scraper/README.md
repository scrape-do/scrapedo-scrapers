# Fnac Scraper

This folder includes a scraper for Fnac.com French retail products using Python `requests` and [Scrape.do](https://scrape.do) for bypassing Fnac's custom WAF and aggressive rate-limiting with French geo-targeting and premium routing.

[Find extended technical guide here. 📘](https://scrape.do/blog/fnac-scraping/)

## What's Included

### Product Information Scraper
* `scrapeProductInfo.py`: Scrapes detailed product information from Fnac listings including product name and pricing with French geo-targeting and premium proxy routing.

## Requirements

* Python 3.7+
* `requests` library<br>Install with:<br>`pip install requests`
* `beautifulsoup4` library<br>Install with:<br>`pip install beautifulsoup4`
* A [Scrape.do API token](https://dashboard.scrape.do/signup) for accessing Fnac bypassing custom WAF protection (free 1000 credits/month)

## How to Use: `scrapeProductInfo.py`

1. Copy the full product URL from Fnac, example:<br>`https://www.fnac.com/Apple-iPhone-16-Pro-Max-6-9-5G-256-Go-Double-SIM-Noir-Titane/a17312773/w-4`

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
Product Name: Apple iPhone 16 Pro Max 6,9" 5G 256 Go Double SIM Noir Titane
Product Price: 1 479,00€
```

## Technical Details

### Data Extraction Method
- **Product name**: Targets `h1` header element
- **Price extraction**: Uses specific class `f-faPriceBox__price userPrice checked`
- **French geo-targeting**: Uses `geoCode=fr` parameter for regional access
- **Premium routing**: Uses `super=true` for advanced protection bypass

### API Configuration
- `render=true`: **JavaScript rendering required for dynamic content**
- `geoCode=fr`: **French geo-targeting (REQUIRED)**
- `super=true`: **Premium routing for WAF and rate-limit bypass**

### Protection Bypass
Fnac uses **custom WAF** (Web Application Firewall) and **aggressive rate-limiting** that are automatically bypassed using Scrape.do's premium proxy network and advanced anti-bot detection evasion.

## Common Errors

**403 or 429:** Custom WAF or rate-limiting triggered; premium routing via `super=true` required<br>**Rate-limiting errors:** Aggressive rate-limiting bypassed through premium proxy rotation<br>**French geo-targeting needed:** Content only accessible from France via `geoCode=fr`<br>**JavaScript rendering required:** Product pages need full rendering for dynamic pricing

## Why Use Scrape.do?

- Rotating premium proxies & geo-targeting
- Built-in header spoofing
- Handles redirects, CAPTCHAs, and JavaScript rendering
- **Bypasses custom WAF protection**
- **Overcomes aggressive rate-limiting**
- **French geo-targeting capabilities**
- 1000 free credits/month

[Get your free API token here](https://dashboard.scrape.do/signup)