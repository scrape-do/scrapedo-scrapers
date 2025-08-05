# Allegro Scraper

This folder includes a scraper for Allegro.pl (Poland's largest e-commerce platform) using Python `requests` and [Scrape.do](https://scrape.do) for bypassing Allegro's heavy geo-restrictions and JavaScript rendering requirements using premium Polish residential proxies.

[Find extended technical guide here. 📘](https://scrape.do/blog/allegro-scraping/)

## What's Included

### Product Information Scraper
* `scrapeProductInfo.py`: Scrapes detailed product information from Allegro product pages including name, pricing, and customer ratings with Polish geo-targeting.

## Requirements

* Python 3.7+
* `requests` library<br>Install with:<br>`pip install requests`
* `beautifulsoup4` library<br>Install with:<br>`pip install beautifulsoup4`
* A [Scrape.do API token](https://dashboard.scrape.do/signup) for accessing Allegro bypassing geo-restrictions and JS rendering (free 1000 credits/month)

## How to Use: `scrapeProductInfo.py`

1. Copy the full product URL from Allegro, example:<br>`https://allegro.pl/oferta/macbook-air-m2-13-6-16gb-256gb-space-gray-16784193631`

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
Product Name: MacBook Air M2 13.6" 16GB 256GB Space Gray
Product Price: 5999.00
Product Rating: 4.8
```

## Technical Details

### Data Extraction Method
The scraper uses HTML selectors and microdata to extract product information from Allegro product pages:

- **Product name**: Targets `h1` header element
- **Price extraction**: Uses `meta[itemprop="price"]` microdata content
- **Rating extraction**: Uses `span[data-testid="aggregateRatingValue"]` selector
- **Polish geo-targeting**: Uses `geoCode=pl` parameter for accessing Poland-restricted content

### Element Selectors Used
- Product title: `h1`
- Price: `meta[itemprop="price"][content]`
- Rating: `span[data-testid="aggregateRatingValue"]`

### API Configuration
The script uses specific Scrape.do parameters:
- `render=false`: Static HTML parsing (faster performance)
- `geoCode=pl`: **Polish geo-targeting for regional access (REQUIRED)**
- `super=true`: **Premium proxy routing with Polish residential IPs (ESSENTIAL)**

### Protection & Access Requirements
Allegro has **extremely strict geo-restrictions** and requires:
- **Polish residential IP addresses** (provided via `super=true`)
- **Heavy JavaScript rendering** for full content access (some products may need `render=true`)
- **Regional compliance** - content only accessible from Poland

## Common Errors

**403 or 429:** Heavy geo-restrictions triggered; requires Polish residential IPs via `super=true`<br>**Regional access denied:** Allegro blocks non-Polish traffic; `geoCode=pl` with premium routing essential<br>**Missing content:** Some products may require `render=true` for JavaScript-heavy pages<br>**Element not found:** Product may not exist or page structure changed<br>**Price/rating missing:** Microdata format may vary for different product types

## Output Format

The script outputs key product information directly to console for quick Polish e-commerce market analysis and price monitoring.

## Supported Product Types

This scraper works with all Allegro product categories including:
- Electronics and computers
- Fashion and clothing
- Home and garden products
- Automotive parts and accessories
- Books, media, and entertainment
- Sports and outdoor equipment
- Health and beauty products

## Product URL Format

Allegro uses structured URLs with unique offer identifiers:
- Format: `/oferta/product-description-offer-id`
- Example: `/oferta/macbook-air-m2-13-6-16gb-256gb-space-gray-16784193631`
- Polish language product descriptions in URLs

## Geo-Restriction Notice

⚠️ **IMPORTANT**: Allegro.pl is **heavily geo-restricted** and only accessible from Poland. This scraper requires:
- **Premium Scrape.do account** with `super=true` routing
- **Polish residential IP addresses** (automatically provided)
- **Compliance with Polish e-commerce regulations**

---

## Why Use Scrape.do?

- Rotating premium proxies & geo-targeting
- Built-in header spoofing
- Handles redirects, CAPTCHAs, and JavaScript rendering
- **Polish residential IP addresses for geo-restrictions**
- **Heavy JavaScript rendering capabilities**
- **Premium routing for restricted content**
- 1000 free credits/month

[Get your free API token here](https://dashboard.scrape.do/signup)