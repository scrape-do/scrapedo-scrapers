# PeopleSearchNow Scraper

This folder includes a scraper for PeopleSearchNow.com people lookup using Python `requests` and [Scrape.do](https://scrape.do) for bypassing PeopleSearchNow's protection systems using premium US residential proxies.

## What's Included

### Person Information Scraper
* `scrapePersonInfo.py`: Scrapes detailed person information from PeopleSearchNow profile pages including name, age, address, city, and state data.
* `test_scrapePersonInfo.py`: Simple test suite to validate the scraper functionality.

## Requirements

* Python 3.7+
* `requests` library<br>Install with:<br>`pip install requests`
* `beautifulsoup4` library<br>Install with:<br>`pip install beautifulsoup4`
* A [Scrape.do API token](https://dashboard.scrape.do/signup) for accessing PeopleSearchNow bypassing its protection systems (free 1000 credits/month)

## How to Use: `scrapePersonInfo.py`

1. Copy the full person profile URL from PeopleSearchNow, example:<br>`https://www.peoplesearchnow.com/person/john-doe`

2. In the script, replace:

   ```python
   token = "<your_token>"
   target_url = "<target_person_url>"
   ```

   **⚠️ SECURITY WARNING:** Never commit your actual Scrape.do API token to version control or share it publicly. Keep your token secure and private at all times.

3. Run the script:

   ```bash
   python scrapePersonInfo.py
   ```

The script will display person information in the console:

```yaml
Name: John Doe
Age: 35
Address: 123 Main Street
City: Los Angeles
State: CA
```

## Technical Details

### Data Extraction Method
The scraper uses HTML element selectors to extract person information from PeopleSearchNow profile pages:

- **Name extraction**: Extracts from `h1.name` element
- **Age extraction**: Uses `.age` class selector and removes "Age: " or "Age " prefix
- **Address parsing**: Targets `.address` class with nested span elements
- **City and State parsing**: Extracts from address component and splits by comma
- **US geo-targeting**: Uses `geoCode=us` parameter for residential proxy routing

### Element Selectors Used
- Name: `h1.name`
- Age: `div.age`
- Address container: `div.address`
- Address components: `span` elements within address container

### Proxy Configuration
The script uses US-based residential proxies (`geoCode=us`) which are essential for accessing PeopleSearchNow content reliably.

## Common Errors

- **403 or 429:** Your IP might be blocked; the script uses US residential proxies via `geoCode=us`
- **Element not found:** Person profile may not exist or be formatted differently
- **Parsing errors:** Profile page structure may have changed; verify the page loads correctly
- **Missing address data:** Some profiles may not have current address information
- **Split errors:** City/state format may vary for different profiles

## Output Format

The script outputs key person information directly to console for quick lookup and verification purposes.

## Supported Profile Types

This scraper works with PeopleSearchNow profile pages including:
- Individual person profiles
- Profiles with current addresses
- Profiles with age information
- Multi-location profiles
- Historical address data

## Testing

A basic test suite is included to validate the scraper functionality:

```bash
python test_scrapePersonInfo.py
```

**Note:** To run meaningful tests, you must first:
1. Add your valid Scrape.do API token in `scrapePersonInfo.py`
2. Set a valid profile URL in the `target_url` variable
3. The tests will verify that required fields are extracted

## Privacy & Legal Considerations

- Only access publicly available information
- Respect privacy and data protection laws
- Use responsibly and ethically
- Do not use for harassment or stalking
- Comply with local regulations regarding personal data
- **Never share your Scrape.do API token publicly**
- Be aware that scraping personal information may be subject to legal restrictions in your jurisdiction
- Always verify you have the legal right to access and use this data

---

## Why Use Scrape.do?

- Rotating premium proxies & geo-targeting
- Built-in header spoofing
- Handles redirects, CAPTCHAs, and JavaScript rendering
- 1000 free credits/month
- **Remember: Keep your API token secure and never share it**

[Get your free API token here](https://dashboard.scrape.do/signup)
