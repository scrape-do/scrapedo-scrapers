# Best Buy Product Scrapers (Python)

Best Buy has one of the most aggressive JS rendering in e-commerce and locks all results behind a forced country-select screen. 🔒

This repo includes two working scrapers using two different tools that bypass country-select screen, renders the page and products with lazy-loading, and extract product listings from a specific category on Best Buy. 🔑

Both scripts collect brand, title, price, image, model, SKU and print them to a CSV document while looping through all category pages.

[Read full technical guide here.](https://scrape.do/blog/best-buy-scraping/)

## `bestBuySeleniumScraper.py`

Uses Selenium to launch a real browser, click through the country selection screen, scroll each page, and scrape product data.

Suited for small-scale jobs or local testing; will get blocked and fail after a few runs.

## `bestBuyScrapeDoScraper.py`
Uses the Scrape.do API to fully render pages in the cloud, simulate scroll and click behavior, and extract all products from all category pages. 

Built for scale and stability with error handling and retry logic. [**Get free API token by signing up**](https://dashboard.scrape.do/signup).

## Why Scrape.do?

With **Scrape.do**, you don’t need to manage proxies, handle browser execution, or build retry logic from scratch.

Just send a request, and get clean, rendered data back.

* ✅ Unblocked access with geo-targeted residential IPs
* 🧠 Smart browser automation with `playWithBrowser`
* 💨 Fast, stable infrastructure built for scale

[**Get 1000 free credits and start scraping websites with Scrape.do**](https://dashboard.scrape.do/signup).
