# FastPeopleSearch Scraper

This folder includes a scraper for FastPeopleSearch.com people lookup using Python `requests` and [Scrape.do](https://scrape.do) for bypassing FastPeopleSearch's protection systems using premium US residential proxies.

[Find extended technical guide here. 📘](https://scrape.do/blog/fast-people-search-scraping/)

## What's Included

### Person Information Scraper
* `scrapePersonInfo.py`: Scrapes detailed person information from FastPeopleSearch profile pages including name, age, address, ZIP code, phone numbers, email addresses, aliases, and relatives.

## Requirements

* Python 3.7+
* `requests` library<br>Install with:<br>`pip install requests`
* `beautifulsoup4` library<br>Install with:<br>`pip install beautifulsoup4`
* A [Scrape.do API token](https://dashboard.scrape.do/signup) for accessing FastPeopleSearch bypassing its protection systems (free 1000 credits/month)

## How to Use: `scrapePersonInfo.py`

1. Copy the full person profile URL from FastPeopleSearch, example:<br>`https://www.fastpeoplesearch.com/john-doe`

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
Name: John Doe
Age: 47
Address: 756 E 91st St
City: Chicago
State: IL (Illinois)
ZIP: 60601
Phone: (312) 555-0199
Email: johndoe@example.com
Aliases: John A Doe, John Anthony Doe, Johnny Doe
Relatives: Mary Doe, Robert Smith, Emily Doe, Thomas Doe, Sarah Johnson
```

## Technical Details

### Data Extraction Method
The scraper uses a combination of HTML element selectors and JSON-LD structured data to extract person information:

- **Name and location**: Parsed from `h1#details-header`, split on "in" to separate name from city/state
- **Age**: Extracted from `h2#age-header` with "Age " prefix removed
- **Address**: First text line from `div#current_address_section` anchor element
- **ZIP code**: Extracted from JSON-LD `Person.homeLocation.address.postalCode`
- **Phone numbers and aliases**: Extracted from JSON-LD `Person.telephone` and `Person.additionalName` arrays
- **Relatives**: Parsed from JSON-LD `Person.relatedTo` array of nested Person objects
- **Emails**: Extracted from `FAQPage` JSON-LD block, where email answers contain plaintext addresses (bypasses Cloudflare's XOR email obfuscation in HTML)
- **US geo-targeting**: Uses `geoCode=us` parameter for residential proxy routing

### Element Selectors Used
- Header: `h1#details-header` (name + city/state)
- Age: `h2#age-header`
- Address: `div#current_address_section a`
- Person data: JSON-LD `@type: "Person"` in `<script type="application/ld+json">`
- Email data: JSON-LD `@type: "FAQPage"` in `<script type="application/ld+json">`

### Proxy Configuration
The script uses US-based residential proxies (`geoCode=us` + `super=true`) which are essential for accessing FastPeopleSearch. The site enforces US geoblocking and Cloudflare protection that blocks datacenter IPs.

## Common Errors

- **403 or blocked:** Your IP is being rejected; requires US residential proxies via `geoCode=us` and `super=true`
- **Split error on header:** Profile page may not contain the expected "Name in City, State" format
- **Missing JSON-LD:** Some profiles may not include `Person` or `FAQPage` structured data blocks
- **Empty email list:** Not all profiles have a FAQ section with email addresses
- **No current address:** Some profiles may not have a `current_address_section` element

## Output Format

The script outputs 10 structured fields directly to console:
- Full name, exact age
- Current address with city, state, and ZIP code
- Primary phone number and email address
- Known aliases (up to 5)
- Relatives (up to 5)

## Privacy & Legal Considerations

- Only access publicly available information
- Respect privacy and data protection laws
- Use responsibly and ethically
- Do not use for harassment or stalking
- Comply with local regulations regarding personal data

---

## Why Use Scrape.do?

- Rotating premium proxies & US geo-targeting
- Automatic Cloudflare bypass with browser emulation
- Handles JavaScript rendering and CAPTCHAs
- 1000 free credits/month

[Get your free API token here](https://dashboard.scrape.do/signup)
