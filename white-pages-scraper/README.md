# Whitepages Scraper

This folder includes a scraper for Whitepages.com people lookup using Python `requests` and [Scrape.do](https://scrape.do) for bypassing Whitepages' protection systems using premium US residential proxies.

[Find extended technical guide here. 📘](https://scrape.do/blog/white-pages-scraping/)

## What's Included

### Person Information Scraper
* `scrapePersonInfo.py`: Scrapes person information from Whitepages profile pages including name, approximate age range, address, city, state, ZIP code, and primary phone number.

## Requirements

* Python 3.7+
* `requests` library<br>Install with:<br>`pip install requests`
* `beautifulsoup4` library<br>Install with:<br>`pip install beautifulsoup4`
* A [Scrape.do API token](https://dashboard.scrape.do/signup) for accessing Whitepages bypassing its protection systems (free 1000 credits/month)

## How to Use: `scrapePersonInfo.py`

1. Copy the full person profile URL from Whitepages, example:<br>`https://www.whitepages.com/name/John-Doe/New-York-NY/abc123`

2. In the script, replace:

   ```python
   token = "<your_token>"
   target_url = "<target_person_url>"
   ```

3. Run the script:

   ```bash
   python scrapePersonInfo.py
   ```

The script will display person information in the console:

```yaml
Name: Michael G Scott
Age: in their 50s
Address: 1725 Slough Ave
City: Scranton
State: PA
ZIP: 18503
Phone: (570) 555-0100
```

## Technical Details

### Data Extraction Method
The scraper uses a combination of HTML element selectors and JSON-LD structured data to extract person information:

- **Name**: Extracted from `div.big-name` element (Vue.js/Nuxt SSR markup)
- **Address**: Street from `div.address-line1`, city/state/ZIP parsed from `div.address-line2`
- **Phone**: Uses `a[data-qa-selector="phone-number-link"]` attribute selector
- **Age**: Parsed from JSON-LD `Person.description` field (e.g., "Michael G Scott is in their 50s.")
- **US geo-targeting**: Uses `geoCode=us` parameter for residential proxy routing

### Element Selectors Used
- Name: `div.big-name`
- Street address: `div.address-line1`
- City/State/ZIP: `div.address-line2`
- Phone: `a[data-qa-selector="phone-number-link"]`
- Age: JSON-LD `Person.description` field in `<script type="application/ld+json">`

### Proxy Configuration
The script uses US-based residential proxies (`geoCode=us` + `super=true`) which are essential for accessing Whitepages. The site enforces strict geoblocking and Cloudflare Turnstile verification that blocks datacenter IPs.

## Common Errors

- **403 or blocked:** Your IP is being rejected; requires US residential proxies via `geoCode=us` and `super=true`
- **Empty name field:** Profile may not exist, may have been removed, or page structure changed
- **Missing age data:** Whitepages shows approximate age ranges (e.g., "in their 50s") on free profiles; exact ages require premium access
- **No phone number:** Some profiles don't list a primary phone on the free tier
- **ZIP code missing:** Not all profiles include ZIP codes in the address line

## Output Format

The script outputs 7 fields directly to console:
- Full name
- Approximate age range
- Current street address with city, state, and ZIP code
- Primary phone number

## Privacy & Legal Considerations

- Only access publicly available information
- Respect privacy and data protection laws
- Use responsibly and ethically
- Do not use for harassment or stalking
- Comply with local regulations regarding personal data

---

## Why Use Scrape.do?

- Rotating premium proxies & US geo-targeting
- Automatic Cloudflare Turnstile bypass
- Handles JavaScript rendering and browser emulation
- 1000 free credits/month

[Get your free API token here](https://dashboard.scrape.do/signup)
