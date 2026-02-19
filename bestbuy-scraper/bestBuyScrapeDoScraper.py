import requests
import urllib.parse
from bs4 import BeautifulSoup
import json
import time
import csv

TOKEN = "<SDO-token>"
BASE_URL = "https://www.bestbuy.com/site/searchpage.jsp?browsedCategory=pcmcat311200050005&cp={cp}&id=pcat17071&st=categoryid%24pcmcat311200050005"
MAX_PAGES = 3

play_with_browser = [
    {
        "action": "WaitSelector",
        "timeout": 30000,
        "waitSelector": "[data-testid='price-block-customer-price']"
    },
    {
        "action": "Execute",
        "execute": (
            "(async()=>{"
            "let h=document.body.scrollHeight,step=400,pos=0;"
            "while(pos<h){window.scrollTo(0,pos);pos+=step;"
            "await new Promise(r=>setTimeout(r,500));"
            "h=document.body.scrollHeight;}"
            "window.scrollTo(0,h);"
            "})();"
        )
    },
    {
        "action": "Wait",
        "timeout": 3000
    },
    {
        "action": "Execute",
        "execute": (
            "(async()=>{"
            "for(let i=0;i<20;i++){"
            "if(!document.querySelector('.skeleton-product-grid-view'))break;"
            "await new Promise(r=>setTimeout(r,500));}"
            "})();"
        )
    },
    {
        "action": "Wait",
        "timeout": 1000
    }
]


def get_products_from_page(cp):
    url = BASE_URL.format(cp=cp)
    jsonData = urllib.parse.quote_plus(json.dumps(play_with_browser))
    api_url = (
        "https://api.scrape.do/?"
        f"url={urllib.parse.quote_plus(url)}"
        f"&token={TOKEN}"
        f"&super=true"
        f"&render=true"
        f"&playWithBrowser={jsonData}"
        f"&blockResources=false"
        f"&setCookies=locDestZip%3D04785%3B%20locStoreId%3D463"
        f"&geoCode=us"
        f"&waitUntil=load"
        f"&timeout=120000"
    )
    response = requests.get(api_url)

    if response.status_code != 200:
        print(f"  HTTP error: {response.status_code}")
        return []

    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    product_items = soup.select('li.product-list-item')
    products = []

    for item in product_items:
        if item.select_one('.skeleton-product-grid-view'):
            continue
        brand = None
        product_title = None
        title_tag = item.select_one('.product-title')
        if title_tag:
            brand_span = title_tag.find('span', class_='first-title')
            if brand_span:
                brand = brand_span.get_text(strip=True)
            full_title = title_tag.get('title') or title_tag.get_text(strip=True)
            if brand and full_title.startswith(brand):
                product_title = full_title[len(brand):].strip(' -\n')
            else:
                product_title = full_title

        img_src = None
        img = item.select_one('img[data-testid="product-image"]')
        if not img:
            img = item.select_one('div.product-image img')
        if img:
            img_src = img.get('src')

        price = None
        price_el = item.select_one('[data-testid="price-block-customer-price"] span')
        if price_el:
            price = price_el.get_text(strip=True)

        rating = None
        rating_el = item.select_one('.c-ratings-reviews p.visually-hidden')
        if rating_el:
            rating = rating_el.get_text(strip=True)

        sku = item.get('data-testid')

        product_url = None
        link = item.select_one('a.product-list-item-link')
        if link:
            href = link.get('href', '')
            if href.startswith('/'):
                product_url = 'https://www.bestbuy.com' + href
            else:
                product_url = href

        products.append({
            'Brand': brand,
            'Product Title': product_title,
            'Image': img_src,
            'Price': price,
            'Rating': rating,
            'SKU': sku,
            'URL': product_url
        })
    return products


def has_valid_data(products):
    """Check that at least some products have actual populated data."""
    for p in products:
        if p.get('Product Title') and p.get('Price'):
            return True
    return False


def main():
    all_products = []
    cp = 1
    while cp <= MAX_PAGES:
        print(f"Scraping page {cp}...")
        attempts = 0
        products = []
        while attempts < 4:
            products = get_products_from_page(cp)
            valid = has_valid_data(products)
            print(f"  Attempt {attempts+1}: Found {len(products)} products, data valid: {valid}")
            if len(products) >= 18 and valid:
                break
            attempts += 1
            if attempts < 4:
                time.sleep(2)

        if not products or len(products) < 1:
            print(f"No products found on page {cp}. Stopping.")
            break
        all_products.extend(products)
        cp += 1
        time.sleep(1)

    print(f"Total products scraped: {len(all_products)}")
    with open('bestbuy_products_scrapedo.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Brand', 'Product Title', 'Image', 'Price', 'Rating', 'SKU', 'URL']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for product in all_products:
            writer.writerow(product)
    print("Products written to bestbuy_products_scrapedo.csv")


if __name__ == "__main__":
    main()
