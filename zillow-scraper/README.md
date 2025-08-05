# Zillow Scraper

This folder includes a scraper for Zillow.com real estate listings using Python `requests` and [Scrape.do](https://scrape.do) for bypassing Zillow's protection systems using premium proxies and header rotation.

[Find extended technical guide here. 📘](https://scrape.do/blog/zillow-scraping/)

## What's Included

### Property Listing Scraper
* `scrapeListingData.py`: Scrapes detailed property information from Zillow listing pages using regex patterns and HTML parsing.

## Requirements

* Python 3.7+
* `requests` library<br>Install with:<br>`pip install requests`
* `beautifulsoup4` library<br>Install with:<br>`pip install beautifulsoup4`
* A [Scrape.do API token](https://dashboard.scrape.do/signup) for accessing Zillow bypassing its protection systems (free 1000 credits/month)

## How to Use: `scrapeListingData.py`

1. Copy the full property URL from Zillow, example:<br>`https://www.zillow.com/homedetails/8926-Silver-City-San-Antonio-TX-78254/124393863_zpid/`

2. In the script, replace:

   ```python
   token = "<your_token>"
   target_url = "<target_property_url>"
   ```

3. Run the script:

   ```bash
   python scrapeListingData.py
   ```

The script will display property information in the console:

```yaml
Price: $245,000
Address: 8926 Silver City
City: San Antonio
State: TX
Days on Zillow: 15
Zestimate: $248,900
```

## Technical Details

### Data Extraction Method
The scraper uses a combination of HTML parsing and regex patterns to extract property information from Zillow listing pages:

- **Price extraction**: Uses data-testid selectors for reliable price detection
- **Address parsing**: Regex pattern to separate street, city, and state components
- **Market metrics**: Extracts "Days on Zillow" and Zestimate values using targeted regex
- **Text processing**: Parses full page text content for comprehensive data extraction

### Regex Patterns Used
- Address pattern: `(\d+\s+[^,]+),\s*([^,]+),\s*(\w{2})\s+\d{5}`
- Days on Zillow: `(\d+)\s+days?\s*on\s+Zillow`
- Zestimate: `\$[\d,]+(?=\s*Zestimate)`

## Common Errors

**403 or 429:** Your IP might be blocked; the script uses `super=true` for premium proxy rotation<br>**Regex match errors:** Property page format may have changed; verify the listing loads correctly in your browser<br>**Missing price data:** Ensure the property is active and publicly listed<br>**Address parsing issues:** Some properties may have non-standard address formats<br>**Days on Zillow not found:** New listings may not have this metric yet

## Supported Property Types

This scraper works with all Zillow property listings including:
- Single-family homes
- Condominiums
- Townhouses
- Multi-family properties
- Land listings
- New construction

## Output Format

The script outputs key property metrics directly to console for quick analysis and integration into other systems.

---

## Why Use Scrape.do?

- Rotating premium proxies & geo-targeting
- Built-in header spoofing
- Handles redirects, CAPTCHAs, and JavaScript rendering
- 1000 free credits/month

[Get your free API token here](https://dashboard.scrape.do/signup)