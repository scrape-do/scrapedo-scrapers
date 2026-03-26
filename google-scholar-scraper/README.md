# Google Scholar Scraper

Scrape Google Scholar search results and author profiles — with an optional bonus that downloads each paper as clean markdown. Scholar has no public API and some of the most aggressive bot detection in Google's ecosystem, so every request routes through [Scrape.do](https://scrape.do) with residential proxies.

[Find the full technical guide here. 📘](https://scrape.do/blog/google-scholar-scraping/)

## What's Included

* `searchScraper.py`: Searches Scholar with pagination, collects paper titles, snippets, authors, and links. Then optionally downloads each linked paper as markdown using a three-tier fallback strategy (basic → super → super+render).
* `authorScraper.py`: Scrapes an author's profile — name, affiliation, verified email, citation counts (all-time and since 2020), and a full paginated list of publications (up to 100 per page).

## Requirements

* Python 3.7+
* `requests` and `beautifulsoup4`<br>`pip install requests beautifulsoup4`
* A [Scrape.do API token](https://dashboard.scrape.do/signup) (free 1000 credits/month)

## How to Use: `searchScraper.py`

1. Configure your search:

   ```python
   TOKEN = "<your_token>"
   SEARCH_QUERY = "breakfast in the morning"
   MAX_PAGES = 3
   ```

2. Run: `python searchScraper.py`

Output → `scholar_search_results.json`:

```yaml
- title: "The role of breakfast in health"
  description: "This study examines the impact of..."
  authors: "J Smith, K Johnson - Journal of Nutrition, 2024"
  link: "https://..."
```

Papers with accessible links also get downloaded as markdown files into `scholar_articles/`.

## How to Use: `authorScraper.py`

1. Grab an author URL from Scholar and configure:

   ```python
   TOKEN = "<your_token>"
   AUTHOR_URL = "https://scholar.google.com/citations?user=qNuSIPAAAAAJ"
   ```

2. Run: `python authorScraper.py`

Output → `scholar_author_articles.json`:

```yaml
- title: "Attention Is All You Need"
  authors: "A Vaswani, N Shazeer, N Parmar..."
  journal: "Advances in neural information processing systems"
  citations: "120000"
  year: "2017"
  link: "https://scholar.google.com/citations?..."
```

The console also prints the author's name, affiliation, verified email, and citation stats.

## How It Works

### Why `super=true` Is Non-Negotiable

Scholar's bot detection is one of the tightest in Google's lineup. Without residential proxies, you'll hit CAPTCHAs on the first request. Every request in both scripts uses `super=true` — this is the one Google property where you can't get away with standard datacenter proxies.

The upside: Scholar is fully server-side rendered. No `render=true` needed, no JavaScript execution, no headless browsers. Just clean HTML with BeautifulSoup.

### Search Pagination

Scholar serves 10 results per page. Pagination uses the `start` parameter (`0`, `10`, `20`...). Each result lives inside a `div.gs_ri` container — title in `h3.gs_rt`, snippet in `div.gs_rs`, author/venue in `div.gs_a`.

### Article Download: Three-Tier Fallback

For each search result with a link, the script tries to fetch the full article as markdown via Scrape.do's `output=markdown`:

1. **Basic** — plain request, cheapest option
2. **`super=true`** — residential proxy, handles most publisher WAFs
3. **`super=true&render=true`** — full browser rendering, for JavaScript-heavy journal sites

A download is only considered successful if it returns HTTP 200 and the body exceeds 100 characters (filters out paywall stubs and error pages).

### Author Profile: Server-Side Pagination

Scholar's author page defaults to showing 20 articles with a "Show More" button. Instead of simulating clicks, the script bypasses this entirely by appending `cstart` and `pagesize` URL parameters — requesting up to 100 articles per page and looping until no more rows appear.

Citation stats come from `table#gsc_rsb_st` (the "Citations" / "h-index" / "i10-index" table). Articles are in `tr.gsc_a_tr` rows. Articles without a detail link are flagged as citation-only entries.

## Watch Out For

- **CAPTCHAs without `super=true`**: Scholar will block you instantly — this parameter isn't optional here
- **Paywall failures**: Many papers are behind publisher paywalls. The three-tier fallback handles most, but some will fail regardless
- **Citation-only entries**: Some author articles have no Scholar detail page link — they're imported citations, not full entries
- **Rate limits**: A 1-second delay between requests is built in. Scholar is particularly sensitive to rapid-fire requests

## Output Files

| Script | Output | Contents |
|--------|--------|----------|
| `searchScraper.py` | `scholar_search_results.json` | title, description, authors, link |
| `searchScraper.py` | `scholar_articles/*.md` | downloaded paper content as markdown |
| `authorScraper.py` | `scholar_author_articles.json` | title, authors, journal, citations, year, link |

---

**Scrape.do** handles the residential proxies and anti-bot bypass that Scholar demands. [Get your free API token](https://dashboard.scrape.do/signup) (1000 credits/month).
