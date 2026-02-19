import re
import json
import time
import html
import csv
import urllib.parse
import requests
from bs4 import BeautifulSoup

# Configuration
TOKEN = "<your-token>"
QUERY = "wireless gaming headset"
SEARCH_URL = f"https://www.google.com/search?q={urllib.parse.quote_plus(QUERY)}&udm=28"
PAGE_SIZE = 10
PAUSE_SECONDS = 1.0

# HTTP helper function
def scrape_do(url: str, session: requests.Session) -> requests.Response:
    """Route requests through Scrape.do API to bypass blocks"""
    api_url = f"http://api.scrape.do/?token={TOKEN}&url={urllib.parse.quote(url)}"
    r = session.get(api_url)
    r.raise_for_status()
    return r

# Token extraction for pagination
def extract_tokens_from_initial(html_text: str, soup: BeautifulSoup):
    """Extract tokens needed for async pagination."""
    # ei / kEI
    ei = None
    m = re.search(r"_g=\{kEI:'([^']+)'", html_text)
    if not m:
        m = re.search(r'kEI[:=]\s*[\'"]([^\'"]+)[\'"]', html_text)
    if m:
        ei = m.group(1)

    basejs = basecss = basecomb = None
    for script in soup.find_all("script"):
        text = script.string or ""
        if not text:
            continue
        if "google.xjs" in text:
            obj = re.search(r"google\.xjs\s*=\s*(\{.*?\})", text, re.DOTALL)
            if obj:
                body = obj.group(1)
                pairs = re.findall(r"(\w+)\s*:\s*['\"]([^'\"]+)['\"]", body)
                if pairs:
                    d = {}
                    for k, v in pairs:
                        v = v.replace("\\x3d", "=").replace("\\x22", '"').replace("\\x26", "&")
                        d[k] = v
                    basejs   = d.get("basejs", basejs)
                    basecss  = d.get("basecss", basecss)
                    basecomb = d.get("basecomb", basecomb)
    return ei, basejs, basecss, basecomb

def build_async_url(ei, basejs, basecss, basecomb, q, start):
    """Build URL for async pagination endpoint."""
    arc_id = f"srp_{ei or 'X'}_{start}"
    _id    = f"arc-srp_{ei or 'X'}_{start}"

    async_parts = [
        f"arc_id:{arc_id}",
        "ffilt:all",
        "ve_name:MoreResultsContainer",
        "use_ac:false",
        "inf:1",
        "_pms:s",
        "_fmt:pc",
        f"_id:{_id}",
    ]
    if basejs:   async_parts.append(f"_basejs:{basejs}")
    if basecss:  async_parts.append(f"_basecss:{basecss}")
    if basecomb: async_parts.append(f"_basecomb:{basecomb}")
    async_param = ",".join(async_parts)

    params = {
        "q": q,
        "udm": "28",
        "start": str(start),
        "sa": "N",
        "asearch": "arc",
        "cs": "1",
        "async": async_param,
    }
    return "https://www.google.com/search?" + urllib.parse.urlencode(params, safe=":,_")

def _unescape_google_inline(html_fragment: str) -> str:
    """De-escape Google's inline HTML encoding."""
    def repl(m):
        return chr(int(m.group(1), 16))
    s = re.sub(r"\\x([0-9a-fA-F]{2})", repl, html_fragment)
    return html.unescape(s)

def fetch_async_snippets(session: requests.Session, async_url: str):
    """Fetch and parse async pagination response."""
    resp = scrape_do(async_url, session)
    body = resp.text
    txt = body.lstrip(")]}'\n ")
    snippets = []

    # Try JSON lines format
    json_hits = re.findall(r'^\{.*?"html":.*\}$', txt, flags=re.M | re.S)
    if json_hits:
        for hit in json_hits:
            try:
                data = json.loads(hit)
                h = data.get("html") or ""
                if h:
                    snippets.append(_unescape_google_inline(h))
            except Exception:
                pass

    # Fallback to raw HTML
    if not snippets:
        snippets.append(txt)

    return snippets

def extract_products_from_soup(soup: BeautifulSoup):
    """Extract products from a BeautifulSoup object."""
    products = []
    for group in soup.select(".MjjYud"):
        for card in group.select(".Ez5pwe"):
            # Extract product title
            title_tag = card.select_one(".gkQHve.SsM98d.RmEs5b")
            title = title_tag.get_text(strip=True) if title_tag else None
            
            # Extract price
            price_tag = card.select_one(".lmQWe")
            price = price_tag.get_text(strip=True) if price_tag else None
            
            # Skip products without title or price
            if not title or not price:
                continue
            
            # Extract image URL
            # Images are lazy-loaded with data-deferred="1" and base64 placeholders on initial page
            # Async-loaded products may have different image structure
            # Try VeBrne first (works better for async responses), then fall back to nGT6qb (initial page)
            image_url = "N/A"
            
            # Try VeBrne selector first (better for async-loaded products)
            img = card.select_one("img.VeBrne")
            if not img:
                # Fall back to nGT6qb selector (for initial page products)
                img = card.select_one("img.nGT6qb")
            
            if img:
                # Check for actual image URL in various attributes
                # Skip base64 placeholders - only accept real URLs
                for attr in ("src", "data-src", "data-jslayout-progressive-load"):
                    if img.has_attr(attr):
                        attr_value = img[attr]
                        # Skip base64 data URIs and placeholders
                        if (not attr_value.startswith("data:image") and 
                            not attr_value.startswith("data:image/gif") and
                            (attr_value.startswith("http") or attr_value.startswith("//"))):
                            image_url = attr_value
                            break
            
            # Extract seller name from specific span
            seller_name = "N/A"
            seller_span = card.select_one("span.WJMUdc.rw5ecc")
            if seller_span:
                seller_name = seller_span.get_text(strip=True)
            
            # Extract rating and review count from specific spans
            rating = review_count = None
            rating_span = card.select_one("span.yi40Hd.YrbPuc")
            if rating_span:
                rating = rating_span.get_text(strip=True)
            
            # Extract review count - ensure we get a span, not a link
            review_span = card.select_one("span.RDApEe.YrbPuc")
            if review_span and review_span.name == "span":  # Ensure it's actually a span
                # Get only direct text, not from nested elements (to avoid getting link hrefs)
                review_text = ""
                # Try to get direct string content first
                if review_span.string:
                    review_text = review_span.string.strip()
                else:
                    # Fall back to get_text() but filter out any URL-like content
                    review_text = review_span.get_text(strip=True)
                
                # Validate: skip if it looks like a URL or is suspiciously long
                if review_text and len(review_text) < 20:
                    if not (review_text.startswith("http") or "://" in review_text or 
                            review_text.startswith("www.") or review_text.count("/") > 2):
                        # Extract number from "(1.8K)" format
                        review_match = re.search(r'\(([0-9.]+[KM]?)\)', review_text)
                        if review_match:
                            review_count = review_match.group(1)
                        # Also try direct match if no parentheses (some formats might differ)
                        elif re.match(r'^[0-9.]+[KM]?$', review_text):
                            review_count = review_text
            
            products.append({
                "title": title,
                "price": price,
                "image_url": image_url,
                "seller_name": seller_name,
                "rating": rating,
                "review_count": review_count
            })
    return products

# Main scraping logic
def main():
    session = requests.Session()
    
    # Fetch initial page
    print("Fetching initial page...")
    response = scrape_do(SEARCH_URL, session)
    soup = BeautifulSoup(response.content, "html.parser")

    # Extract tokens for async pagination (we will only use async responses)
    ei, basejs, basecss, basecomb = extract_tokens_from_initial(response.text, soup)
    print(f"Extracted tokens: ei={ei[:20] if ei else None}...")

    # We intentionally do NOT take products from the initial HTML page.
    # Instead, we rely entirely on async responses starting from start=0
    # to keep one unified code path.
    all_products = []
    seen = set()
    print("Starting async pagination from start=0 (no products taken from initial HTML)")

    # Paginate through results
    consecutive_empty_pages = 0
    page_idx = 0

    while consecutive_empty_pages < 3:  # Stop after 3 consecutive empty pages
        start = PAGE_SIZE * page_idx

        print(f"Fetching page {page_idx + 1} (start={start})...")

        # Try async endpoint
        async_url = build_async_url(ei, basejs, basecss, basecomb, QUERY, start)
        try:
            snippets = fetch_async_snippets(session, async_url)
        except requests.HTTPError as e:
            print(f"  Async request failed: {e}")
            snippets = []

        new_products = []
        if snippets:
            # Parse async snippets
            for snip in snippets:
                batch_soup = BeautifulSoup(snip, "html.parser")
                batch_products = extract_products_from_soup(batch_soup)
                new_products.extend(batch_products)

        # Fallback to plain page if async didn't work
        if not new_products:
            plain_url = f"https://www.google.com/search?q={urllib.parse.quote_plus(QUERY)}&udm=28&start={start}"
            try:
                r2 = scrape_do(plain_url, session)
                batch_soup = BeautifulSoup(r2.content, "html.parser")
                new_products = extract_products_from_soup(batch_soup)
            except requests.HTTPError as e:
                print(f"  Fallback request failed: {e}")
                new_products = []

        # Deduplicate
        fresh = [p for p in new_products if (p["title"], p["price"]) not in seen]
        for p in fresh:
            seen.add((p["title"], p["price"]))
        all_products.extend(fresh)

        print(f"  Found {len(fresh)} new products (total: {len(all_products)})")

        if not fresh:
            consecutive_empty_pages += 1
        else:
            consecutive_empty_pages = 0
        page_idx += 1

        time.sleep(PAUSE_SECONDS)

    # Export to CSV
    with open("google_shopping_search.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["title", "price", "image_url", "seller_name", "rating", "review_count"])
        writer.writeheader()
        writer.writerows(all_products)

    print(f"\nExported {len(all_products)} products to google_shopping_search.csv")

if __name__ == "__main__":
    main()

