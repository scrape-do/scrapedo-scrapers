# TruePeopleSearch Scraper

This folder includes a scraper for TruePeopleSearch.com people lookup using Python `requests` and [Scrape.do](https://scrape.do) for bypassing TruePeopleSearch's protection systems using premium US residential proxies.

[Find extended technical guide here. 📘](https://scrape.do/blog/true-people-search-scraping/)

## What's Included

### Person Information Scraper
* `scrapePersonInfo.py`: Scrapes detailed person information from TruePeopleSearch profile pages including name, age, address, ZIP code, phone numbers, email addresses, aliases, and relatives.

## Requirements

* Python 3.7+
* `requests` library<br>Install with:<br>`pip install requests`
* `beautifulsoup4` library<br>Install with:<br>`pip install beautifulsoup4`
* A [Scrape.do API token](https://dashboard.scrape.do/signup) for accessing TruePeopleSearch bypassing its protection systems (free 1000 credits/month)

## How to Use: `scrapePersonInfo.py`

1. Copy the full person profile URL from TruePeopleSearch, example:<br>`https://www.truepeoplesearch.com/find/person/jane-doe`

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
Name: Jane Doe
Age: 23
Address: 2912 Northern Ave WE
City: Washington
State: DC
ZIP: 20001
Phone: (202) 555-5555
Email: janedoe@example.com
Aliases: Jane Marie Doe, Jane D Smith
Relatives: John Doe, Mary Doe, Robert Smith, Emily Doe, Thomas Doe
```

## Technical Details

### Data Extraction Method
The scraper uses a combination of HTML data attributes and JSON-LD structured data to extract person information:

- **Name and age**: Extracted from `data-fn`, `data-ln`, and `data-age` attributes on `div#personDetails`
- **Address, ZIP, phone, email**: Parsed from `ProfilePage` JSON-LD schema via `mainEntity` Person object
- **Aliases**: Extracted from JSON-LD `alternateName` array
- **Relatives**: Extracted from JSON-LD `relatedTo` array of nested Person objects
- **US geo-targeting**: Uses `geoCode=us` parameter for residential proxy routing

### Element Selectors Used
- Person details: `div#personDetails` with `data-fn`, `data-ln`, `data-age` attributes
- JSON-LD: `<script type="application/ld+json">` with `@type: "ProfilePage"`
- Address: JSON-LD `mainEntity.address` object
- Phone/Email: JSON-LD `mainEntity.telephone` and `mainEntity.email` arrays
- Aliases: JSON-LD `mainEntity.alternateName` array
- Relatives: JSON-LD `mainEntity.relatedTo` array

### Proxy Configuration
The script uses US-based residential proxies (`geoCode=us` + `super=true`) which are essential for accessing TruePeopleSearch. The site enforces US geoblocking and Cloudflare protection that blocks datacenter IPs.

## Common Errors

- **403 or blocked:** Your IP is being rejected; requires US residential proxies via `geoCode=us` and `super=true`
- **Element not found:** Person profile may not exist or page structure may have changed
- **Missing JSON-LD:** Some profiles may not include the `ProfilePage` structured data block
- **Empty email/phone arrays:** Not all profiles have email addresses or multiple phone numbers listed
- **Data attribute missing:** Profile structure may have changed; verify the page loads correctly

## Output Format

The script outputs 10 structured fields directly to console:
- Full name, exact age
- Current address with city, state, and ZIP code
- Primary phone number and email address
- Known aliases
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
