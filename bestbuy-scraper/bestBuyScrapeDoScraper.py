import requests
import urllib.parse
from bs4 import BeautifulSoup
import json
import time
import csv

TOKEN = "<your-token>"
BASE_URL = "https://www.bestbuy.com/site/searchpage.jsp?browsedCategory=pcmcat311200050005&cp={cp}&id=pcat17071&st=categoryid%24pcmcat311200050005"

play_with_browser = [
    {
        "action": "WaitSelector",
        "timeout": 25000,
        "waitSelector": "[data-testid='medium-customer-price']"
    },
    {
        "action": "Execute",
        "execute": "setInterval(()=>{window.scrollTo({top:Math.random()*document.body.scrollHeight})},1200);"
    },
    {
        "action": "Click",
        "selector": "#Exclude_Out_of_Stock_Items"
    },
    {
        "action": "Wait",
        "timeout": 3000
    },
    {
        "action": "Click",
        "selector": "#Exclude_Out_of_Stock_Items"
    },
    {
        "action": "Wait",
        "timeout": 2000
    },
    {
        "action": "Execute",
        "execute": "(async()=>{for(;document.querySelector('.a-skeleton-shimmer');)await new Promise(e=>setTimeout(e,700))})();"
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
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    product_items = soup.select('li.product-list-item')
    products = []
    for item in product_items:
        brand = None
        product_title = None
        h2 = item.find('h2', class_='product-title')
        if h2:
            brand_span = h2.find('span', class_='first-title')
            if brand_span:
                brand = brand_span.get_text(strip=True)
            full_title = h2.get_text(strip=True)
            if brand and full_title.startswith(brand):
                product_title = full_title[len(brand):].strip(' -\n')
            else:
                product_title = full_title
        img_src = None
        img = item.select_one('div.product-image.m-100 img')
        if img:
            img_src = img.get('src')
        price = None
        price_div = item.select_one('div.customer-price.medium')
        if price_div:
            price = price_div.get_text(strip=True)
        model = None
        sku = None
        attr_divs = item.select('div.product-attributes div.attribute')
        if len(attr_divs) > 0:
            model_span = attr_divs[0].find('span', class_='value')
            if model_span:
                model = model_span.get_text(strip=True)
        if len(attr_divs) > 1:
            sku_span = attr_divs[1].find('span', class_='value')
            if sku_span:
                sku = sku_span.get_text(strip=True)
        products.append({
            'Brand': brand,
            'Product Title': product_title,
            'Image': img_src,
            'Price': price,
            'Model': model,
            'SKU': sku
        })
    return products

def main():
    all_products = []
    cp = 1
    while True:
        print(f"Scraping page {cp}...")
        attempts = 0
        products = []
        while attempts < 4:
            products = get_products_from_page(cp)
            print(f"  Attempt {attempts+1}: Found {len(products)} products.")
            if len(products) >= 18:
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
    # Write to CSV
    with open('bestbuy_products_scrapedo.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Brand', 'Product Title', 'Image', 'Price', 'Model', 'SKU']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for product in all_products:
            writer.writerow(product)
    print("Products written to bestbuy_products_scrapedo.csv")

if __name__ == "__main__":
    main()
