# TicketMaster Scraper

This folder includes a scraper for TicketMaster.com event listings using Python `requests` and [Scrape.do](https://scrape.do) for bypassing TicketMaster's protection systems and handling heavy JavaScript rendering requirements with premium US proxies.

[Find extended technical guide here. 📘](https://scrape.do/blog/ticketmaster-scraping/)

## What's Included

### Event Details Scraper
* `scrapeEventDetails.py`: Scrapes all event details from TicketMaster artist pages including event names, dates, venues, and locations using JSON-LD structured data extraction.

## Requirements

* Python 3.7+
* `requests` library<br>Install with:<br>`pip install requests`
* A [Scrape.do API token](https://dashboard.scrape.do/signup) for accessing TicketMaster bypassing protection systems and heavy JS rendering (free 1000 credits/month)

## How to Use: `scrapeEventDetails.py`

1. Copy the full artist URL from TicketMaster, example:<br>`https://www.ticketmaster.com/post-malone-tickets/artist/2119390`

2. In the script, replace:

   ```python
   token = "<your_token>"
   target_url = "<target_artist_url>"
   ```

3. Run the script:

   ```bash
   python scrapeEventDetails.py
   ```

The script will display all events for the artist in the console:

```yaml
Event: Houston Rodeo w/ Post Malone
Date: 2025-03-18T18:45:00
Venue: NRG Stadium
Location: Houston, TX

Event: Post Malone Presents: The BIG ASS Stadium Tour
Date: 2025-04-29T19:30:00
Venue: Rice-Eccles Stadium
Location: Salt Lake City, UT

Event: Post Malone Presents: The BIG ASS Stadium Tour
Date: 2025-05-03T19:30:00
Venue: Allegiant Stadium
Location: Las Vegas, NV

..
..

```

## Technical Details

### Data Extraction Method
The scraper uses regex to extract JSON-LD structured data from TicketMaster artist pages:

- **JSON-LD extraction**: Uses regex pattern `<script type="application/ld\+json">(.*?)</script>`
- **Event iteration**: Loops through all events in the structured data array
- **Location parsing**: Extracts venue names and full addresses from nested location objects
- **US geo-targeting**: Uses `geoCode=us` parameter for accessing US-based content

### Regex Pattern Used
```python
r'<script type="application/ld\+json">(.*?)</script>'
```
Extracts JSON-LD structured data containing all event information.

### API Configuration
The script uses specific Scrape.do parameters:
- `render=false`: Static HTML parsing (faster performance for JSON-LD extraction)
- `geoCode=us`: US geo-targeting for regional access
- `super=true`: Premium proxy routing for reliability

### Heavy JavaScript Requirements
TicketMaster uses **extensive JavaScript rendering** for dynamic content. While this scraper uses static parsing for performance, some pages may require:
- `render=true`: For JavaScript-heavy dynamic content
- **Extended processing time** for complex artist pages
- **Premium routing** to handle anti-bot measures

## Common Errors

**403 or 429:** TicketMaster protection triggered; premium proxies via `super=true` required<br>**JSON parsing errors:** Structured data format may have changed or be missing<br>**No events found:** Artist may not have upcoming events or page structure changed<br>**Heavy JS rendering needed:** Some pages may require `render=true` for full content access<br>**Regional restrictions:** Content may vary by geographic location

## Output Format

The script outputs comprehensive event information directly to console for quick tour schedule analysis and venue tracking.

## Supported Content Types

This scraper works with TicketMaster content including:
- Artist tour pages and schedules
- Concert and event listings
- Venue information and locations
- Event dates and timing
- Multi-city tour information
- Festival and special event listings

## Artist URL Format

TicketMaster uses structured URLs with artist identifiers:
- Format: `/artist-name-tickets/artist/artist-id`
- Example: `/post-malone-tickets/artist/2119390`
- Artist ID is unique numeric identifier

## Why Use Scrape.do?

- Rotating premium proxies & geo-targeting
- Built-in header spoofing
- Handles redirects, CAPTCHAs, and JavaScript rendering
- **Heavy JavaScript rendering capabilities**
- **US geo-targeting for regional content**
- **Premium anti-bot protection bypass**
- 1000 free credits/month

[Get your free API token here](https://dashboard.scrape.do/signup)