# Naver Scraper

This folder includes two examples for scraping product data from Naver using Python `requests` for Scraping and [Scrape.do](https://scrape.do) for bypassing Naver's WAF.

One method scrapes the HTML from a product page; the other uses Naver’s internal API for cleaner results.

For the full guide and documentation, go here: https://scrape.do/blog/naver-scraping/

## What’s Included

* `productpage.py`: Scrapes product name and price from a Naver product page using regex.
* `APIscraper.py`: Fetches full product details from Naver’s API and exports them to CSV.

## Requirements

* Python 3.7+
* `requests` library<br>Install with:<br>`pip install requests`
* A [Scrape.do API token](https://dashboard.scrape.do/signup) for accessing Naver bypassing its WAF (free 1000 credits/month)

## How to Use: `productpage.py`

1. Copy the full product URL from Naver, example:<br>`https://brand.naver.com/steelseries/products/11800715035`
2. In the script, replace:

   ```python
   token = "<your_token>"
   target_url = "<target_product_url>"
   ```
3. Run the script:

   ```bash
   python productpage.py
   ```

The script will return:

```yaml
Product Name: ...
Price: ...₩
```

## How to Use: `APIscraper.py`

1. Get the `channel_uid` and `product_id`
   * `product_id` is the numeric ID in the product URL, example: `11800715035`
   * `channel_uid` can be found in the page source (search `"channelUid"` in DevTools)
2. In the script, replace:

   ```python
   token = "<your_token>"
   channel_uid = "<product_channel_uid>"
   product_id = "<product_id>"
   ```
3. Run the script:

   ```bash
   python APIscraper.py
   ```

A file called `naver_product_data.csv` will be created with:

* **Product Name**
* **Price**
* **Discount**
* **Image URL**
* **Stock Quantity**

## Common Errors

**403 or 429:** Add `&geoCode=kr` to the end of the Scrape.do URL to use a Korean IP<br>**Empty or missing fields:** Double-check your `channel_uid` and `product_id`; make sure the product is public and available<br>**Regex failure in `productpage.py`:** Confirm the page is returning complete HTML and you’re not being blocked<br>**404 from `APIscraper.py`**: API endpoint might've been changed, view the full tutorial to confirm the correct API structure.
