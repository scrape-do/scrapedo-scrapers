# AUTODOC Scraper

This folder includes a scraper for AUTODOC.de automotive parts using Python `requests` and [Scrape.do](https://scrape.do) for bypassing AUTODOC's protection systems using premium proxies and header rotation.

[Find extended technical guide here. 📘](https://scrape.do/blog/autodoc-de-scraping/)

## What's Included

### Product Scraper
* `scrapeProducts.py`: Scrapes detailed product information from AUTODOC.de product pages using structured JSON-LD data and exports to CSV.

## Requirements

* Python 3.7+
* `requests` library<br>Install with:<br>`pip install requests`
* `beautifulsoup4` library<br>Install with:<br>`pip install beautifulsoup4`
* A [Scrape.do API token](https://dashboard.scrape.do/signup) for accessing AUTODOC bypassing its protection systems (free 1000 credits/month)

## How to Use: `scrapeProducts.py`

1. Copy the full product URL from AUTODOC.de, example:<br>`https://www.autodoc.de/reifen/hankook-8808563543369-1029031`

2. In the script, replace:

   ```python
   token = "<your_token>"
   target_url = "<target_product_url>"
   ```

3. Run the script:

   ```bash
   python scrapeProducts.py
   ```

The script will display product information in the console:

```yaml
📋 Product Information:
MPN:                 1029031
SKU:                 8808563543369
Product Name:        HANKOOK Kinergy 4S2 H750
Brand Name:          HANKOOK
Product Description: All-season tire for passenger cars...
Price:               89.99 EUR
Image URLs:          3 image(s)
Availability:        In stock
Seller Name:         AUTODOC
```

A file called `autodoc_product_data.csv` will be created with:

* **MPN** (Manufacturer Part Number)
* **SKU** (Stock Keeping Unit)
* **Product Name**
* **Brand**
* **Description**
* **Price**
* **Currency**
* **Image URLs**
* **Availability**
* **Seller**

## Technical Details

### Data Extraction Method
The scraper uses AUTODOC's structured JSON-LD data embedded in product pages, which provides reliable and comprehensive product information including:

- Product identifiers (MPN, SKU)
- Pricing and availability information
- Product descriptions and specifications
- Brand information
- Multiple product images
- Seller details

### Error Handling
The script includes comprehensive error handling for:
- Network connection issues
- Invalid product URLs
- Missing or malformed JSON-LD data
- File writing permissions

## Common Errors

**403 or 429:** Your IP might be blocked; try using different proxy settings with Scrape.do<br>**Empty product data:** Ensure the URL is a valid AUTODOC product page and the product is publicly available<br>**JSON parsing errors:** The page structure may have changed; verify the product page loads correctly in your browser<br>**File permission errors:** Ensure you have write permissions in the script directory<br>**Missing structured data:** Some product pages may not include JSON-LD data; try with different products

## Output Format

The CSV file contains all extracted product information with UTF-8 encoding to properly handle international characters and product descriptions in multiple languages.

## Supported Product Types

This scraper works with all AUTODOC.de product categories including:
- Tires (reifen)
- Auto parts (autoteile)
- Car accessories
- Oil and fluids
- Tools and equipment
