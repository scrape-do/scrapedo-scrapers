import re
import json
import time
import html
import urllib.parse
import requests
from bs4 import BeautifulSoup
from singleProductDetail import parse_product_details

# -----------------------------
# Config
# -----------------------------
TOKEN = "<your-token>"
QUERY = "pc wireless gaming headset"
SEARCH_URL = f"https://www.google.com/search?q={urllib.parse.quote_plus(QUERY)}&udm=28"

OUT_JSON = "google_shopping_results.json"
PAGE_SIZE = 10
MAX_PAGES = 0  # 0 = unlimited
PAUSE_SECONDS = 1.0

# -----------------------------
# HTTP helper
# -----------------------------
def scrape_do(url: str, session: requests.Session) -> requests.Response:
    api = f"http://api.scrape.do/?token={TOKEN}&url={urllib.parse.quote(url)}"
    r = session.get(api)
    r.raise_for_status()
    return r

# -----------------------------
# Parsing helpers
# -----------------------------
def extract_product_data(soup: BeautifulSoup, ei=None):
    """
    Parse products from udm=28 layout.
    Returns (list of products, total_found_count).
    """
    products = []
    seen_veds = set()
    total_found = 0

    for group in soup.select(".MjjYud"):
        for card in group.select(".Ez5pwe"):
            clickable_area = card.select_one('div[data-ved]')
            if not clickable_area:
                continue

            ved = clickable_area.get('data-ved')
            if not ved or ved in seen_veds:
                continue
            seen_veds.add(ved)

            title_tag = card.select_one(".gkQHve.SsM98d.RmEs5b")
            title = title_tag.get_text(strip=True) if title_tag else None

            price_tag = card.select_one(".lmQWe")
            price = price_tag.get_text(strip=True) if price_tag else None

            if not title or not price:
                continue
            
            total_found += 1

            image_url = "N/A"
            img = card.select_one("img.VeBrne")
            if not img:
                img = card.select_one("img.nGT6qb")
            if img:
                for attr in ("src", "data-src", "data-jslayout-progressive-load"):
                    if img.has_attr(attr):
                        attr_value = img[attr]
                        if (not attr_value.startswith("data:image") and
                            (attr_value.startswith("http") or attr_value.startswith("//"))):
                            image_url = attr_value
                            break

            # Extract seller name
            seller_name = "N/A"
            seller_span = card.select_one("span.WJMUdc.rw5ecc")
            if seller_span:
                seller_name = seller_span.get_text(strip=True)

            # Extract rating
            rating = None
            rating_span = card.select_one("span.yi40Hd.YrbPuc")
            if rating_span:
                rating = rating_span.get_text(strip=True)

            # Extract review count
            review_count = None
            review_span = card.select_one("span.RDApEe.YrbPuc")
            if review_span and review_span.name == "span":
                review_text = review_span.get_text(strip=True)
                if review_text and len(review_text) < 20:
                    review_match = re.search(r'\(([0-9.]+[KM]?)\)', review_text)
                    if review_match:
                        review_count = review_match.group(1)
                    elif re.match(r'^[0-9.]+[KM]?$', review_text):
                        review_count = review_text
            
            link = "N/A"
            
            # Try to extract product detail parameters from data attributes.
            # Google may or may not embed these; when present they enable
            # fetching richer detail via the OAPV endpoint.
            product_params = None
            product_container = (
                card.select_one('[data-cid]') or
                card.select_one('.MtXiu') or
                card.select_one('.shntl') or
                card.select_one('.sh-dgr__content')
            )
            if not product_container and card.get('data-cid'):
                product_container = card

            if product_container:
                catalogid = product_container.get('data-cid')
                gpcid = product_container.get('data-gid')
                headline_offer_docid = product_container.get('data-oid')
                image_docid = product_container.get('data-iid')
                mid = product_container.get('data-mid')
                rds = product_container.get('data-rds')
                
                if all([catalogid, gpcid, headline_offer_docid, image_docid, mid]):
                    product_params = {
                        "catalogid": catalogid,
                        "gpcid": gpcid,
                        "headlineOfferDocid": headline_offer_docid,
                        "imageDocid": image_docid,
                        "mid": mid,
                        "rds": rds or "",
                        "ei": ei,
                        "ved": ved
                    }

            products.append({
                "title": title,
                "price": price,
                "link": link,
                "image_url": image_url,
                "seller_name": seller_name,
                "rating": rating,
                "review_count": review_count,
                "product_params": product_params
            })
            
    return products, total_found

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

def parse_async_batch(snippets, ei=None):
    products = []
    total_found = 0
    for snip in snippets:
        soup = BeautifulSoup(snip, "html.parser")
        batch_products, batch_total = extract_product_data(soup, ei)
        products.extend(batch_products)
        total_found += batch_total
    return products, total_found

def build_product_detail_url(params: dict, query: str):
    """Build URL for product detail popup."""
    if not params:
        return None
    
    required = ['catalogid', 'gpcid', 'headlineOfferDocid', 'imageDocid', 'mid']
    if not all(params.get(key) for key in required):
        return None
    
    async_parts = [
        f"catalogid:{params['catalogid']}",
        f"gpcid:{params['gpcid']}",
        f"headlineOfferDocid:{params['headlineOfferDocid']}",
        f"imageDocid:{params['imageDocid']}",
        f"mid:{params['mid']}",
    ]
    
    if params.get('rds'):
        async_parts.append(f"rds:{params['rds']}")
    
    async_parts.extend([
        "pvo:3",
        "isp:true",
        f"query:{urllib.parse.quote(query)}",
        "gl:0",
        "pvt:hg",
        "_fmt:jspb"
    ])
    
    if params.get('ei'):
        async_parts.append(f"ei:{params['ei']}")
    
    async_param = ",".join(async_parts)
    
    url_params = {
        "udm": "28",
        "yv": "3",
        "currentpv": "1",
        "q": query,
        "async_context": "PV_OPEN",
        "pvorigin": "3",
        "cs": "0",
        "async": async_param,
    }
    
    if params.get('ved'):
        url_params["ved"] = params['ved']
    if params.get('ei'):
        url_params["ei"] = params['ei']
    
    return "https://www.google.com/async/oapv?" + urllib.parse.urlencode(url_params, safe=":,_")



def fetch_product_details(session: requests.Session, params: dict, query: str):
    """Fetch detailed product information."""
    if not params:
        return None
    
    detail_url = build_product_detail_url(params, query)
    if not detail_url:
        return None
    
    try:
        resp = scrape_do(detail_url, session)
        details = parse_product_details(resp.text)
        return details
    except Exception as e:
        print(f"[detail] Error fetching product details: {e}")
        return None

# -----------------------------
# Main
# -----------------------------
def run_extraction(session, existing_products=None):
    """
    Run a single product extraction pass.
    
    Args:
        session: requests.Session
        existing_products: dict keyed by (title, price) of products already found
    
    Returns:
        tuple: (new_products_dict, new_count) where new_products_dict is dict of products found in this pass,
               and new_count is number of new products added
    """
    if existing_products is None:
        existing_products = {}
    
    print("\n[extraction] Starting...")
    
    # Initial page: only used to extract tokens required for async pagination.
    # We intentionally do NOT parse products from this HTML, to keep all
    # product collection consistent with the async responses.
    r = scrape_do(SEARCH_URL, session)
    soup = BeautifulSoup(r.content, "html.parser")

    # Extract tokens for async pagination
    ei, basejs, basecss, basecomb = extract_tokens_from_initial(r.text, soup)

    # Products found in this pass
    pass_products = {}
    total_all = 0

    consecutive_empty_pages = 0
    page_limit = MAX_PAGES if MAX_PAGES > 0 else 999
    
    for page_idx in range(0, page_limit + 1):
        start = PAGE_SIZE * page_idx

        # Try async endpoint
        async_url = build_async_url(ei, basejs, basecss, basecomb, QUERY, start)
        try:
            snippets = fetch_async_snippets(session, async_url)
        except requests.HTTPError as e:
            snippets = []

        new_batch, page_total = parse_async_batch(snippets, ei) if snippets else ([], 0)

        # Fallback to plain page
        if not new_batch:
            plain_url = f"https://www.google.com/search?q={urllib.parse.quote_plus(QUERY)}&udm=28&start={start}"
            try:
                r2 = scrape_do(plain_url, session)
                new_batch, page_total = extract_product_data(BeautifulSoup(r2.content, "html.parser"), ei)
            except requests.HTTPError:
                new_batch, page_total = [], 0

        # Add all products (with or without detail params)
        page_added = 0
        with_params = 0
        for p in new_batch:
            key = (p["title"], p["price"])
            if key not in existing_products and key not in pass_products:
                pass_products[key] = p
                page_added += 1
                if p.get("product_params"):
                    with_params += 1

        total_all += page_total

        print(f"[page {page_idx + 1}] found {page_total} products, {page_added} new ({with_params} with detail params)")
        
        # Stopping logic: stop after 3 consecutive pages that return no products at all.
        # We deliberately look at page_total (not page_added) so that we keep
        # going through pages even if they only contain products we've already seen.
        if page_total == 0:
            consecutive_empty_pages += 1
            if consecutive_empty_pages >= 3:
                break
        else:
            consecutive_empty_pages = 0

        time.sleep(PAUSE_SECONDS)
    
    new_count = len(pass_products)
    print(f"[extraction] Found {new_count} new products in this pass")
    
    return pass_products, new_count

def main():
    session = requests.Session()

    print(f"[scraper] Starting Google Shopping scraper")
    print(f"[scraper] Query: {QUERY}")
    print(f"[scraper] Max pages: {MAX_PAGES if MAX_PAGES > 0 else 'unlimited'}")
    
    # Multi-run extraction: keep running until no new products found
    all_products_dict = {}
    run_index = 0
    
    while True:
        run_index += 1
        
        print(f"\n{'='*80}")
        print(f"[scraper] Extraction run #{run_index}")
        print(f"{'='*80}")
        
        pass_products, new_count = run_extraction(session, all_products_dict)
        
        # Merge new products into global dict
        for key, product in pass_products.items():
            all_products_dict[key] = product
        
        print(f"[scraper] Run #{run_index} complete: {new_count} new products, {len(all_products_dict)} total")
        
        # Stop when no new products found
        if new_count == 0:
            print(f"[scraper] No new products found in run #{run_index}, stopping multi-run extraction")
            break
        
        time.sleep(PAUSE_SECONDS)
    
    all_products = list(all_products_dict.values())
    
    print(f"\n[scraper] Extraction summary:")
    print(f"[scraper] Total unique products: {len(all_products)}")
    print(f"[scraper] Total extraction runs: {run_index}")

    # Count how many have detail params for OAPV fetching
    products_with_params = [p for p in all_products if p.get("product_params")]
    products_without_params = [p for p in all_products if not p.get("product_params")]

    # 4) Fetch detailed information for products that have valid params
    if products_with_params:
        print(f"\n[details] Fetching detailed information for {len(products_with_params)} products with detail params...")
        success_count = 0
        
        for idx, product in enumerate(products_with_params):
            print(f"[details] {idx + 1}/{len(products_with_params)}: {product['title'][:60]}...")
            
            details = fetch_product_details(session, product["product_params"], QUERY)
            
            if details:
                product.update(details)
                success_count += 1
            
            time.sleep(PAUSE_SECONDS / 2)
        
        print(f"[details] Summary: {success_count}/{len(products_with_params)} successful")
    else:
        print(f"\n[details] No products have detail params for OAPV fetching (Google may have changed their HTML structure)")
        print(f"[details] Basic product data (title, price, image, seller, rating, reviews) was still extracted from cards")

    # Ensure uniform schema: every product gets the same set of keys
    # so downstream consumers see a consistent structure.
    detail_defaults = {
        "brand": None,
        "rating": None,
        "review_count": None,
        "description": None,
        "detail_images": [],
        "reviews": [],
        "forums": [],
        "offers": []
    }
    for product in all_products:
        for key, default in detail_defaults.items():
            product.setdefault(key, default)
        product.pop("product_params", None)

    # 5) Export to JSON
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(all_products, f, ensure_ascii=False, indent=2)

    print(f"\n[scraper] Done! Scraped {len(all_products)} unique products")
    print(f"[scraper] Saved: {OUT_JSON}")
    
    # Print summary
    total_offers = sum(len(p.get("offers", [])) for p in all_products)
    total_reviews = sum(len(p.get("reviews", [])) for p in all_products)
    total_forums = sum(len(p.get("forums", [])) for p in all_products)
    products_with_desc = sum(1 for p in all_products if p.get("description"))
    
    print(f"[scraper] Total offers: {total_offers}")
    print(f"[scraper] Total reviews: {total_reviews}")
    print(f"[scraper] Total forums: {total_forums}")
    print(f"[scraper] Products with descriptions: {products_with_desc}/{len(all_products)}")

if __name__ == "__main__":
    main()
