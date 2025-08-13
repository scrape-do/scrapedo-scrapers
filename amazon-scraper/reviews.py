import requests
import urllib.parse
import csv
from bs4 import BeautifulSoup
import re

# Scrape.do token and target URL
token = "<your-token>"
url = "https://us.amazon.com/Calvin-Klein-Underwear-Classics-Multipack/dp/B07TCJS1NS"

# Make API request and parse HTML
api_url = f"http://api.scrape.do?token={token}&url={urllib.parse.quote_plus(url)}&geoCode=us"
soup = BeautifulSoup(requests.get(api_url).text, "html.parser")

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
    
    reviews.append([review.get("id", ""), rating, date, content, helpful])

# Save to CSV and print results
print(f"Found {len(reviews)} reviews")
with open("amazon_reviews.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["review_id", "rating", "date", "content", "helpful"])
    writer.writerows(reviews)

print("Reviews saved to amazon_reviews.csv")
