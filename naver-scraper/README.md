# Naver Scraper

This folder includes scrapers for various Naver services using Python `requests` and [Scrape.do](https://scrape.do) for bypassing Naver's WAF.

[Find the full guide and documentation here. 📗](https://scrape.do/blog/naver-scraping/)

## What's Included

### Ecommerce Scrapers
* `ecommerceProductPage.py`: Scrapes product name and price from a Naver product page using regex.
* `ecommerceAPI.py`: Fetches full product details from Naver's API and exports them to CSV.

### Search Scrapers
* `naverSearchAds.py`: Scrapes paid search advertisements from Naver search results.
* `naverSearchOrganic.py`: Scrapes organic search results from Naver with pagination support using JavaScript data extraction.
* `naverSearchImages.py`: Scrapes image search results using Naver's image search API.

## Requirements

* Python 3.7+
* `requests` library<br>Install with:<br>`pip install requests`
* A [Scrape.do API token](https://dashboard.scrape.do/signup) for accessing Naver bypassing its WAF (free 1000 credits/month)

## How to Use: `ecommerceProductPage.py`

1. Copy the full product URL from Naver, example:<br>`https://brand.naver.com/steelseries/products/11800715035`
2. In the script, replace:

   ```python
   token = "<your_token>"
   target_url = "<target_product_url>"
   ```
3. Run the script:

   ```bash
   python ecommerceProductPage.py
   ```

The script will return:

```yaml
Product Name: ...
Price: ...₩
```

## How to Use: `ecommerceAPI.py`

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
   python ecommerceAPI.py
   ```

A file called `naver_product_data.csv` will be created with:

* **Product Name**
* **Price**
* **Discount**
* **Image URL**
* **Stock Quantity**

## How to Use: `naverSearchAds.py`

1. In the script, replace:

   ```python
   token = "<your_token>"
   query = "<search_query>"
   ```
2. Run the script:

   ```bash
   python naverSearchAds.py
   ```

A file called `naver_ads_results.csv` will be created with:

* **Ad Title**
* **Ad URL**
* **Ad Description**

## How to Use: `naverSearchOrganic.py`

1. In the script, replace:

   ```python
   token = "<your_token>"
   query = "<search_query>"
   ```
2. Run the script:

   ```bash
   python naverSearchOrganic.py
   ```

A file called `naver_organic_results.csv` will be created with:

* **Title**
* **URL**
* **Description**

The script automatically scrapes multiple pages and includes retry logic for better results. Uses JavaScript data extraction to handle Naver's modern search result structure.

## How to Use: `naverSearchImages.py`

1. In the script, replace:

   ```python
   token = "<your_token>"
   query = "<search_query>"
   ```
2. Run the script:

   ```bash
   python naverSearchImages.py
   ```

A file called `naver_images_results.csv` will be created with:

* **Title**
* **Link**
* **Original URL**

The script uses Naver's image search API for reliable results and handles JSONP responses automatically.

## Common Errors

**403 or 429:** Add `&geoCode=kr` to the end of the Scrape.do URL to use a Korean IP<br>**Empty or missing fields:** Double-check your `channel_uid` and `product_id`; make sure the product is public and available<br>**Regex failure in `ecommerceProductPage.py`:** Confirm the page is returning complete HTML and you're not being blocked<br>**404 from `ecommerceAPI.py`**: API endpoint might've been changed, view the full tutorial to confirm the correct API structure.<br>**JSON parsing errors in `naverSearchImages.py`**: The API response format may have changed; check the response structure.
