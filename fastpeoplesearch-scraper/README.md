# FastPeopleSearch Scraper

This folder includes a scraper for FastPeopleSearch.com people lookup using Python `requests` and [Scrape.do](https://scrape.do) for bypassing FastPeopleSearch's protection systems using premium US residential proxies.

[Find extended technical guide here. 📘](https://scrape.do/blog/fast-people-search-scraping/)

## What's Included

### Person Information Scraper
* `scrapePersonInfo.py`: Scrapes detailed person information from FastPeopleSearch profile pages including name, age, location, and address data.

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
Age: 35
City: Los Angeles
State: CA
Address: 123 Main Street
```

## Technical Details

### Data Extraction Method
The scraper uses HTML element selectors to extract person information from FastPeopleSearch profile pages:

- **Name and location parsing**: Extracts from `h1#details-header` element and splits location data
- **Age extraction**: Uses `h2#age-header` selector and removes "Age " prefix
- **Address parsing**: Targets `div#current_address_section` to find current address information
- **US geo-targeting**: Uses `geoCode=us` parameter for residential proxy routing

### Element Selectors Used
- Header information: `h1#details-header`
- Age data: `h2#age-header`
- Address section: `div#current_address_section`

### Proxy Configuration
The script uses US-based residential proxies (`geoCode=us`) which are essential for accessing FastPeopleSearch content reliably.

## Common Errors

**403 or 429:** Your IP might be blocked; the script uses US residential proxies via `geoCode=us`<br>**Element not found:** Person profile may not exist or be formatted differently<br>**Parsing errors:** Profile page structure may have changed; verify the page loads correctly<br>**Missing address data:** Some profiles may not have current address information<br>**Split errors:** Name/location format may vary for different profiles

## Output Format

The script outputs key person information directly to console for quick lookup and verification purposes.

## Supported Profile Types

This scraper works with FastPeopleSearch profile pages including:
- Individual person profiles
- Profiles with current addresses
- Profiles with age information
- Multi-location profiles
- Historical address data

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