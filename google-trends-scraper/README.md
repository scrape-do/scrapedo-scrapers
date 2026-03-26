# Google Trends Scraper

Scrape Google Trends data without the official API — interest over time, regional breakdowns, related queries, and real-time trending topics. Works by hitting Google's internal JSON endpoints directly through [Scrape.do](https://scrape.do).

[Find the full technical guide here. 📘](https://scrape.do/blog/google-trends-scraping/)

## What's Included

* `scrapeGoogleTrends.py`: Talks to Google's undocumented Explore API — fetches widget tokens, then pulls interest-over-time, interest-by-region, and related queries into a single JSON file.
* `scrapeTrendingNow.py`: Renders the Trending Now page in a headless browser, scrapes the trends table, then clicks each row to grab related news articles from the detail panel.
* `serpApiTrends.py`: Hits Scrape.do's structured SERP API to pull AI Overview data with automatic handling of deferred (async) responses.

## Requirements

* Python 3.7+
* `requests` and `beautifulsoup4`<br>`pip install requests beautifulsoup4`
* A [Scrape.do API token](https://dashboard.scrape.do/signup) (free 1000 credits/month)

## How to Use: `scrapeGoogleTrends.py`

1. Configure your search:

   ```python
   token = "<your_token>"
   keyword = "coffee"
   timeframe = "today 3-m"
   geo = ""          # "" = worldwide; "US", "GB", "TR" = country; "US-CA" = state
   category = 0      # 0 = all; 3 = Business, 71 = Science/Tech
   property_filter = ""  # "" = Web, "youtube", "news", "images", "froogle"
   hl = "en-GB"
   tz = -180         # minutes offset: -180 = UTC+3, 0 = UTC
   ```

2. Run: `python scrapeGoogleTrends.py`

Output → `google-trends.json`:

```yaml
keyword: coffee
interest_over_time:
  - time: "Mar 1, 2026"
    value: 78
interest_by_region:
  - country_code: US
    country: United States
    value: 100
related_queries:
  top:
    - query: "coffee beans"
      value: 100
  rising:
    - query: "mushroom coffee"
      change: "+250%"
```

## How to Use: `scrapeTrendingNow.py`

1. Configure:

   ```python
   token = "<your_token>"
   geo = "US"
   hours = 24           # 4, 24, 48, or 168 (7 days)
   fetch_articles = True # set False to skip news extraction (saves credits)
   max_details = 5       # trends to expand for articles (each = 1 extra API call)
   ```

2. Run: `python scrapeTrendingNow.py`

Output → `trending-now.json`:

```yaml
trends:
  - name: "March Madness"
    search_volume: "500K+"
    volume_change: "1,200%"
    started: "2 hours ago"
    status: Active
    related_queries: ["NCAA", "bracket", "scores"]
    articles:
      - title: "March Madness 2026 bracket update"
        source: ESPN
```

## How to Use: `serpApiTrends.py`

1. Set your query:

   ```python
   token = "<your_token>"
   query = "why is pickleball so popular"
   ```

2. Run: `python serpApiTrends.py`

Output → `serp-api-ai-overview.json` with text blocks and source references.

## How It Works

### The Widget Token Dance (scrapeGoogleTrends.py)

Google Trends doesn't have a public API. Under the hood, the Explore page loads data through internal JSON endpoints. The trick is a two-step handshake:

1. Hit `/trends/api/explore` with your keyword/timeframe/geo — this returns a set of "widgets", each with a cryptographic `token`
2. Use each widget's token to call `/trends/api/widgetdata/{endpoint}` for the actual data

The tokens are tied to the exact request payload they were issued for — modify the payload after fetching, and you'll get a 401. All responses are prefixed with `)]}'` (Google's anti-XSSI protection), which gets stripped before JSON parsing.

### Browser Automation (scrapeTrendingNow.py)

The Trending Now page is a full JavaScript SPA — no useful data in the initial HTML. The script uses Scrape.do's `playWithBrowser` to:
- Wait for the trends table to render
- Parse trend names, search volumes, and metadata from the table rows
- Click individual rows (`data-row-id`) to open the detail panel
- Extract news articles from the `div.EMz5P` container

This requires `render=true` + `super=true`, making each request heavier (and more expensive) than the Explore API approach.

### SERP API (serpApiTrends.py)

Calls `/plugin/google/search` for structured JSON. When the AI Overview state is `deferred`, a follow-up call with the `session_key` is needed within 60 seconds. The script handles this automatically.

## Watch Out For

- **401 on widget data**: You modified the widget's request payload after getting the token — don't do that, the token is cryptographically bound to the exact payload
- **Empty regional data**: Some keywords just don't have enough search volume for regional breakdowns
- **Trending Now timeouts**: The SPA needs time to render; default timeout is 120s, bump it if your proxy is slow
- **Deferred AI Overview**: Session keys are single-use and expire in ~60 seconds; the script handles this, but be aware if you're modifying the code

## Output Files

| Script | Output | Contents |
|--------|--------|----------|
| `scrapeGoogleTrends.py` | `google-trends.json` | keyword, timeframe, geo, interest_over_time, interest_by_region, related_queries |
| `scrapeTrendingNow.py` | `trending-now.json` | geo, hours, trends with volumes, changes, articles |
| `serpApiTrends.py` | `serp-api-ai-overview.json` | query, state, text_blocks, references |

---

**Scrape.do** handles residential proxy rotation, CAPTCHAs, and JS rendering so you don't have to. [Get your free API token](https://dashboard.scrape.do/signup) (1000 credits/month).
