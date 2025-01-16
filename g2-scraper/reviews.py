import requests
from bs4 import BeautifulSoup
import urllib.parse
import csv

base_url = "https://www.g2.com/products/breeze-llc-breeze/reviews"
token = "YOUR_TOKEN"
page = 1

# Define CSV output file and header
output_file = "reviews.csv"
csv_headers = ["Reviewer", "Title", "Industry", "Review Title", "Rating", "Content"]


# Function to fetch review page
def fetch_review_page(page_number):
    url = urllib.parse.quote_plus(f"{base_url}?page={page_number}")
    api_url = f"https://api.scrape.do?token={token}&url={url}&geoCode=us"
    response = requests.get(api_url)
    return response.text if response.status_code == 200 else None


# Function to process and return review details
def process_review(r):
    try:
        reviewer_name = r.select_one('span[itemprop="author"]').text.strip()
    except Exception:
        reviewer_name = r.select_one('div[itemprop="author"]').text.strip().split("Information")[0]
    title = r.find('div', class_='c-midnight-80').find_all('div', class_='mt-4th')[0].text.strip()
    try:
        industry = r.find('div', class_='c-midnight-80').find_all('div', class_='mt-4th')[1].text.strip()
    except:
        industry = "-"
    review_title = r.select_one('div[itemprop="name"]').text.strip()
    star = r.find('div', class_='stars')
    rating = float(float(star["class"][len(star)-1].split("-")[1]) / 2)
    content = r.select_one('div[itemprop="reviewBody"]').text.strip()

    return {
        "Reviewer": reviewer_name,
        "Title": title,
        "Industry": industry,
        "Review Title": review_title,
        "Rating": rating,
        "Content": content
    }


# Open CSV file and write data
with open(output_file, mode="w", newline="", encoding="utf-8") as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
    writer.writeheader()  # Write CSV headers

    while True:
        html_content = fetch_review_page(page)
        if not html_content:
            break

        soup = BeautifulSoup(html_content, 'html.parser')
        reviews = soup.find('div', class_="nested-ajax-loading").find_all('div', class_='paper')
        if not reviews:
            break

        for review in reviews:
            review_data = process_review(review)
            writer.writerow(review_data)  # Write review data to CSV

        page += 1

print(f"Reviews exported to {output_file}")
