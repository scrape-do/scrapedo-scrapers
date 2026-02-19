import json
import html
import re
import urllib.parse

import requests


TOKEN = "<your-token>"

# Paste the full /async/oapv URL you copied from the browser here:
DETAIL_URL = "https://www.google.com/async/oapv?vet=12ahUKEwio5-WcwJ6RAxW2D1kFHUirKSs4FBD0yAR6BAgvECc..i&ved=2ahUKEwio5-WcwJ6RAxW2D1kFHUirKSs4FBCuiAZ6BAgvEBE&bl=TpiC&s=web&opi=95576897&sca_esv=b46502feac7af8df&udm=28&yv=3&ei=a6UuaeiFFraf5NoPyNam2QI&currentpv=1&q=wireless+gaming+headset&async_context=PV_OPEN&pvorigin=3&cs=1&async=catalogid:13769275119917897627,gpcid:15623829887498710473,headlineOfferDocid:2786845769671092314,rds:PC_15623829887498710473%7CPROD_PC_15623829887498710473,imageDocid:6663907422662909808,pvo:3,isp:true,ei:U6UuadjWMvvn5NoPkpmDiAU,localAnnotatedOfferDocid:2786845769671092314,vw:1343,query:wireless%20gaming%20headset,gl:0,pvt:hg,_fmt:jspb"

def scrape_do(url: str, session: requests.Session) -> requests.Response:
    """Route requests through Scrape.do API to bypass blocks."""
    api_url = f"http://api.scrape.do/?token={TOKEN}&url={urllib.parse.quote(url)}"
    r = session.get(api_url)
    r.raise_for_status()
    return r


def find_image_urls(node):
    """
    Recursively search a JSON-like structure (dict/list/str)
    for strings that look like image URLs.
    """
    candidates = set()

    def _walk(value):
        if isinstance(value, dict):
            for v in value.values():
                _walk(v)
        elif isinstance(value, list):
            for v in value:
                _walk(v)
        elif isinstance(value, str):
            text = value.strip()
            if text.startswith("http"):
                # Skip tiny favicon-style images
                if "favicon" in text.lower():
                    return
                if re.search(r"\.(jpg|jpeg|png|webp)(\?|$)", text, re.IGNORECASE) or "gstatic.com" in text:
                    candidates.add(text)

    _walk(node)
    return sorted(candidates)


def parse_product_details(response_text: str):
    """Parse detailed product information from API response."""
    details = {
        "brand": None,
        "rating": None,
        "review_count": None,
        "description": None,
        "detail_images": [],
        "reviews": [],
        "forums": [],
        "offers": []
    }

    try:
        text = response_text.lstrip(")]}'\n ")
        data = json.loads(text)

        # Collect first few image URLs from the entire detail payload.
        all_images = find_image_urls(data)
        details["detail_images"] = all_images[:5]

        if isinstance(data, dict):
            product_result = data.get("ProductDetailsResult")
            if product_result and isinstance(product_result, list) and len(product_result) > 0:

                # Brand
                if len(product_result) > 2 and product_result[2]:
                    details["brand"] = product_result[2]

                # Rating info
                if len(product_result) > 3 and product_result[3] and isinstance(product_result[3], list):
                    rating_info = product_result[3]
                    if len(rating_info) > 0:
                        details["review_count"] = str(rating_info[0])
                    if len(rating_info) > 1:
                        details["rating"] = str(rating_info[1])

                # Description
                if len(product_result) > 5 and product_result[5]:
                    if isinstance(product_result[5], list) and len(product_result[5]) > 0:
                        desc = product_result[5][0]
                        if desc and isinstance(desc, str):
                            details["description"] = desc
                    elif isinstance(product_result[5], str):
                        details["description"] = product_result[5]

                # Forum discussions
                if len(product_result) > 17 and product_result[17] and isinstance(product_result[17], list):
                    forums_data = product_result[17]
                    for forum in forums_data:
                        if isinstance(forum, list) and len(forum) > 2:
                            forum_obj = {
                                "rating": forum[0] if len(forum) > 0 else None,
                                "url": forum[1] if len(forum) > 1 else None,
                                "source": forum[2] if len(forum) > 2 else None,
                                "description": forum[3] if len(forum) > 3 else None,
                                "title": forum[4] if len(forum) > 4 else None
                            }
                            details["forums"].append(forum_obj)

                # Extract offers
                def extract_offer(offer, from_comparison: bool = False):
                    if isinstance(offer, list) and len(offer) > 29:
                        price = offer[9] if len(offer) > 9 else None
                        currency = offer[10] if len(offer) > 10 else "USD"
                        original_price = None

                        # Extract original price
                        if len(offer) > 27 and offer[27] and isinstance(offer[27], list):
                            for price_data in offer[27]:
                                if isinstance(price_data, list) and len(price_data) > 2:
                                    nested = price_data[2]
                                    if isinstance(nested, list):
                                        for price_item in nested:
                                            if isinstance(price_item, list) and len(price_item) > 6:
                                                orig = price_item[6]
                                                if isinstance(orig, int) and orig > 1000000:
                                                    original_price = orig
                                                    break

                        # Extract seller name
                        seller_name = None
                        if from_comparison and len(offer) > 1 and isinstance(offer[1], list) and len(offer[1]) >= 2:
                            seller_name = offer[1][0]
                        else:
                            if len(offer) > 29 and offer[29]:
                                url = offer[29]
                                match = re.search(r'https?://(?:www\.)?([^/]+)', url)
                                if match:
                                    domain = match.group(1)
                                    seller_name = domain.replace('.com', '').replace('.', ' ').title()

                        # Get URL
                        url = None
                        if from_comparison and len(offer) > 2 and isinstance(offer[2], list) and len(offer[2]) > 0:
                            url = offer[2][0]
                        elif len(offer) > 29:
                            url = offer[29]

                        return {
                            "price": f"${price / 1000000:.2f}" if price else None,
                            "currency": currency,
                            "original_price": f"${original_price / 1000000:.2f}" if original_price else None,
                            "title": offer[28] if len(offer) > 28 else None,
                            "url": url,
                            "seller_name": seller_name,
                            "rating": offer[18] if len(offer) > 18 else None,
                            "review_count": offer[19] if len(offer) > 19 else None
                        }
                    return None

                # Main offers at index 37
                if len(product_result) > 37 and product_result[37] and isinstance(product_result[37], list):
                    if len(product_result[37]) > 6 and product_result[37][6]:
                        offers_section = product_result[37][6]
                        if isinstance(offers_section, list):
                            for offer in offers_section:
                                offer_obj = extract_offer(offer, from_comparison=False)
                                if offer_obj:
                                    details["offers"].append(offer_obj)

                # Comparison offers at index 81
                if len(product_result) > 81 and product_result[81] and isinstance(product_result[81], list):
                    if len(product_result[81]) > 0 and product_result[81][0]:
                        compare_section = product_result[81][0]
                        if isinstance(compare_section, list) and len(compare_section) > 0:
                            variants = compare_section[0]
                            if isinstance(variants, list):
                                for variant in variants:
                                    if isinstance(variant, list) and len(variant) > 26 and variant[26]:
                                        variant_offers = variant[26]
                                        if isinstance(variant_offers, list):
                                            for offer in variant_offers:
                                                offer_obj = extract_offer(offer, from_comparison=True)
                                                if offer_obj:
                                                    details["offers"].append(offer_obj)

                # Deduplicate offers by URL
                seen_offer_urls = set()
                unique_offers = []
                for offer in details["offers"]:
                    offer_url = offer.get("url")
                    if offer_url and offer_url not in seen_offer_urls:
                        seen_offer_urls.add(offer_url)
                        unique_offers.append(offer)
                    elif not offer_url:
                        unique_offers.append(offer)

                details["offers"] = unique_offers

                # Extract customer reviews from index 99
                if len(product_result) > 99 and product_result[99] and isinstance(product_result[99], list):
                    if len(product_result[99]) > 2 and product_result[99][2] and isinstance(product_result[99][2], list):
                        if len(product_result[99][2]) > 1 and product_result[99][2][1] and isinstance(product_result[99][2][1], list):
                            if len(product_result[99][2][1]) > 0 and isinstance(product_result[99][2][1][0], list):
                                reviews_container = product_result[99][2][1][0]
                                for review_data in reviews_container[:10]:
                                    if isinstance(review_data, list) and len(review_data) > 6:
                                        review_text = review_data[2] if len(review_data) > 2 else None
                                        if review_text and review_text.strip():
                                            review_obj = {
                                                "text": review_text,
                                                "source": review_data[3] if len(review_data) > 3 else None,
                                                "author": review_data[4] if len(review_data) > 4 else None,
                                                "rating": review_data[5] if len(review_data) > 5 else None,
                                                "date": review_data[6] if len(review_data) > 6 else None,
                                                "review_id": review_data[11] if len(review_data) > 11 else None
                                            }
                                            details["reviews"].append(review_obj)

    except (json.JSONDecodeError, IndexError, TypeError, KeyError) as e:
        print(f"[detail] Error parsing product details: {e}")

    return details


def main():
    if not DETAIL_URL or DETAIL_URL.startswith("<PASTE"):
        raise SystemExit("Please paste a valid /async/oapv detail URL into DETAIL_URL before running.")

    session = requests.Session()

    print("Fetching product detail response via Scrape.do...")
    resp = scrape_do(DETAIL_URL, session)

    # Strip the CSRF protection prefix and parse JSON
    text = resp.text.lstrip(")]}'\n ")
    data = json.loads(text)

    # Use parser to extract structured details
    details = parse_product_details(resp.text)

    print("\n=== Parsed Product Details (single product) ===")
    print(json.dumps(details, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()


