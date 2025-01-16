import requests
from bs4 import BeautifulSoup
import urllib.parse

# Scrape.do token and target URL
token = "YOUR_TOKEN"
url = urllib.parse.quote_plus("https://www.g2.com/products/monday-com")

# API call
api_url = f"https://api.scrape.do?token={token}&url={url}&geoCode=us"
response = requests.get(api_url)
html_content = ""

# Check if the request is successful and store the contents
if response.status_code == 200:
    html_content = response.text
    print("Page fetched successfully!")
else:
    print(f"Failed to fetch page. Status: {response.status_code}")

# If any content is available
if html_content:
    # Parse the data
    soup = BeautifulSoup(html_content, 'html.parser')

    product_name = soup.find('div', class_='product-head__title').select_one('div[itemprop="name"]').text.strip()

    try:
        product_website = soup.find('input', id='secure_url')['value']
    except TypeError:
        product_website = "Not available"

    try:
        product_logo = soup.find('img', class_='js-product-img')['src']
    except TypeError:
        product_logo = "Not available"

    try:
        review_count = soup.find('h3', class_='mb-half').text.strip()
    except TypeError:
        review_count = "0"

    try:
        review_rating = soup.find('span', class_='fw-semibold').text.strip()
    except TypeError:
        review_rating = "Not available"

    # Extract pricing for each option
    # If there is no money unit available omit it and get the price text
    pricing_info = []

    for tag in soup.find_all('a', class_='preview-cards__card'):
        head = tag.find('div', class_='preview-cards__card__head').text.strip()
        money_unit = tag.find('span', class_='money__unit')
        money_value = tag.find('span', class_='money__value').text.strip()

        if money_unit:
            money_unit_text = money_unit.text.strip()
            pricing_info.append(f"{head} - {money_unit_text}{money_value}")
        else:
            pricing_info.append(f"{head} - {money_value}")

    pros = [tag.text.strip() for tag in soup.select_one('div[aria-label="Pros"]').find_all('div', class_='ellipsis')]
    cons = [tag.text.strip() for tag in soup.select_one('div[aria-label="Cons"]').find_all('div', class_='ellipsis')]

    # Output the results
    print(f"Product Name: {product_name}")
    print(f"Website: {product_website}")
    print(f"Logo URL: {product_logo}")
    print(f"Review Count: {review_count}")
    print(f"Rating: {review_rating}")
    print(f"Pricing: {pricing_info}")
    print(f"Pros: {pros}")
    print(f"Cons: {cons}")
