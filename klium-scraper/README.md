# Klium Scraper

This folder includes a scraper for Klium.com tools and equipment using Python `requests` and [Scrape.do](https://scrape.do) for bypassing Klium's Cloudflare protection using premium proxies.

[Find extended technical guide here. 📘](https://scrape.do/blog/klium-scraping/)

## What's Included

### Product Information Scraper
* `scrapeProductInfo.py`: Scrapes detailed product information from Klium product pages including name, pricing, and stock availability with intelligent stock detection.

## Requirements

* Python 3.7+
* `requests` library<br>Install with:<br>`pip install requests`
* `beautifulsoup4` library<br>Install with:<br>`pip install beautifulsoup4`
* A [Scrape.do API token](https://dashboard.scrape.do/signup) for accessing Klium bypassing Cloudflare protection (free 1000 credits/month)

## How to Use: `scrapeProductInfo.py`

1. Copy the full product URL from Klium, example:<br>`https://www.klium.com/en/bosch-gbh-2-28-f-rotary-hammer-with-sds-plus-880-w-in-case-0611267600-121096`

2. In the script, replace:

   ```python
   token = "<your_token>"
   target_url = "<target_product_url>"
   ```

3. Run the script:

   ```bash
   python scrapeProductInfo.py
   ```

The script will display product information in the console:

```yaml
Product Name: Bosch GBH 2-28 F Rotary Hammer with SDS-Plus 880 W in Case
Price: €189.99
Stock Availability: 5 in stock
```

## Technical Details

### Data Extraction Method
The scraper uses HTML selectors and regex patterns to extract product information from Klium product pages:

- **Product name**: Targets `h1` header element
- **Price extraction**: Uses `span.current-price-value` content attribute
- **Stock detection**: Intelligent regex parsing of page text for stock quantities
- **Cloudflare bypass**: Automatic handling through Scrape.do's proxy network

### Element Selectors Used
- Product title: `h1`
- Price: `span.current-price-value[content]`
- Stock text: Full page text parsing with regex

### Stock Detection Logic
The script uses smart regex patterns to detect various stock formats:
- **Specific quantities**: "we have X products in stock" → "X in stock"
- **General availability**: "in stock" text → "In stock"
- **Default fallback**: No stock indicators → "Out of stock"

### Protection Bypass
Klium uses **Cloudflare** protection that is automatically bypassed using Scrape.do's proxy network and anti-bot detection evasion.

## Common Errors

**403 or 429:** Cloudflare protection triggered; Scrape.do automatically handles this<br>**Element not found:** Product may not exist or page structure changed<br>**Price parsing issues:** Some products may have different pricing formats<br>**Stock detection failure:** Regex pattern may need adjustment for new stock text formats<br>**Content attribute missing:** Price element structure may have changed

## Output Format

The script outputs key product information directly to console for quick tool sourcing and price comparison.

## Supported Product Types

This scraper works with all Klium product categories including:
- Power tools and equipment
- Hand tools
- Measuring instruments
- Safety equipment
- Workshop accessories
- Construction tools
- Professional equipment

## Product URL Format

Klium uses descriptive URLs with product codes:
- Format: `/en/{product-description}-{product-code}`
- Example: `/en/bosch-gbh-2-28-f-rotary-hammer-with-sds-plus-880-w-in-case-0611267600-121096`
- Multi-language support (EN, FR, etc.)

---

## Why Use Scrape.do?

- Rotating premium proxies & geo-targeting
- Built-in header spoofing
- Handles redirects, CAPTCHAs, and JavaScript rendering
- **Bypasses Cloudflare protection automatically**
- **Professional tool supplier access**
- 1000 free credits/month

[Get your free API token here](https://dashboard.scrape.do/signup)