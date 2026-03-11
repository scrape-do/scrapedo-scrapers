# Reddit Scraper

Three Python scrapers for extracting subreddit posts, search results, and comments from Reddit using [Scrape.do](https://scrape.do) for anti-bot bypass.

[Find extended technical guide here. 📘](https://scrape.do/blog/reddit-scraping/)

## What's Included

* `scrapeSubredditPosts.py`: Scrapes posts from any subreddit with sort options (new, hot, top, rising), time filters, and multi-page pagination.
* `scrapeRedditSearch.py`: Scrapes Reddit search results for any query with sort options (relevance, hot, new, top, comments) and cursor-based pagination.
* `scrapeRedditComments.py`: Scrapes Reddit comments matching a search query with sort options (relevance, new, top) and pagination.

## Requirements

* Python 3.7+
* `requests` library<br>Install with:<br>`pip install requests`
* `beautifulsoup4` library<br>Install with:<br>`pip install beautifulsoup4`
* A [Scrape.do API token](https://dashboard.scrape.do/signup) for bypassing Reddit's anti-bot protection (free 1000 credits/month)

## How to Use: `scrapeSubredditPosts.py`

1. In the script, replace the token and configure your target:

   ```python
   token = "<your_token>"
   subreddit = "fishing"
   sort = "new"          # "new", "hot", "top", "rising"
   time_filter = "month" # only for sort="top"
   max_pages = 3
   ```

2. Run the script:

   ```bash
   python scrapeSubredditPosts.py
   ```

Output saved to `subreddit-posts.csv`:

```yaml
title: Any north Indiana/Michigan angler?
author: landonx420x
score: 2
comments: 0
timestamp: 2026-03-11T08:31:18.644000+0000
permalink: https://www.reddit.com/r/Fishing/comments/1rqo5cp/...
```

## How to Use: `scrapeRedditSearch.py`

1. In the script, replace the token and configure your search:

   ```python
   token = "<your_token>"
   query = "best fishing rod"
   sort = "relevance"    # "relevance", "hot", "new", "top", "comments"
   time_filter = "year"  # only for sort="top"
   max_pages = 3
   ```

2. Run the script:

   ```bash
   python scrapeRedditSearch.py
   ```

Output saved to `search-results.csv`:

```yaml
title: What's the best rod out there?
subreddit: r/Fishing_Gear
url: https://www.reddit.com/r/Fishing_Gear/comments/1p6y9sr/...
```

## How to Use: `scrapeRedditComments.py`

1. In the script, replace the token and configure your search:

   ```python
   token = "<your_token>"
   query = "best fishing rod"
   sort = "relevance"  # "relevance", "new", "top"
   time_filter = "all" # only for sort="top"
   max_pages = 3
   ```

2. Run the script:

   ```bash
   python scrapeRedditComments.py
   ```

Output saved to `reddit-comments.csv`:

```yaml
author: u/trout_master42
comment: For the price, the St. Croix Triumph is hard to beat...
thread_title: Best rod recommendations for beginners?
subreddit: r/Fishing_Gear
thread_url: https://www.reddit.com/r/Fishing_Gear/comments/abc123/...
```

## Technical Details

### Data Extraction Method

Each script targets different Reddit endpoints and HTML structures:

- **Subreddit posts**: Uses Reddit's internal Shreddit API (`/svc/shreddit/community-more-posts/{sort}/`). Post data is stored as attributes on `<shreddit-post>` custom HTML elements (`post-title`, `author`, `score`, `comment-count`, `created-timestamp`, `permalink`).
- **Search results**: Uses the standard search page (`/search/?q={query}`). Results are inside `[data-testid="sdui-post-unit"]` containers with title in `[data-testid="post-title-text"]`.
- **Comments**: Uses the search page with `type=comments`. Comments are inside `[data-testid="search-sdui-comment-unit"]` containers with body text in `[data-testid="search-comment-content"]`.

### Pagination

- **Subreddit posts**: Uses a base64-encoded `after` token extracted via regex from the response HTML.
- **Search results and comments**: Use a `cursor` + `iId` pair extracted via regex.

### Proxy Configuration

All scripts use `super=true` for premium residential proxy routing through Scrape.do. Reddit's anti-bot protection returns a stripped-down page (with status 200) when it detects automated requests. The `super=true` parameter bypasses this without requiring JavaScript rendering (`render=true` is not needed).

## Common Errors

- **200 status but limited content**: Missing `super=true` parameter; Reddit serves only 3 posts instead of 25
- **No posts/results found**: The subreddit name or search query may not have results, or the page structure may have changed
- **Pagination stops early**: Reddit may return fewer pages for certain queries or sort options
- **~1 post overlap between pages**: Normal behavior for Reddit's cursor-based pagination; deduplicate in post-processing if needed

## Output Format

Each script saves results to a CSV file:

- `subreddit-posts.csv`: title, author, score, comments, timestamp, permalink
- `search-results.csv`: title, subreddit, url
- `reddit-comments.csv`: author, comment (truncated to 500 chars), thread_title, subreddit, thread_url

## Privacy & Legal Considerations

- Only access publicly available information
- Respect Reddit's robots.txt and rate limits
- Do not scrape login-protected or private content
- Use collected data responsibly and ethically
- Comply with local regulations regarding data collection

---

## Why Use Scrape.do?

- Premium residential proxies that bypass Reddit's anti-bot detection
- No JavaScript rendering needed for Reddit (faster requests)
- Handles CAPTCHAs and browser fingerprinting automatically
- 1000 free credits/month

[Get your free API token here](https://dashboard.scrape.do/signup)
