import requests
import urllib.parse
from bs4 import BeautifulSoup
import csv

TOKEN = "<your-token"
start_url = "<product-url>"

def extract_reviews(soup):
    reviews = soup.select(".ebay-review-section")
    data = []

    for r in reviews:
        try:
            reviewer = r.select_one(".review-item-author").get_text(strip=True)
        except:
            reviewer = None

        try:
            rating = r.select_one("div.star-rating")["data-stars"].split("-")[0]
        except:
            rating = None

        try:
            title = r.select_one(".review-item-title").get_text(strip=True)
        except:
            title = None

        try:
            date = r.select_one(".review-item-date").get_text(strip=True)
        except:
            date = None

        try:
            comment = r.select_one(".review-item-content").get_text(strip=True)
        except:
            comment = None

        data.append({
            "Reviewer": reviewer,
            "Rating": rating,
            "Title": title,
            "Date": date,
            "Comment": comment
        })

    return data


def get_next_page(soup):
    try:
        return soup.select_one('a[rel="next"]')["href"]
    except:
        return None


all_reviews = []
current_url = start_url

while current_url:
    encoded = urllib.parse.quote_plus(current_url)
    api_url = f"https://api.scrape.do/?token={TOKEN}&url={encoded}&super=true&geocode=us"

    response = requests.get(api_url)
    soup = BeautifulSoup(response.text, "html.parser")

    all_reviews.extend(extract_reviews(soup))

    current_url = get_next_page(soup)

# Export results
with open("ebay_paginated_reviews.csv", mode="w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["Reviewer", "Rating", "Title", "Date", "Comment"])
    writer.writeheader()
    for row in all_reviews:
        writer.writerow(row)

print("Saved all reviews to ebay_paginated_reviews.csv")
