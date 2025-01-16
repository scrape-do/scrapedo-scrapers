import requests
from bs4 import BeautifulSoup
import urllib.parse
import csv

token = "YOUR_TOKEN"
page = 1

# Define CSV output file and header
output_file = "categories.csv"
csv_headers = ["Company", "Logo", "Review Link", "Description", "Industries", "Pros", "Cons"]


# Function to fetch category page
def fetch_category_page(page_number):
    category_url = urllib.parse.quote_plus(f"https://www.g2.com/categories/project-management?page={page_number}")
    api_url = f"https://api.scrape.do?token={token}&url={category_url}&geoCode=us"
    response = requests.get(api_url)
    return response.text if response.status_code == 200 else None


# Function to process and return category item details
def process_category_item(i):

    company_name = i.find('div', class_='product-card__product-name').text.strip()

    try:
        company_logo = i.select_one('img[itemprop="image"]')['data-deferred-image-src']
    except AttributeError:
        company_logo = "Not available"
    except KeyError:
        company_logo = "Not available"

    review_link = i.find('a', class_='js-log-click')['href']

    try:
        description = i.find('span', class_='product-listing__paragraph').text.strip() + \
                      i.find('span', class_='product-listing__paragraph')['data-truncate-revealer-overflow-text']
    except AttributeError:
        description = "Not available"

    industries = [tag.text.strip() for tag in i.find_all('div', class_='cell')[1].find_all('li')]

    try:
        pros = [tag.text.strip() for tag in i.select_one('div[aria-label="Pros"]').find_all('div', class_='ellipsis')]
    except AttributeError:
        pros = []

    try:
        cons = [tag.text.strip() for tag in i.select_one('div[aria-label="Cons"]').find_all('div', class_='ellipsis')]
    except AttributeError:
        cons = []

    return {
        "Company": company_name,
        "Logo": company_logo,
        "Review Link": review_link,
        "Description": description,
        "Industries": ", ".join(industries),
        "Pros": "; ".join(pros),
        "Cons": "; ".join(cons)
    }


# Open CSV file and write data
with open(output_file, mode="w", newline="", encoding="utf-8") as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
    writer.writeheader()  # Write CSV headers

    while True:
        html_content = fetch_category_page(page)
        if not html_content:
            break

        soup = BeautifulSoup(html_content, 'html.parser')
        category_items = soup.find_all('div', class_='segmented-shadow-card')
        if not category_items:
            break

        for item in category_items:
            category_data = process_category_item(item)
            writer.writerow(category_data)  # Write category data to CSV

        page += 1

print(f"Categories exported to {output_file}")
