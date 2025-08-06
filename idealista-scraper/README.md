# Idealista Scraper

This folder includes scrapers for Idealista.com Spanish real estate listings using Python `requests` and [Scrape.do](https://scrape.do) for bypassing Idealista's protection systems with Spanish geo-targeting, JavaScript rendering, and comprehensive data extraction.

[Find extended technical guide here. 📘](https://scrape.do/blog/idealista-scraping/)

## What's Included

### Individual Property Scraper
* `listingData.py`: Scrapes detailed property information from individual Idealista listing pages including price, location, features, advertiser details, and property specifications with Spanish geo-targeting.

### Region/Search Results Scraper
* `regionSearch.py`: Scrapes multiple property listings from Idealista search result pages with automatic pagination, extracts key property data, and exports to CSV format for bulk data collection.

### Phone Number Extraction (⚠️ GDPR RESTRICTED)
* `phoneNumbers.py`: **PHONE NUMBERS ARE PERSONAL DATA UNDER GDPR (EU) - FOR PERSONAL USE ONLY** - Extracts phone numbers from property listings using browser automation. **STRICTLY PROHIBITED for commercial use.**

## Requirements

* Python 3.7+
* `requests` library<br>Install with:<br>`pip install requests`
* `beautifulsoup4` library<br>Install with:<br>`pip install beautifulsoup4`
* A [Scrape.do API token](https://dashboard.scrape.do/signup) for accessing Idealista bypassing Spanish geo-restrictions and anti-bot protection (free 1000 credits/month)

## How to Use: `listingData.py`

1. Copy the full property URL from Idealista, example:<br>`https://www.idealista.com/inmueble/107795847/`

2. In the script, replace:

   ```python
   token = "<your_token>"
   target_url = urllib.parse.quote_plus("<target_property_url>")
   ```

3. Run the script:

   ```bash
   python listingData.py
   ```

The script will display comprehensive property information in the console:

```yaml
Property Type: Casa o chalet independiente
For: en venta
Square Size: 300 m²
Bedroom Count: 4 hab.
Neighborhood: Bernabéu-Hispanoamérica
City: Madrid
Full Address: Avenida del Levante, Barrio Bernabéu-Hispanoamérica, Distrito Chamartín, Madrid, Madrid capital, Madrid
Last Updated Days: 21
Advertiser Name: Engel & Völkers Madrid
Price: 1.850.000 €
```

## How to Use: `regionSearch.py`

1. Copy the search URL from Idealista, example:<br>`https://www.idealista.com/venta-viviendas/madrid-madrid/`

2. In the script, replace:

   ```python
   token = "<your_token>"
   base_url = "<target_search_url>"
   ```

3. Run the script:

   ```bash
   python regionSearch.py
   ```

The script will automatically:
- Scrape all pages of search results
- Extract property data from each listing
- Save results to `idealista_properties.csv`

```yaml
Scraping page 1...
Found 20 listings on page 1
Scraping page 2...
Found 18 listings on page 2
...
Scraping complete! Found 271 total properties.
Data saved to idealista_properties.csv
```

## How to Use: `phoneNumbers.py`

### ⚠️ LEGAL REQUIREMENTS BEFORE USAGE:
- ✅ **Confirm personal, non-commercial use only**
- ✅ **Read and understand GDPR implications**
- ✅ **Verify compliance with local privacy laws**
- ✅ **Respect individual privacy rights**

### Usage Instructions:

1. **Replace configuration variables:**
   ```python
   TOKEN = "<your-scrape-do-token>"
   TARGET_URL = "<target-property-url>"  # e.g. https://www.idealista.com/inmueble/108889120/
   ```

2. **Run the script:**
   ```bash
   python phoneNumbers.py
   ```

3. **Expected output:**
   ```yaml
   Property Title: Casa o chalet independiente en venta en Carretera de la Costa s/n, Tijarafe
   Price: 245.000 €
   Phone Number: +34[REDACTED]
   ```

## Technical Details

### API Configuration
- `render=true`: **JavaScript rendering required for dynamic content**
- `geoCode=es`: **Spanish geo-targeting (REQUIRED)**
- `super=true`: **Premium routing for enhanced protection bypass**

### Protection Bypass
Idealista uses **DataDome anti-bot protection**, **back-to-back CAPTCHAs**, and **geo-restrictions** that are automatically bypassed using Scrape.do's premium proxy network with Spanish IP addresses and JavaScript rendering capabilities.

### Common Errors

**403 or 429:** DataDome protection or back-to-back CAPTCHAs triggered; premium routing via `super=true` required<br>**Spanish geo-targeting needed:** Content only accessible from Spain via `geoCode=es`<br>**JavaScript rendering required:** Property pages need full rendering for dynamic content<br>**CAPTCHA challenges:** DataDome may present multiple CAPTCHAs; automatic bypass via premium routing<br>**Element not found:** Property may not exist or page structure changed<br>**No listings found:** Search results page may be empty or pagination ended<br>**⚠️ GDPR Violation:** Using phone extraction for commercial purposes - **ILLEGAL UNDER EU LAW**<br>**⚠️ Privacy Law Breach:** Bulk phone number extraction - **MASSIVE FINES POSSIBLE**

## Why Use Scrape.do?

- Rotating premium proxies & geo-targeting
- Built-in header spoofing
- Handles redirects, CAPTCHAs, and JavaScript rendering
- **Bypasses DataDome anti-bot protection**
- **Automatic CAPTCHA solving for back-to-back challenges**
- **Spanish geo-targeting capabilities**
- **Real estate marketplace expertise**
- **Automatic pagination handling**
- 1000 free credits/month

[Get your free API token here](https://dashboard.scrape.do/signup)