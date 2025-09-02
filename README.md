# Scrape.do Scrapers

_Stop relying on overpriced APIs for popular domains!_ 🤚🏻

This repository contains scraping samples for the most scraped domains on the web, with full-length tutorials and functioning scrapers mainly built with Python and NodeJS (_NodeJS files included in separate folders_).

Scrapers in this repository are programmed to help you understand the basics of scraping these popular websites and serving as a base for you to customize and use in your own projects.

For Python, you'll be using: 
- __Python 3.8+__, 
- [__Requests__](https://github.com/psf/requests) for handling HTTP requests, 
- [__Beautiful Soup__](https://pypi.org/project/beautifulsoup4/) for parsing information, 
- and [__urllib.parse__](https://docs.python.org/3/library/urllib.parse.html) for URL encoding.

This repository also uses [Scrape.do](https://scrape.do/)'s web scraping API, __to bypass Web Application Firewalls (WAFs)__ of the domains you're scraping and also __interacting with the browser__.

## Available Scrapers

| Domain | Status | Scraped Data | Tutorial | Last Updated |
|--------|--------|---------|----------|--------------|
| [Amazon](./amazon-scraper/) | 🟢 Working | • Product data from single pages<br>• Product variants with different sizes<br>• Search results and categories | [Scrape Product Data from Amazon](https://scrape.do/blog/amazon-scraping/) | Aug 13, 2025 |
| [eBay](./ebay-scraper/) | 🟢 Working | • Basic product listings<br>• Product reviews with pagination<br>• Search results with multiple layouts<br>• Product variants and hidden data | [Scrape Products, Reviews, and Variants from eBay](https://scrape.do/blog/ebay-scraping/) | Aug 1, 2025 |
| [Google Search](./google-search-scraper/) | 🟢 Working | • First page organic results<br>• All paginated organic results<br>• Paid search advertisements<br>• Frequently asked questions<br>• Related search terms | [Scrape Organic Results, Ads, and FAQs from Google](https://scrape.do/blog/scraping-google-search-results/) | Jun 23, 2025 |
| [Instagram](./instagram-scraper/) | 🟢 Working | • Profile information and bio<br>• Top 12 recent posts<br>• Individual post details<br>• Post comments and replies | [Scrape Profiles, Posts, and Comments from Instagram](https://scrape.do/blog/instagram-scraping/) | May 30, 2025 |
| [G2](./g2-scraper/) | 🟢 Working | • Company and product data<br>• Product reviews<br>• Search results and categories | [Scrape Company Data and Reviews from G2](https://scrape.do/blog/g2-scraping/) | Aug 5, 2025 |
| [DoorDash](./doordash-scraper/) | 🟢 Working | • Consumer address registration<br>• Restaurant and store listings<br>• Category-specific products<br>• Full menu catalogs | [Scrape Restaurants, Products, and Menus from DoorDash](https://scrape.do/blog/doordash-scraping/) | Jul 17, 2025 |
| [Best Buy](./bestbuy-scraper/) | 🟢 Working | • Product listings with Selenium<br>• Product data with cloud rendering | [Scrape Products from Best Buy](https://scrape.do/blog/best-buy-scraping/) | Jul 9, 2025 |
| [Uber Eats](./ubereats-scraper/) | 🟢 Working | • Store listings via API<br>• Store listings via frontend<br>• Restaurant menus<br>• Chain store products | [Scrape Stores, Menus, and Products from Uber Eats](https://scrape.do/blog/ubereats-scraping/) | Aug 1, 2025 |
| [Zillow](./zillow-scraper/) | 🟢 Working | • Property listing details<br>• Pricing and market data | [Scrape Property Data from Zillow](https://scrape.do/blog/zillow-scraping/) | Aug 5, 2025 |
| [Naver](./naver-scraper/) | 🟢 Working | • E-commerce product pages<br>• Product data via API<br>• Paid search advertisements<br>• Organic search results<br>• Image search results | [Scrape Products and Search Results from Naver](https://scrape.do/blog/naver-scraping/) | Sep 1, 2025 |
| [Chewy](./chewy-scraper/) | 🟢 Working | • Pet product information<br>• Names and pricing | [Scrape Pet Products from Chewy](https://scrape.do/blog/chewy-scraping/) | Aug 5, 2025 |
| [Mouser](./mouser-scraper/) | 🟢 Working | • Electronic component data<br>• Product names and pricing | [Scrape Electronic Components from Mouser](https://scrape.do/blog/mouser-scraping/) | Aug 5, 2025 |
| [Fnac](./fnac-scraper/) | 🟢 Working | • French retail product data<br>• Names and pricing | [Scrape Products from Fnac](https://scrape.do/blog/fnac-scraping/) | Aug 5, 2025 |
| [Ubersuggest](./ubersuggest-scraper/) | 🟢 Working | • Bearer token generation<br>• Keyword overview data<br>• SERP results<br>• Automated keyword analysis | [Scrape Keyword Data from Ubersuggest](https://scrape.do/blog/ubersuggest-scraping/) | Jun 23, 2025 |
| [Zomato](./zomato-scraper/) | 🟢 Working | • Restaurant information<br>• Delivery menu data | [Scrape Restaurant Data from Zomato](https://scrape.do/blog/zomato-scraping/) | Jul 2, 2025 |
| [Allegro](./allegro-scraper/) | 🟢 Working | • Polish e-commerce products<br>• Names, pricing, and ratings | [Scrape Products from Allegro](https://scrape.do/blog/allegro-scraping/) | Aug 5, 2025 |
| [AUTODOC](./AUTODOC-scraper/) | 🟢 Working | • Automotive parts data<br>• Product details and pricing | [Scrape Auto Parts from AUTODOC](https://scrape.do/blog/autodoc-de-scraping/) | Aug 5, 2025 |
| [AutoScout24](./autoscout24-scraper/) | 🟢 Working | • Car listing information<br>• Vehicle names and pricing | [Scrape Car Listings from AutoScout24](https://scrape.do/blog/autoscout24-scraping/) | Aug 5, 2025 |
| [Idealista](./idealista-scraper/) | 🟢 Working | • Spanish real estate listings<br>• Property details, pricing, and location data<br>• Search results with pagination | [Scrape Property Data from Idealista](https://scrape.do/blog/idealista-scraping/) | Aug 6, 2025 |
| [FastPeopleSearch](./fastpeoplesearch-scraper/) | 🟢 Working | • Person information lookup<br>• Names, ages, and addresses | [Scrape People Data from FastPeopleSearch](https://scrape.do/blog/fast-people-search-scraping/) | Aug 5, 2025 |
| [HungerStation](./hungerstation-scraper/) | 🟢 Working | • Restaurant listings<br>• Store menu items | [Scrape Restaurants and Menus from HungerStation](https://scrape.do/blog/hunger-station-scraping/) | Jul 17, 2025 |
| [Imovelweb](./imovelweb-scraper/) | 🟢 Working | • Brazilian real estate data<br>• Property details and pricing | [Scrape Properties from Imovelweb](https://scrape.do/blog/imovelweb-scraping/) | Aug 5, 2025 |
| [Klium](./klium-scraper/) | 🟢 Working | • Tool and equipment data<br>• Product names, pricing, and stock | [Scrape Tools from Klium](https://scrape.do/blog/klium-scraping/) | Aug 5, 2025 |
| [MSC Direct](./mscdirect-scraper/) | 🟢 Working | • Industrial supply products<br>• Brand, names, and pricing | [Scrape Industrial Supplies from MSC Direct](https://scrape.do/blog/mscdirect-scraping/) | Aug 5, 2025 |
| [TicketMaster](./ticketmaster-scraper/) | 🟢 Working | • Event details and schedules<br>• Dates, venues, and locations | [Scrape Events from TicketMaster](https://scrape.do/blog/ticketmaster-scraping/) | Aug 5, 2025 |
| [TruePeopleSearch](./truepeoplesearch-scraper/) | 🟢 Working | • Person information lookup<br>• Names, addresses, and contacts | [Scrape People Data from TruePeopleSearch](https://scrape.do/blog/true-people-search-scraping/) | Aug 5, 2025 |
| [Walmart](./walmart-scraper/) | 🟢 Working | • Individual product details with store-specific pricing<br>• Product variations (sizes, colors, packs)<br>• Category pages with pagination<br>• Price and stock change tracking | [Scrape Complete Grocery Data from Walmart](https://scrape.do/blog/walmart-scraping/) | Sep 2, 2025 |
| [Zoro](./zoro-scraper/) | 🟢 Working | • Industrial business supplies<br>• Product names and manufacturer data | [Scrape Business Supplies from Zoro](https://scrape.do/blog/zoro-scraping/) | Aug 5, 2025 |
| [Cineworld](./cineworld-scraper/) | 🟢 Working | • Movie screenings and showtimes<br>• Ticket prices for all screening types | [Scrape Screenings and Ticket Prices from Cineworld](https://scrape.do/blog/cineworld-scraping/) | Aug 27, 2025 |
| [Regmovies](./regmovies-scraper/) | 🟢 Working | • Regal Cinemas movie screenings<br>• Ticket prices and availability | [Scrape Screenings and Ticket Prices from Regmovies](https://scrape.do/blog/regmovies-com-scraping/) | Aug 27, 2025 |

