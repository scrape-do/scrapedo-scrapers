# TruePeopleSearch Scraper

This folder includes a scraper for TruePeopleSearch.com people lookup using Python `requests` and [Scrape.do](https://scrape.do) for bypassing TruePeopleSearch's protection systems using premium US residential proxies.

[Find extended technical guide here. 📘](https://scrape.do/blog/true-people-search-scraping/)

## What's Included

### Person Information Scraper
* `scrapePersonInfo.py`: Scrapes detailed person information from TruePeopleSearch profile pages including name, age, location, address, and phone number data.

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
Age: 42
Address: 456 Oak Avenue
City: Chicago
State: IL
Phone Number: (555) 123-4567
```

## Technical Details

### Data Extraction Method
The scraper uses data attributes and schema.org microdata to extract person information from TruePeopleSearch profile pages:

- **Name extraction**: Uses `data-fn` and `data-ln` attributes from `div#personDetails`
- **Age extraction**: Uses `data-age` attribute from person details div
- **Address parsing**: Targets schema.org microdata with `itemprop` attributes
- **Phone extraction**: Uses `data-link-to-more="phone"` selector with telephone microdata
- **US geo-targeting**: Uses `geoCode=us` parameter for residential proxy routing

### Element Selectors Used
- Person details: `div#personDetails` with data attributes
- Address link: `a[data-link-to-more="address"]`
- Street address: `span[itemprop="streetAddress"]`
- City: `span[itemprop="addressLocality"]`
- State: `span[itemprop="addressRegion"]`
- Phone: `a[data-link-to-more="phone"] span[itemprop="telephone"]`

### Proxy Configuration
The script uses US-based residential proxies (`geoCode=us`) which are essential for accessing TruePeopleSearch content reliably.

## Common Errors

**403 or 429:** Your IP might be blocked; the script uses US residential proxies via `geoCode=us`<br>**Element not found:** Person profile may not exist or be formatted differently<br>**Data attribute missing:** Profile structure may have changed; verify the page loads correctly<br>**Missing phone data:** Some profiles may not have phone number information<br>**Microdata parsing errors:** Schema.org markup may vary for different profiles

## Output Format

The script outputs comprehensive person information directly to console for quick lookup and verification purposes.

## Supported Profile Types

This scraper works with TruePeopleSearch profile pages including:
- Individual person profiles
- Profiles with current addresses
- Profiles with phone numbers
- Profiles with age information
- Multi-location profiles
- Historical contact data

## Privacy & Legal Considerations

- Only access publicly available information
- Respect privacy and data protection laws
- Use responsibly and ethically
- Do not use for harassment or stalking
- Comply with local regulations regarding personal data

---

## Why Use Scrape.do?

- Rotating premium proxies & geo-targeting
- Built-in header spoofing
- Handles redirects, CAPTCHAs, and JavaScript rendering
- 1000 free credits/month

[Get your free API token here](https://dashboard.scrape.do/signup)