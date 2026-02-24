# SearchPeopleFree Scraper

This folder includes a scraper for SearchPeopleFree.com people lookup using Python `requests` and [Scrape.do](https://scrape.do) for bypassing SearchPeopleFree's dual-layer protection systems (DataDome + Cloudflare) using premium US residential proxies.

[Find extended technical guide here. 📘](https://scrape.do/blog/search-people-free-scraping/)

## What's Included

### Person Information Scraper
* `scrapePersonInfo.py`: Scrapes detailed person information from SearchPeopleFree profile pages including name, exact age, address, ZIP code, phone numbers, email addresses, spouse, and family members.

## Requirements

* Python 3.7+
* `requests` library<br>Install with:<br>`pip install requests`
* `beautifulsoup4` library<br>Install with:<br>`pip install beautifulsoup4`
* A [Scrape.do API token](https://dashboard.scrape.do/signup) for accessing SearchPeopleFree bypassing its protection systems (free 1000 credits/month)

## How to Use: `scrapePersonInfo.py`

1. Copy the full person profile URL from SearchPeopleFree, example:<br>`https://www.searchpeoplefree.com/find/john-smith/abc123`

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
Name: Rick Sanchez
Age: 70
Address: 312 Portal Way
City: Seattle
State: WA
ZIP: 98101
Phone: (206) 555-0242
Email: rsanchez@dimensionc137.com
Spouse: Diane Sanchez
Family: Morty C Smith, Beth Sanchez, Summer Sanchez, Birdperson Phoenixson, Amy Lee Withrow
```

## Technical Details

### Data Extraction Method
The scraper uses a combination of JSON-LD structured data and HTML element selectors to extract person information:

- **Name, phone, email, address**: Extracted from JSON-LD `Person` schema in `<script type="application/ld+json">` blocks
- **Age**: Regex on `article.current-bg` HTML element (age is not included in JSON-LD)
- **Spouse and family**: Parsed from JSON-LD `spouse` and `relatedTo` arrays of nested Person objects
- **Email bypass**: JSON-LD stores emails in plaintext, bypassing Cloudflare's XOR email obfuscation in HTML
- **US geo-targeting**: Uses `geoCode=us` parameter for residential proxy routing

### Element Selectors Used
- Person data: JSON-LD `@type: "Person"` in `<script type="application/ld+json">`
- Age: `article.current-bg` text content with regex `Age\s+(\d+)`
- Address: JSON-LD `contentLocation.address` object
- Phone/Email: JSON-LD `telephone` and `email` arrays
- Family: JSON-LD `relatedTo` and `spouse` arrays

### Proxy Configuration
The script uses US-based residential proxies (`geoCode=us` + `super=true`) which are essential for accessing SearchPeopleFree. The site enforces dual-layer protection (DataDome + Cloudflare) and strict US geoblocking.

## Common Errors

- **403 or blocked:** Both DataDome and Cloudflare are rejecting the request; requires `super=true` with US residential proxies
- **Empty person object:** Profile may not exist or JSON-LD schema may be missing on that page
- **Missing age:** The `article.current-bg` element may not be present on all profiles
- **No email returned:** Not all profiles have email addresses listed
- **Family list empty:** Some profiles don't include family connections in the JSON-LD data

## Output Format

The script outputs 10 structured fields directly to console:
- Full name, exact age
- Current address with city, state, and ZIP code
- Primary phone number and email address
- Spouse name
- Family members (up to 5)

## Privacy & Legal Considerations

- Only access publicly available information
- Respect privacy and data protection laws
- Use responsibly and ethically
- Do not use for harassment or stalking
- Comply with local regulations regarding personal data

---

## Why Use Scrape.do?

- Rotating premium proxies & US geo-targeting
- Automatic DataDome + Cloudflare dual bypass
- Handles JavaScript rendering and email obfuscation
- 1000 free credits/month

[Get your free API token here](https://dashboard.scrape.do/signup)
