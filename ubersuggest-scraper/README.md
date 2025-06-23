# Ubersuggest Scraper

[Find full technical guide here 📔](https://scrape.do/blog/ubersuggest-scraping/)

This repository includes Python scripts to extract keyword data and search engine result pages (SERPs) directly from Ubersuggest using [Scrape.do](https://scrape.do). It bypasses Ubersuggest’s bot protection by rotating proxies, handling headers, and injecting bearer tokens.

All scripts use publicly accessible API endpoints, no login required.

⚠ This guide was created for research and educational purposes and our approach of bypassing Ubersuggest using Bearer Tokens might be invalid in the near future.

---

## What’s Included

* `bearerTokenGenerator.py`: Extracts a temporary Bearer token from Ubersuggest's network.
* `keywordOverview.py`: Fetches volume, CPC, SEO difficulty, and paid difficulty for any keyword.
* `SERPresults.py`: Retrieves full SERP breakdown (URLs, titles, positions, clicks, domain authority).
* `keywordOverviewAutoBearer.py`: Automates both bearer token generation and keyword lookup.

## Requirements

* Python 3.7+
* `requests` library, install with:

  ```bash
  pip install requests
  ```
* A [Scrape.do API token](https://dashboard.scrape.do/signup) (**1000 free credits/month**)

---

## 🔍 How to Use Each Script

### `bearerTokenGenerator.py`

**Fetches a temporary Bearer token used by Ubersuggest’s APIs.**

1. Replace the API token:

   ```python
   scrape_token = "<your-token>"
   ```
2. Run:

   ```bash
   python bearerTokenGenerator.py
   ```

Returns a Bearer token that you can plug into other scripts.

### `keywordOverview.py`

**Gets keyword volume, CPC, SEO difficulty, and paid difficulty for a given keyword.**

1. Replace your API and bearer tokens:

   ```python
   scrape_token = "<your-token>"
   bearer_token = "app#unlogged__XXXX..."
   ```
2. Set your keyword and region:

   ```python
   keyword = "ubersuggest"
   locId = 2840  # USA
   ```
3. Run:

   ```bash
   python keywordOverview.py
   ```

Returns a summary like:

```text
Keyword: ubersuggest
Volume : 22,200
CPC    : $3.17
SEO Difficulty: 40
Paid Difficulty: 37
```

### `SERPresults.py`

**Pulls the full organic SERP from Ubersuggest’s backend API.**

1. Replace API and bearer tokens:

   ```python
   scrape_token = "<your-token>"
   bearer_token = "app#unlogged__XXXX..."
   ```
2. Run:

   ```bash
   python SERPresults.py
   ```

Outputs a list of ranking URLs with position, title, clicks, domain, and authority.

### `keywordOverviewAutoBearer.py`

**End-to-end script that fetches a fresh Bearer token and retrieves keyword overview data.**

1. Replace your Scrape.do token:

   ```python
   scrape_token = "<your-token>"
   ```
2. Run:

   ```bash
   python keywordOverviewAutoBearer.py
   ```

No need to manually handle headers or bearer tokens.

---

## ⚠️ Notes & Limitations

* Each Bearer token is temporary; you must refresh it frequently.
* Use realistic delays or caching to avoid wasting API credits.
* Data comes from public APIs used by Ubersuggest frontend; no login required.
* We do not condone large-scale scraping using this method, which can become unethical very quickly.

---

## 📈 Why Use Scrape.do?

Scrape.do handles the heavy lifting so you don’t have to:

* Bypass WAFs and geo-blocks
* Inject custom headers and bearer tokens
* Works on JS-heavy, API-backed tools
* 1000 API requests/month for free

👉 [Get your free API key](https://dashboard.scrape.do/signup)
