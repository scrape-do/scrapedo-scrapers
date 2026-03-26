# Google Search Scraper

Six scripts that cover every section of the Google SERP: organic results, paid ads, "People also ask" questions, related searches, and a SERP API alternative that returns all of the above as structured JSON in a single call. All requests route through [Scrape.do](https://scrape.do) with residential proxies.

[Find the full guide here.](https://scrape.do/blog/scraping-google-search-results/) 📔

## What's Included

| Script | What It Scrapes | Output |
|--------|----------------|--------|
| `firstPageResults.py` | Organic results from page 1 | `first-page-results.csv` |
| `allOrganicResults.py` | Organic results across multiple pages | `all-organic-results.csv` |
| `paidSearchAds.py` | Sponsored ad blocks (top + bottom) | `paid-search-ads.json` |
| `frequentlyAskedQuestions.py` | "People also ask" accordion | `faq-results.json` |
| `relatedSearchTerms.py` | "Related searches" at the bottom | `related-search-terms.json` |
| `serpApiSearch.py` | Everything above via SERP API | `serp-api-search-results.json` |

## Requirements

* Python 3.7+
* `requests` and `beautifulsoup4`<br>`pip install requests beautifulsoup4`
* A [Scrape.do API token](https://dashboard.scrape.do/signup) (**free** 1000 credits/month)

---

## Quick Start

Every HTML-based script follows the same pattern — set your token and query, run it:

```python
token = "<your_token>"
query = "python web scraping"
```

```bash
python firstPageResults.py
python allOrganicResults.py    # also set MAX_PAGES = 5
python paidSearchAds.py
python frequentlyAskedQuestions.py
python relatedSearchTerms.py
```

### SERP API: All-in-One

`serpApiSearch.py` skips HTML parsing entirely. It calls Scrape.do's `/plugin/google/search` endpoint and gets organic results, ads, People Also Ask, and related searches back as structured JSON in one request:

```python
token = "<your_token>"
query = "python web scraping"
```

```bash
python serpApiSearch.py
```

Output → `serp-api-search-results.json` with `organic_results`, `top_ads`, `bottom_ads`, `related_questions`, `related_searches`.

## How It Works

All HTML scripts use `super=true` for residential proxy rotation and `hl=en&gl=us` for English/US results. BeautifulSoup parses the response. The scripts target specific SERP sections:

- **Organic results** (`firstPageResults.py`, `allOrganicResults.py`): Grabs `div` containers with the `Ww4FFb` class, extracts `h3` title, `a` link, and `VwiC3b` description. The multi-page version paginates via `start=10`, `start=20`, etc.
- **Paid ads** (`paidSearchAds.py`): Targets the `uEierd` ad container blocks, with fallback class matching for ad titles (`CCgQ5`, `vCa9Yd`, `QfkTvb`) and descriptions (`Va3FIb`, `r025kc`, `lVm3ye`).
- **FAQs** (`frequentlyAskedQuestions.py`): Finds `div` elements with `jsname="yEVEwb"` — the "People also ask" accordion items.
- **Related searches** (`relatedSearchTerms.py`): Targets `div.b2Rnsc.vIifob` at the bottom of the SERP.

The **SERP API** (`serpApiSearch.py`) bypasses all of this by calling `/plugin/google/search`, which does the parsing server-side and returns clean JSON.

## Watch Out For

- **Google changes class names**: The HTML selectors (`Ww4FFb`, `uEierd`, etc.) can change without notice. The SERP API is more stable long-term.
- **No ads for some queries**: Not every search triggers sponsored results — `paidSearchAds.py` will return an empty list.
- **Pagination stops early**: Google may return fewer pages for tail-end queries. `allOrganicResults.py` stops when no more results are found.

---

**Scrape.do** handles proxy rotation, header spoofing, CAPTCHAs, and JS rendering. [Get your free API token](https://dashboard.scrape.do/signup) (1000 credits/month).
