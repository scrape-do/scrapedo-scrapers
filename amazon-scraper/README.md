# Amazon Scraper

A comprehensive Amazon scraping toolkit powered by [Scrape.do](https://scrape.do). Extract product data, search results, reviews, seller offers, and more from Amazon with ready-to-use scripts in Python, Node.js, and cURL.

> **Note:** The Python and Node.js scripts can work without Scrape.do. If you have your own headless browser setup with rotating proxies and proper headers, simply replace the API URL with your direct Amazon request. The parsing logic will work the same way.

## Features

| Scraper | Description | Output |
|---------|-------------|--------|
| **searchResults** | Scrape product listings from search queries | CSV |
| **singleProduct** | Extract detailed product information by ASIN | CSV |
| **productVariations** | Recursively scrape all color/size variations | CSV |
| **reviews** | Extract customer reviews for any product | CSV |
| **bestSellers** | Scrape best seller rankings by category | CSV |
| **sellerOffers** | Get all seller listings for a product | CSV |
| **sponsoredProducts** | Extract sponsored ads from search results | JSON |
| **relatedSearches** | Get related search suggestions | Terminal |

## Tutorials

For detailed step-by-step guides on how each scraper works:

- [How to Scrape Amazon Product Pages](https://scrape.do/blog/amazon-scraping/) - PDP, seller offers, and variations
- [How to Scrape Amazon Search Results](https://scrape.do/blog/scrape-amazon-search/) - Search results, related searches, and sponsored products
- [How to Scrape Amazon Best Sellers](https://scrape.do/blog/scrape-amazon-best-sellers/) - Best seller rankings by category
- [How to Scrape Amazon Reviews](https://scrape.do/blog/scrape-amazon-reviews/) - Product reviews (includes technical guidelines for authenticated scraping, though large-scale or commercial use behind login is prohibited)
- [Best Amazon Scraper APIs Compared](https://scrape.do/blog/best-amazon-scraper-api/) - Performance benchmarks of top Amazon scraping APIs

## Quick Start

### Python

```bash
cd python
pip install -r ../requirements.txt
python searchResults.py
```

### Node.js

```bash
cd node.js
npm install
node searchResults.js
```

### cURL (Scrape.do Ready API)

```bash
cd "cURL(ready-API)"
bash search.sh
```

## Configuration

Each script has a configuration section at the top. Update the token and parameters as needed:

```python
# Python
token = "<SDO-token>"
asin = "B07TCJS1NS"  # Change this to any product ASIN
geocode = "us"
zipcode = "10001"
```

```javascript
// Node.js
const token = "<SDO-token>";
const asin = "B07TCJS1NS"; // Change this to any product ASIN
const geocode = "us";
const zipcode = "10001";
```

## Scrape.do Amazon API Endpoints

The `cURL(ready-API)` folder contains scripts that use Scrape.do's structured Amazon API endpoints:

### Product Detail Page (PDP)
```
GET https://api.scrape.do/plugin/amazon/pdp
    ?token=<SDO-token>
    &asin=B0C7BKZ883
    &geocode=us
    &zipcode=10001
```

### Search Results
```
GET https://api.scrape.do/plugin/amazon/search
    ?token=<SDO-token>
    &keyword=laptop%20stands
    &geocode=us
    &zipcode=10001
    &page=1
```

### Seller Offers
```
GET https://api.scrape.do/plugin/amazon/offer-listing
    ?token=<SDO-token>
    &asin=B0DGJ7HYG1
    &geocode=us
    &zipcode=10001
```

## Installation

### Python Requirements
```bash
pip install requests beautifulsoup4
```

### Node.js Requirements
```bash
npm install axios cheerio csv-writer
```

## Usage Examples

### Scrape Search Results (Python)
```bash
python python/searchResults.py
# Output: searchResults.csv
```

### Scrape Product Reviews (Node.js)
```bash
node node.js/reviews.js
# Output: reviews.csv
```

### Get Product Data via API (cURL)
```bash
bash "cURL(ready-API)/pdp.sh"
# Output: output/SDOpdp.json
```

## Output Examples

Sample outputs can be found in [output](output) folder.

## License

MIT - see [LICENSE](LICENSE) for details.

## Links

- [Scrape.do](https://scrape.do)
- [Scrape.do Documentation](https://scrape.do/documentation/)
- [Amazon Scraper API Docs](https://scrape.do/documentation/amazon-scraper-api/)
