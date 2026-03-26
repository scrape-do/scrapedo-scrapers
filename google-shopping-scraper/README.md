# Google Shopping Scraper

Scrape product listings, detailed specs, seller offers, and customer reviews from Google Shopping. These scripts reverse-engineer Google's async pagination and the hidden `/async/oapv` product detail endpoint to get data that never appears in the initial HTML. Uses [Scrape.do](https://scrape.do) for proxy rotation and anti-bot bypass.

[Find the full technical guide here. 📘](https://scrape.do/blog/google-shopping-scraping/)

## What's Included

* `searchResults.py`: Scrapes product cards from Google Shopping search with async pagination — title, price, image, seller, rating, reviews. Handles session token extraction, hex-escaped responses, and deduplication. Saves to CSV.
* `singleProductDetail.py`: Parses a single `/async/oapv` response for brand, description, images, reviews, forums, and seller offers. Also used as a module by `consistentScraper.py`.
* `consistentScraper.py`: The full pipeline — multi-pass search extraction, then fetches extended details for every product with available `data-*` attributes. Outputs a uniform JSON schema regardless of whether detail data was available.
* `serpApiShopping.py`: Calls Scrape.do's AI Mode API for AI-generated product recommendations, shopping results, and references.

## Requirements

- Python 3.7+
- `requests` and `beautifulsoup4`<br>`pip install requests beautifulsoup4`
- A [Scrape.do API token](https://dashboard.scrape.do/signup) (free 1000 credits/month)

---

## How to Use: `searchResults.py`

1. Set your token and query (via script or env var):

   ```python
   SCRAPE_DO_TOKEN = "<your_token>"
   QUERY = "wireless gaming headset"
   ```

2. Run: `python searchResults.py`

Output → `google_shopping_search.csv` with title, price, image_url, seller_name, rating, review_count.

## How to Use: `singleProductDetail.py`

1. Copy a `/async/oapv` URL from Chrome DevTools (Network tab → click a product → find the `oapv` request):

   ```python
   SCRAPE_DO_TOKEN = "<your_token>"
   DETAIL_URL = "https://www.google.com/async/oapv?..."
   ```

2. Run: `python singleProductDetail.py`

Prints parsed product details (brand, rating, description, offers, reviews, forums) as JSON.

## How to Use: `consistentScraper.py`

1. Set your token and query:

   ```python
   SCRAPE_DO_TOKEN = "<your_token>"
   QUERY = "pc wireless gaming headset"
   ```

   Also configurable via env vars: `SCRAPE_DO_TOKEN`, `GOOGLE_QUERY`, `OUT_JSON`, `MAX_PAGES`, `PAUSE_SECONDS`.

2. Run: `python consistentScraper.py`

Output → `google_shopping_results.json` — each product has card-level fields (title, price, image, seller) plus detail fields when available (brand, description, offers, reviews, forums).

## How to Use: `serpApiShopping.py`

1. Set your token and query:

   ```python
   token = "<your_token>"
   query = "wireless gaming headset"
   ```

2. Run: `python serpApiShopping.py`

Output → `serp-api-shopping-results.json` with AI-curated shopping results, text blocks, and references.

---

## How It Works

### Why the Initial Page Is (Almost) Empty

Google Shopping uses `udm=28` (Universal Design Mode 28). The initial HTML contains a skeleton with barely any products. The real data loads via async JavaScript requests to `/search?async=...`. This is why you can't just parse the HTML — you need to extract session tokens and replay the async requests.

### Session Token Extraction

The initial page response contains three tokens buried in script blocks that you need for pagination:

- **`ei`** — a session identifier from the `kEI` JavaScript variable
- **`basejs`**, **`basecss`**, **`basecomb`** — asset identifiers from the `google.xjs` object

Without these, the async pagination URLs return empty responses.

### The OAPV Endpoint

Detailed product data (brand, reviews, seller offers, forum discussions) lives behind Google's **OAPV** (Open Async Product View) endpoint at `/async/oapv`. Getting there requires five hidden parameters that are embedded in product card `data-*` attributes:

- `catalogid`, `gpcid`, `headlineOfferDocid`, `imageDocid`, `mid`

Not every product card includes all five. Promoted listings and aggregated offers often lack them. `consistentScraper.py` handles both cases — fetching details when available, keeping card-level data when not, and ensuring every product in the output has the same schema.

### Response Format

Google Shopping responses come in two flavors:
- **Async pagination**: JSON-wrapped HTML snippets with hex-encoded characters (`\x3d` → `=`, `\x22` → `"`, etc.) that need unescaping before parsing
- **Product details**: JSPB (JSON Serialized Protocol Buffer) accessed via `ProductDetailsResult`, with data scattered across deeply nested array indices (brand at `[2]`, rating at `[3]`, reviews at `[99]`...)

### Multi-Pass Extraction

`consistentScraper.py` doesn't stop after one pass. Google Shopping surfaces slightly different product slices on each async request, so the script keeps running extraction passes until no new products appear. This consistently surfaces more products than a single-pass approach.

## Watch Out For

- **Empty initial page**: Expected. Products load via async requests — the scripts handle this automatically.
- **Missing `data-*` attributes**: Google doesn't always include the five required detail parameters on every card. Promoted and aggregated listings are especially inconsistent. Card-level data still gets extracted.
- **Expired `ei` tokens**: These are session-specific and short-lived. Don't hardcode async URLs — use the scripts to build them from fresh tokens each run.
- **Fewer products than expected**: Try setting `PAGE_SIZE = 1` to surface more product slices per async page.
- **403/429 errors**: Check your token and credits. Use the `PAUSE_SECONDS` setting to add delays between requests.

---

**Scrape.do** handles proxy rotation, TLS fingerprinting, and anti-bot bypass. [Get your free API token](https://dashboard.scrape.do/signup) (1000 credits/month).
