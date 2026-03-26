# Google Maps Scraper

Extract business listings, place details, and customer reviews from Google Maps without touching a browser. These scripts bypass the rendered map entirely and hit Google's internal protobuf-over-JSON endpoints directly through [Scrape.do](https://scrape.do).

[Find the full technical guide here. 📘](https://scrape.do/blog/google-maps-scraping/)

## What's Included

* `searchScraper.py`: Searches via the `tbm=map` endpoint — returns names, ratings, types, addresses, websites, coordinates, and thumbnails for up to 20 places per request.
* `detailsScraper.py`: Pulls full details for a single place via `/maps/preview/place` — business hours, phone, description, images, and more.
* `reviewsScraper.py`: Fetches customer reviews via `/maps/preview/review/listentitiesreviews` — with sorting (relevant/newest/highest/lowest) and pagination in batches of 10.

## Requirements

* Python 3.7+
* `requests` library<br>`pip install requests`
* A [Scrape.do API token](https://dashboard.scrape.do/signup) (free 1000 credits/month)

## How to Use: `searchScraper.py`

1. Set your search:

   ```python
   TOKEN = "<your_token>"
   SEARCH_QUERY = "museums in paris"
   ```

2. Run: `python searchScraper.py`

Output → `maps_search_results.json`:

```yaml
- name: Musée du Louvre
  feature_id: "0x47e671d8..."
  rating: "4.7"
  review_count: "312849"
  types: ["Art museum", "Museum"]
  address: "Rue de Rivoli, 75001 Paris"
  website: "https://www.louvre.fr"
  latitude: "48.8606"
  longitude: "2.3376"
```

## How to Use: `detailsScraper.py`

1. Grab a `feature_id` from search results (or extract one from a Google Maps URL):

   ```python
   TOKEN = "<your_token>"
   FEATURE_ID = "0x47e66e2eeaaaaaa3:0xdc3fd08aa701960a"
   ```

2. Run: `python detailsScraper.py`

Output → `maps_place_details.json` with name, rating, types, address, phone, website, coordinates, description, hours, and image.

## How to Use: `reviewsScraper.py`

1. Set the feature ID and optionally configure sorting:

   ```python
   TOKEN = "<your_token>"
   FEATURE_ID = "0x47e66e00f9521b7d:0xc8c16b75253918c1"
   SORT_RELEVANT = 1  # 1=relevant, 2=newest, 3=highest, 4=lowest
   OFFSET = 0         # increment by 10 for next page
   ```

2. Run: `python reviewsScraper.py`

Output → `maps_reviews.json` with overall rating, star distribution, and individual reviews (reviewer name, rating, text, language, visit date).

## How It Works

### Protobuf-over-JSON (All Three Scripts)

None of these scripts parse HTML. Google Maps' internal endpoints return data as massive nested JSON arrays — Google's own protobuf-over-JSON serialization format. Every response starts with `)]}'` (anti-XSSI prefix) that needs stripping before parsing.

The `pb` parameter in each request URL acts like a field selector — think of it as a shopping list telling Google which data fields to return. The search scraper uses `!7i20` to request 20 results, while the details scraper requests hours, photos, coordinates, and descriptions.

### Feature IDs: The Glue Between Scripts

Feature IDs like `0x47e66e2eeaaaaaa3:0xdc3fd08aa701960a` connect everything: search → details → reviews. The search scraper extracts them, and you feed them into the other two scripts.

For reviews, there's a fun conversion step: the two hex halves of the feature ID get converted to **signed 64-bit big-endian integers** (via `struct.unpack(">q", ...)`) because the reviews endpoint expects them in `!1y` / `!2y` format inside the `pb` parameter.

### Regex vs Structured Parsing

The search and details scrapers use **regex extraction** against the serialized JSON text — because navigating 15-level-deep nested arrays by index is fragile and unreadable. The reviews scraper takes the structured approach (parsing `data[2]` for reviews, `data[5]` for star distribution) since the review data has a more predictable shape.

### Proxy Setup

All scripts use `super=true` and `geoCode=us` through Scrape.do. No JavaScript rendering needed — these endpoints return raw data, not rendered pages.

## Watch Out For

- **Response doesn't start with `)]}'`**: The request was likely blocked. Double-check your token and that `super=true` is set.
- **Missing fields in details**: Not every place has a phone number, website, or business hours — the script handles `None` values gracefully.
- **Unicode in reviews**: Reviews come in all languages. The script sets `sys.stdout.reconfigure(encoding="utf-8")` for Windows consoles, but pipe output carefully.
- **Pagination**: Reviews come 10 at a time. Bump `OFFSET` by 10 for each page. Rate-limit yourself — Google will notice rapid sequential requests.

## Output Files

| Script | Output | Key Fields |
|--------|--------|------------|
| `searchScraper.py` | `maps_search_results.json` | name, feature_id, rating, review_count, types, address, website, coords, image |
| `detailsScraper.py` | `maps_place_details.json` | name, rating, types, address, phone, website, coords, description, hours, image |
| `reviewsScraper.py` | `maps_reviews.json` | overall_rating, rating_distribution, reviews (reviewer, rating, text, language, visited) |

---

**Scrape.do** handles residential proxies, geo-targeting, and anti-bot bypass so you can focus on parsing. [Get your free API token](https://dashboard.scrape.do/signup) (1000 credits/month).
