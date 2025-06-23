# Google Search Scraper

This repository provides Python scripts to scrape **organic results**, **search ads**, **FAQs**, and **related search terms** directly from Google Search using [Scrape.do](https://scrape.do).

Scrape.do helps bypass Google's anti-bot mechanisms like WAFs, rate limits, CAPTCHAs and JavaScript rendering.

All scripts use publicly accessible HTML data and require no login or session emulation.

[Find the full guide here.](https://scrape.do/blog/scraping-google-search-results/) 📔

---

## What’s Included

* `firstPageResults.py`: Scrapes organic search results (title, link, snippet) from the first page.
* `allOrganicResults.py`: Paginates through all available search result pages and extracts organic results.
* `paidSearchAds.py`: Extracts top and bottom **sponsored search ads** (URL, title, description, display URL).
* `frequentlyAskedQuestions.py`: Scrapes "People also ask" questions shown on the SERP.
* `relatedSearchTerms.py`: Grabs keyword suggestions from the bottom of the SERP.

## Requirements

* Python 3.7+
* `requests` and `beautifulsoup4` libraries&lt;br&gt;Install with:

  ```bash
  pip install requests beautifulsoup4
  ```
* A [Scrape.do API token](https://dashboard.scrape.do/signup) (**free** 1000 API credits/month)

---

## 🔍 How to Use Each Script

### `firstPageResults.py`

**Scrapes all organic search results on the first Google SERP.**

1. Replace the query and token:

   ```python
   scrape_token = "<your-token>"
   query = "python web scraping"
   ```
2. Run:

   ```bash
   python firstPageResults.py
   ```

Outputs titles, URLs, and descriptions for the top 10 results.

### `allOrganicResults.py`

**Paginates through multiple SERP pages to scrape all organic results.**

1. Set the query and token as above.
2. Run the script:

   ```bash
   python allOrganicResults.py
   ```

Prints full organic listings with position, title, and snippet text.

### `paidSearchAds.py`

**Scrapes paid search ads (sponsored results) including title, URL, and ad copy.**

1. Set the query and token:

   ```python
   scrape_token = "<your-token>"
   query = "python web scraping"
   ```
2. Run:

   ```bash
   python paidSearchAds.py
   ```

Extracts ad data from the `uEierd` block used in Google's ad markup.

### `frequentlyAskedQuestions.py`

**Extracts the "People also ask" block (FAQs) from the search results.**

1. Set query and token.
2. Run:

   ```bash
   python frequentlyAskedQuestions.py
   ```

Returns question strings as shown in the FAQ accordion.

### `relatedSearchTerms.py`

**Scrapes the "Related searches" suggestions at the bottom of the SERP.**

1. Set query and token.
2. Run:

   ```bash
   python relatedSearchTerms.py
   ```

Prints related queries useful for keyword research and clustering.

---

## ⚠️ Legal & Ethical Notes

Please ensure:

* You scrape only **public search results**
* You **do not automate excessive requests** or violate [Google’s Terms of Service](https://policies.google.com/terms).
* Scrape.do handles proxies, headers, and anti-bot solutions for you; but always use scraping responsibly.

---

## 🚀 Why Use Scrape.do?

* Rotating premium proxies & geo-targeting
* Built-in header spoofing
* Handles redirects, CAPTCHAs, and JavaScript rendering
* 1000 free credits/month

👉 [Get your free API token here](https://dashboard.scrape.do/signup)
