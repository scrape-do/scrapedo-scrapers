# Zomato Scraper

Scrape restaurant info and full delivery menus from Zomato using Python and the Scrape.do API for proxy & header rotation to bypass IP bans.

## Files:

* restaurantInfo.py – Extracts restaurant name, address, rating, price, etc.
* deliveryMenu.py – Extracts structured delivery menus with item names, categories, and prices.

## Requirements:

Run `pip install requests beautifulsoup4` to install dependencies.

## Usage:

1. Add your Scrape.do API token to each script before running.
2. Run the scraper you want to use:<br>`python restaurantInfo.py`<br>`python deliveryMenu.py`

⚠ Example Zomato URLs are hardcoded in the scripts; replace them with your own targets.
