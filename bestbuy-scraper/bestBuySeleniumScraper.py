from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import csv

# Start at the page where the country selection is shown
base_url = "https://www.bestbuy.com/site/searchpage.jsp?browsedCategory=pcmcat311200050005&cp={cp}&id=pcat17071&st=categoryid%24pcmcat311200050005"

options = Options()
options.add_argument('--no-sandbox')
options.add_argument('--disable-blink-features=AutomationControlled')
# options.add_argument('--headless')  # Uncomment for headless mode

driver = webdriver.Chrome(options=options)

try:
    driver.get(base_url.format(cp=1))
    
    # Wait for the US link to be present and clickable
    us_link = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.CLASS_NAME, 'us-link'))
    )
    us_link.click()
    
    # Wait 6 seconds after clicking
    time.sleep(6)

    # Aggregate all products from all pages
    all_products = []
    start_time = time.time()
    page_num = 1
    while True:
        print(f"\n--- Scraping page {page_num} ---")
        page_url = base_url.format(cp=page_num)
        driver.get(page_url)
        time.sleep(3)  # Wait for page to load

        # Scroll to the bottom to load all products
        scroll_pause = 0.5
        last_height = driver.execute_script("return window.scrollY")
        total_height = driver.execute_script("return document.body.scrollHeight")
        step = 400
        current_position = 0
        while current_position < total_height:
            driver.execute_script(f"window.scrollTo(0, {current_position});")
            time.sleep(scroll_pause)
            current_position += step
            total_height = driver.execute_script("return document.body.scrollHeight")
        driver.execute_script(f"window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

        # Scrape product details from li.product-list-item
        product_items = driver.find_elements(By.CSS_SELECTOR, 'li.product-list-item')
        print(f"Found {len(product_items)} product-list-item elements on page {page_num}.")
        if len(product_items) == 0:
            print(f"No products found on page {page_num}. Stopping.")
            break
        for idx, item in enumerate(product_items, 1):
            # Brand and Product Title
            brand = None
            product_title = None
            try:
                h2 = item.find_element(By.CSS_SELECTOR, 'h2.product-title')
                try:
                    brand_span = h2.find_element(By.CSS_SELECTOR, 'span.first-title')
                    brand = brand_span.text.strip()
                except:
                    brand = None
                full_title = h2.text.strip()
                if brand and full_title.startswith(brand):
                    product_title = full_title[len(brand):].strip(' -\n')
                else:
                    product_title = full_title
            except:
                brand = None
                product_title = None
            # Image source
            img_src = None
            try:
                img = item.find_element(By.CSS_SELECTOR, 'div.product-image.m-100 img')
                img_src = img.get_attribute('src')
            except:
                img_src = None
            # Product price
            price = None
            try:
                price_div = item.find_element(By.CSS_SELECTOR, 'div.customer-price.medium')
                price = price_div.text.strip()
            except:
                price = None
            # Model and SKU
            model = None
            sku = None
            try:
                attr_divs = item.find_elements(By.CSS_SELECTOR, 'div.product-attributes div.attribute')
                if len(attr_divs) > 0:
                    model_span = attr_divs[0].find_element(By.CSS_SELECTOR, 'span.value')
                    model = model_span.text.strip()
                if len(attr_divs) > 1:
                    sku_span = attr_divs[1].find_element(By.CSS_SELECTOR, 'span.value')
                    sku = sku_span.text.strip()
            except:
                model = None
                sku = None
            all_products.append({
                'Brand': brand,
                'Product Title': product_title,
                'Image': img_src,
                'Price': price,
                'Model': model,
                'SKU': sku
            })
        page_num += 1

    # --- Save to CSV ---
    downloads = os.path.join(os.path.expanduser('~'), 'Downloads')
    csv_path = os.path.join(downloads, 'bestbuy_products.csv')
    print(f"\nSaving product data to {csv_path} ...")
    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Brand', 'Product Title', 'Image', 'Price', 'Model', 'SKU']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for product in all_products:
            writer.writerow(product)
    print(f"Saved {len(all_products)} products to CSV.")

    # Print total elapsed time
    elapsed = time.time() - start_time
    print(f"\nTotal elapsed time: {elapsed:.2f} seconds ({elapsed/60:.2f} minutes)")

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    driver.quit()
    print("Browser closed.") 
