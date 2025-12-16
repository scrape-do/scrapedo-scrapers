import urllib.parse
import csv
import re
import requests
from bs4 import BeautifulSoup

# Configuration
token = "<SDO-token>"
asin = "B07TCJS1NS"  # Change this to any product ASIN
geocode = "us"

# Build product URL from ASIN
target_url = f"https://www.amazon.com/dp/{asin}"

# Make API request
targetUrl = urllib.parse.quote(target_url)
apiUrl = "https://api.scrape.do/?token={}&url={}&geoCode={}".format(token, targetUrl, geocode)
response = requests.request("GET", apiUrl)

soup = BeautifulSoup(response.text, "html.parser")

# Extract review data
reviews = []
for review in soup.find_all("li", {"data-hook": "review"}):
    # Get star rating
    rating_elem = review.find("i", {"data-hook": "review-star-rating"}) or review.find("i", class_=re.compile(r"a-icon-star"))
    rating = rating_elem.find("span", class_="a-icon-alt").text.split()[0] if rating_elem else "N/A"

    # Get review date (remove country prefix)
    date_elem = review.find("span", {"data-hook": "review-date"})
    date = re.sub(r"Reviewed in .* on ", "", date_elem.text) if date_elem else "N/A"

    # Get review content
    content_elem = review.find("span", {"data-hook": "review-body"})
    content = content_elem.get_text(strip=True) if content_elem else "N/A"

    # Get helpful votes count
    helpful_elem = review.find("span", {"data-hook": "helpful-vote-statement"})
    helpful = re.findall(r'\d+', helpful_elem.text)[0] if helpful_elem and re.findall(r'\d+', helpful_elem.text) else "0"

    reviews.append({
        "review_id": review.get("id", ""),
        "rating": rating,
        "date": date,
        "content": content,
        "helpful": helpful
    })

# Export to CSV
csv_file = "reviews.csv"
headers = ["review_id", "rating", "date", "content", "helpful"]

with open(csv_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=headers)
    writer.writeheader()
    writer.writerows(reviews)

print(f"Found {len(reviews)} reviews")
print(f"Data exported to {csv_file}")
