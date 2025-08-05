# MSC Direct Scraper

This folder includes a scraper for MSC Direct industrial supply products using Python `requests` and [Scrape.do](https://scrape.do) for bypassing MSC Direct's Incapsula Imperva protection and geo-restrictions using premium proxies.

[Find extended technical guide here. 📘](https://scrape.do/blog/mscdirect-scraping/)

## What's Included

### Product Information Scraper
* `scrapeProductInfo.py`: Scrapes detailed product information from MSC Direct product pages including brand, name, pricing, and stock availability.

## Requirements

* Python 3.7+
* `requests` library<br>Install with:<br>`pip install requests`
* `beautifulsoup4` library<br>Install with:<br>`pip install beautifulsoup4`
* A [Scrape.do API token](https://dashboard.scrape.do/signup) for accessing MSC Direct bypassing Incapsula Imperva protection (free 1000 credits/month)

## How to Use: `scrapeProductInfo.py`

1. Find the MSC product number from any MSC Direct product URL, example:<br>`https://www.mscdirect.com/product/details/53546172` (MSC# is `53546172`)

2. In the script, replace:

   ```python
   token = "<your_token>"
   msc_number = "<msc_product_number>"
   ```

3. Run the script:

   ```bash
   python scrapeProductInfo.py
   ```

The script will display product information in the console:

```yaml
Brand: STARRETT
Product Name: Starrett 18" Steel Rule with Graduations
Price: $12.45
Stock Status: In Stock
```

## Technical Details

### Data Extraction Method
The scraper uses HTML element IDs to extract product information from MSC Direct product pages:

- **Brand extraction**: Uses `id="brand-name"` element
- **Product name**: Targets `h1` header element
- **Price parsing**: Uses `id="webPriceId"` and removes "ea." suffix
- **Stock detection**: Checks `id="availabilityHtml"` for "In Stock" text
- **URL construction**: Builds URLs using MSC product numbers

### Element Selectors Used
- Brand name: `#brand-name`
- Product title: `h1`
- Price: `#webPriceId`
- Availability: `#availabilityHtml`

### Protection Bypass
MSC Direct uses **Incapsula Imperva** protection and has **geo-restrictions** that are automatically bypassed using Scrape.do's premium proxy network and anti-bot detection evasion.

## Common Errors

**403 or 429:** Incapsula protection triggered; Scrape.do uses residential proxies to bypass this<br>**Geo-restriction errors:** MSC Direct blocks certain regions; `super=true` routing handles this automatically<br>**Element not found:** Product may not exist or page structure changed<br>**Price parsing issues:** Some products may have different pricing formats<br>**Stock status detection:** Availability text may vary for different product types

## Output Format

The script outputs key product information directly to console for quick industrial supply sourcing and price checking.

## Supported Product Types

This scraper works with all MSC Direct product categories including:
- Cutting tools and inserts
- Measuring and inspection tools
- Safety equipment
- Fasteners and hardware
- Industrial supplies
- Machinery and equipment
- Hand tools and power tools

## MSC Product Number Format

MSC Direct uses unique product numbers (MSC#) that can be found in:
- Product URLs: `/product/details/{msc_number}`
- Product pages and catalogs
- Part number references
- Search results

---

## Why Use Scrape.do?

- Rotating premium proxies & geo-targeting
- Built-in header spoofing
- Handles redirects, CAPTCHAs, and JavaScript rendering
- **Bypasses Incapsula Imperva protection**
- **Overcomes geo-restrictions automatically**
- 1000 free credits/month

[Get your free API token here](https://dashboard.scrape.do/signup)