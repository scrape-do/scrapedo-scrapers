# AutoScout24 Scraper

This folder includes a scraper for AutoScout24.ch car listings using Python `requests` and [Scrape.do](https://scrape.do) for bypassing AutoScout24's Akamai bot protection and JavaScript challenges with Swiss geo-targeting.

[Find extended technical guide here. 📘](https://scrape.do/blog/autoscout24-scraping/)

## What's Included

### Car Information Scraper
* `scrapeCarInfo.py`: Scrapes detailed car information from AutoScout24 listings including car name and pricing with Swiss geo-targeting and full JavaScript rendering.

## Requirements

* Python 3.7+
* `requests` library<br>Install with:<br>`pip install requests`
* `beautifulsoup4` library<br>Install with:<br>`pip install beautifulsoup4`
* A [Scrape.do API token](https://dashboard.scrape.do/signup) for accessing AutoScout24 bypassing Akamai protection (free 1000 credits/month)

## How to Use: `scrapeCarInfo.py`

1. Copy the full car listing URL from AutoScout24, example:<br>`https://www.autoscout24.ch/de/d/porsche-911-coupe-38-turbo-pdk-12188643`

2. In the script, replace:

   ```python
   token = "<your_token>"
   target_url = urllib.parse.quote_plus("<target_car_url>")
   ```

3. Run the script:

   ```bash
   python scrapeCarInfo.py
   ```

The script will display car information in the console:

```yaml
Car Name: Porsche 911 Coupé 3.8 Turbo PDK
Car Price: CHF 89'500
```

## Technical Details

### Data Extraction Method
- **Car name**: Targets `h1` header element
- **Price extraction**: Uses regex pattern `CHF\s([\d'.,]+)` on full page text
- **Swiss geo-targeting**: Uses `geoCode=ch` parameter for regional access
- **Currency handling**: Extracts Swiss Franc (CHF) pricing with local formatting

### API Configuration
- `render=true`: **JavaScript rendering required for Akamai challenges**
- `geoCode=ch`: **Swiss geo-targeting (REQUIRED)**

### Protection Bypass
AutoScout24 uses **Akamai bot protection** with **JavaScript challenges** that are automatically bypassed using Scrape.do's premium proxy network and advanced anti-bot detection evasion.

## Common Errors

**403 or 429:** Akamai bot protection triggered; Scrape.do automatically handles JS challenges<br>**JavaScript rendering required:** Car pages need `render=true` for Akamai challenge completion<br>**Swiss geo-targeting needed:** Content only accessible from Switzerland via `geoCode=ch`<br>**Price not found:** Regex pattern may need adjustment for different price formats

## Supported Vehicle Types

This scraper works with all AutoScout24 vehicle categories including:
- Cars and sedans
- SUVs and crossovers
- Motorcycles and scooters
- Commercial vehicles
- Classic and vintage cars

---

## Why Use Scrape.do?

- Rotating premium proxies & geo-targeting
- Built-in header spoofing
- Handles redirects, CAPTCHAs, and JavaScript rendering
- **Bypasses Akamai bot protection and JS challenges**
- **Swiss geo-targeting capabilities**
- **Advanced anti-bot detection evasion**
- 1000 free credits/month

[Get your free API token here](https://dashboard.scrape.do/signup)