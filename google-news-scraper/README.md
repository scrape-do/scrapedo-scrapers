# Google News Scraper

Scrape headlines, metadata, and full article text from Google's News tab — plus a SERP API alternative that returns structured JSON without any HTML parsing. Uses [Scrape.do](https://scrape.do) for proxy rotation and bot bypass.

[Find the full technical guide here. 📘](https://scrape.do/blog/google-news-scraping/)

## What's Included

* `newsScraper.py`: Scrapes the Google News tab (`tbm=nws`), extracts headlines with source/date/description, paginates through results, and downloads each article as markdown. If `super=true` returns empty results, it automatically retries with browser rendering.
* `serpApiNews.py`: Calls Scrape.do's SERP API to pull `top_stories` and `discussions_and_forums` as structured JSON — no BeautifulSoup needed.

## Requirements

* Python 3.7+
* `requests` and `beautifulsoup4`<br>`pip install requests beautifulsoup4`
* A [Scrape.do API token](https://dashboard.scrape.do/signup) (free 1000 credits/month)

## How to Use: `newsScraper.py`

1. Configure your search:

   ```python
   TOKEN = "<your_token>"
   SEARCH_QUERY = "artificial intelligence"
   MIN_RESULTS = 20
   MAX_PAGES = 5
   ```

2. Run: `python newsScraper.py`

Output → `news_search_results.json`:

```yaml
- title: "AI breakthrough in medical imaging"
  source: "MIT Technology Review"
  date: "2 hours ago"
  description: "Researchers have developed a new AI model..."
  link: "https://..."
```

Each article also gets downloaded as markdown into the `news_articles/` folder.

## How to Use: `serpApiNews.py`

1. Set your query:

   ```python
   token = "<your_token>"
   query = "artificial intelligence news"
   ```

2. Run: `python serpApiNews.py`

Output → `serp-api-news-results.json` with `articles` (from the top stories carousel) and `discussions_and_forums` (Reddit, Quora threads).

## How It Works

### Dealing with Google's Rotating Class Names

Google's News tab is one of the more annoying targets to parse because Google frequently rotates CSS class names on the news card containers. The script handles this with a shotgun approach — trying multiple known selectors (`SoaBEf`, `dbsr`, `Gx5Zad`, `xuvV6b`) and falling back to `div[role="heading"]` parent containers if none match.

Article URLs on the News tab are wrapped in Google's `/url?q=` redirect. The script unwraps these to get the actual article link.

### Auto-Retry with Rendering

If `super=true` returns no results (which can happen when Google serves a JavaScript-heavy variant of the News tab), the script automatically retries the same page with `render=true` added. This way you only pay the rendering cost when you actually need it.

### Article Download: Three-Tier Fallback

Same progressive strategy used across the repo: basic → `super=true` → `super=true&render=true`. Each article link goes through this chain until one succeeds (HTTP 200 + body > 100 chars). Failed downloads are logged but don't stop the scraper.

### SERP API (serpApiNews.py)

For a cleaner approach, the SERP API returns pre-parsed JSON via `/plugin/google/search`. News articles come from the `top_stories` field (the carousel at the top of Google results). You also get `discussions_and_forums` for free. The trade-off: fewer results than the full News tab, but zero HTML parsing and a more stable interface.

## Watch Out For

- **Empty results on first try**: Google may serve a JS-heavy page variant. The auto-retry with `render=true` handles this, but adds latency.
- **Paywall articles**: The markdown download will get blocked by some publishers. The three-tier fallback handles most, but premium outlets like WSJ/NYT will often fail.
- **CSS class rotation**: If Google changes all the selector class names at once, the script may need updated selectors. The `div[role="heading"]` fallback is the most stable anchor.
- **`tbm=nws` vs `news.google.com`**: This scraper targets the Search News tab, not the Google News homepage. Different page, different structure.

## Output Files

| Script | Output | Contents |
|--------|--------|----------|
| `newsScraper.py` | `news_search_results.json` | title, source, date, description, link |
| `newsScraper.py` | `news_articles/*.md` | downloaded article content as markdown |
| `serpApiNews.py` | `serp-api-news-results.json` | articles (title, source, link), discussions_and_forums |

---

**Scrape.do** handles proxy rotation, rendering fallbacks, and anti-bot bypass. [Get your free API token](https://dashboard.scrape.do/signup) (1000 credits/month).
