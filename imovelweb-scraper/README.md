# Imovelweb Scraper

This folder includes a scraper for Imovelweb.com.br real estate listings using Python `requests` and [Scrape.do](https://scrape.do) for bypassing Imovelweb's DataDome protection and JavaScript rendering requirements with Brazilian geo-targeting.

[Find extended technical guide here. 📘](https://scrape.do/blog/imovelweb-scraping/)

## What's Included

### Property Information Scraper
* `scrapePropertyInfo.py`: Scrapes detailed property information from Imovelweb listings including name, square meters, and pricing with Brazilian geo-targeting and full JavaScript rendering.

## Requirements

* Python 3.7+
* `requests` library<br>Install with:<br>`pip install requests`
* `beautifulsoup4` library<br>Install with:<br>`pip install beautifulsoup4`
* A [Scrape.do API token](https://dashboard.scrape.do/signup) for accessing Imovelweb bypassing DataDome protection (free 1000 credits/month)

## How to Use: `scrapePropertyInfo.py`

1. Copy the full property URL from Imovelweb, example:<br>`https://www.imovelweb.com.br/propriedades/casa-no-condominio-east-village-disponivel-para-venda-2986272608.html`

2. In the script, replace:

   ```python
   token = "<your_token>"
   target_url = urllib.parse.quote_plus("<target_property_url>")
   ```

3. Run the script:

   ```bash
   python scrapePropertyInfo.py
   ```

The script will display property information in the console:

```yaml
Listing Name: Casa no Condomínio East Village
Square Meters: 180
Sale Price: R$ 850.000
```

## Technical Details

### Data Extraction Method
- **Property name**: Targets `h1` header element
- **Square meters**: Uses regex pattern `(\d+)\s*m²` on property type heading
- **Price extraction**: Uses regex pattern `R\$\s*[\d.,]+` on price value div
- **Brazilian geo-targeting**: Uses `geoCode=br` parameter for regional access

### API Configuration
- `render=true`: **JavaScript rendering required for dynamic content**
- `geoCode=br`: **Brazilian geo-targeting (REQUIRED)**

### Protection Bypass
Imovelweb uses **DataDome** protection that is automatically bypassed using Scrape.do's premium proxy network and anti-bot detection evasion.

## Common Errors

**403 or 429:** DataDome protection triggered; Scrape.do automatically handles this<br>**JavaScript rendering required:** Property pages need `render=true` for full content access<br>**Brazilian geo-targeting needed:** Content only accessible from Brazil via `geoCode=br`<br>**Regex pattern failures:** Property format may vary for different listing types

## Supported Property Types

This scraper works with all Imovelweb property categories including:
- Houses and condominiums
- Apartments and studios
- Commercial properties
- Land and lots
- New construction projects

---

## Why Use Scrape.do?

- Rotating premium proxies & geo-targeting
- Built-in header spoofing
- Handles redirects, CAPTCHAs, and JavaScript rendering
- **Bypasses DataDome protection**
- **Brazilian geo-targeting capabilities**
- **Full JavaScript rendering support**
- 1000 free credits/month

[Get your free API token here](https://dashboard.scrape.do/signup)