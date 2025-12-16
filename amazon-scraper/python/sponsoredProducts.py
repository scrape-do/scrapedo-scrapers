import urllib.parse
import json
import re
import requests
from bs4 import BeautifulSoup

# Configuration
token = "<SDO-token>"
search_query = "gaming headsets"  # Change this to any search term
geocode = "us"
zipcode = "10001"

# Build search URL
target_url = f"https://www.amazon.com/s?k={urllib.parse.quote_plus(search_query)}"

# Make API request
targetUrl = urllib.parse.quote(target_url)
apiUrl = "https://api.scrape.do/plugin/amazon/?token={}&url={}&geocode={}&zipcode={}&output=html".format(token, targetUrl, geocode, zipcode)
response = requests.request("GET", apiUrl)

soup = BeautifulSoup(response.text, "html.parser")

# Initialize output structure
sponsored_data = {
    "video_ads": [],
    "in_search": [],
    "carousels": [],
    "featured_brands": []
}

# =============================================================================
# 1. VIDEO ADS - Top featured + VIDEO_SINGLE_PRODUCT
# =============================================================================

# Extract top featured video ad (sb-video-product-collection-desktop)
top_video_widgets = soup.find_all("div", {"cel_widget_id": lambda x: x and "sb-video-product-collection-desktop" in x})
for widget in top_video_widgets:
    try:
        # Find brand and headline
        brand_img = widget.find("img", alt=True)
        brand_name = brand_img.get("alt", "") if brand_img else ""

        headline_elem = widget.find("a", {"data-elementid": "sb-headline"})
        headline = ""
        if headline_elem:
            truncate = headline_elem.find("span", class_="a-truncate-full")
            headline = truncate.text.strip() if truncate else ""

        # Extract products from carousel within video ad
        products = []
        carousel_items = widget.find_all("li", class_="a-carousel-card")
        for item in carousel_items:
            asin_div = item.find("div", {"data-asin": True})
            if asin_div and asin_div.get("data-asin"):
                img = item.find("img")
                products.append({
                    "asin": asin_div.get("data-asin"),
                    "image": img.get("src", "") if img else ""
                })

        sponsored_data["video_ads"].append({
            "type": "top_featured",
            "brand": brand_name,
            "headline": headline,
            "products": products
        })
    except:
        continue

# Extract VIDEO_SINGLE_PRODUCT items
video_single_products = soup.find_all("div", class_=lambda x: x and "VIDEO_SINGLE_PRODUCT" in x)
for video_item in video_single_products:
    try:
        # Get the component props JSON
        component = video_item.find("span", {"data-component-type": "sbv-video-single-product"})
        if component and component.get("data-component-props"):
            props = json.loads(component["data-component-props"])

            # Extract product link and ASIN
            video_link = video_item.find("a", class_="sbv-desktop-video-link")
            href = video_link.get("href", "") if video_link else ""
            asin_match = re.search(r'/dp/([A-Z0-9]{10})', href)

            sponsored_data["video_ads"].append({
                "type": "video_single_product",
                "video_url": props.get("videoSrc", ""),
                "thumbnail": props.get("videoPreviewImageSrc", ""),
                "asin": asin_match.group(1) if asin_match else "",
                "campaign_id": props.get("campaignId", ""),
                "ad_id": props.get("adId", ""),
                "link": href
            })
    except:
        continue

# =============================================================================
# 2. IN-SEARCH ADS - AdHolder with actual ASINs
# =============================================================================

ad_holders = soup.find_all("div", class_=lambda x: x and "AdHolder" in x)
for ad in ad_holders:
    asin = ad.get("data-asin", "")
    # Only process if it has an actual ASIN (not empty)
    if asin and ad.get("data-component-type") == "s-search-result":
        try:
            name_elem = ad.select_one("h2 span")
            name = name_elem.text.strip() if name_elem else ""

            # Price extraction
            try:
                price_elem = ad.select("span.a-price")
                price = str(price_elem).split('a-offscreen">')[1].split('</span>')[0]
            except:
                price = "Price not available"

            link_elem = ad.select_one(".a-link-normal")
            link = link_elem.get("href", "") if link_elem else ""

            img_elem = ad.select_one("img")
            image = img_elem.get("src", "") if img_elem else ""

            if name:
                sponsored_data["in_search"].append({
                    "asin": asin,
                    "name": name,
                    "price": price,
                    "link": link,
                    "image": image
                })
        except:
            continue

# =============================================================================
# 3. CAROUSELS - Themed collection (brand + products)
# =============================================================================

themed_collections = soup.find_all("div", class_=lambda x: x and "sb-desktop" in str(x), id=lambda x: x and "CardInstance" in str(x) if x else False)
# Also try finding by data attribute
if not themed_collections:
    themed_collections = soup.find_all("div", {"data-slot": "desktop-inline"})

for collection in themed_collections:
    try:
        # Skip if it's a video single product (already captured)
        if "VIDEO_SINGLE_PRODUCT" in str(collection.get("class", [])):
            continue

        # Extract brand name
        brand_img = collection.find("img", alt=True)
        brand_name = ""
        if brand_img and brand_img.get("alt"):
            brand_name = brand_img.get("alt")

        # Extract headline
        headline_elem = collection.find("a", {"data-elementid": "sb-headline"})
        headline = ""
        if headline_elem:
            truncate = headline_elem.find("span", class_="a-truncate-full")
            headline = truncate.text.strip() if truncate else ""

        # Extract products from carousel
        products = []
        carousel_items = collection.find_all("li", class_="a-carousel-card")
        for item in carousel_items:
            asin_div = item.find("div", {"data-asin": True})
            if asin_div and asin_div.get("data-asin"):
                img = item.find("img", alt=True)
                products.append({
                    "asin": asin_div.get("data-asin"),
                    "name": img.get("alt", "") if img else "",
                    "image": img.get("src", "") if img else ""
                })

        if brand_name or products:
            sponsored_data["carousels"].append({
                "brand": brand_name,
                "headline": headline,
                "products": products
            })
    except:
        continue

# =============================================================================
# 4. FEATURED BRANDS - "Brands related to your search"
# =============================================================================

# Find multi-brand-creative section
brand_sections = soup.find_all("div", {"cel_widget_id": lambda x: x and "multi-brand-creative-desktop" in x})
for section in brand_sections:
    try:
        # Extract from data-ad-creative-list JSON
        ad_feedback = section.find("div", {"data-ad-creative-list": True})
        if ad_feedback:
            creative_list = json.loads(ad_feedback.get("data-ad-creative-list", "[]"))

            for brand in creative_list:
                # Find corresponding brand card to get image
                brand_name = brand.get("title", "")
                brand_img = section.find("img", alt=brand_name)

                sponsored_data["featured_brands"].append({
                    "brand": brand_name,
                    "campaign_id": brand.get("campaignId", ""),
                    "ad_id": brand.get("adId", ""),
                    "image": brand_img.get("src", "") if brand_img else ""
                })
    except:
        continue

# =============================================================================
# OUTPUT
# =============================================================================

# Print summary
print(f"=== Sponsored Products Summary ===")
print(f"Video Ads: {len(sponsored_data['video_ads'])}")
print(f"In-Search Ads: {len(sponsored_data['in_search'])}")
print(f"Carousels: {len(sponsored_data['carousels'])}")
print(f"Featured Brands: {len(sponsored_data['featured_brands'])}")

# Export to JSON
output_file = "sponsoredProducts.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(sponsored_data, f, indent=2, ensure_ascii=False)

print(f"\nData exported to {output_file}")
