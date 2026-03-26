import requests
import urllib.parse
import json
from bs4 import BeautifulSoup

token = "<your_token>"
query = "python web scraping"

encoded_query = urllib.parse.quote_plus(query)
google_url = f"https://www.google.com/search?q={encoded_query}&hl=en&gl=us"
api_url = f"http://api.scrape.do/?token={token}&url={urllib.parse.quote(google_url, safe='')}&super=true"

response = requests.get(api_url, timeout=60)

if response.status_code != 200:
    print(f"Request failed: {response.status_code}")
    exit()

soup = BeautifulSoup(response.text, "html.parser")
related_searches = soup.find_all("div", class_="b2Rnsc vIifob")

terms = []
for position, item in enumerate(related_searches, 1):
    terms.append({"position": position, "term": item.get_text(strip=True)})

with open("related-search-terms.json", "w", encoding="utf-8") as f:
    json.dump(terms, f, indent=2, ensure_ascii=False)

for t in terms:
    print(f"{t['position']}. {t['term']}")

print(f"\nFound {len(terms)} related terms. Saved to related-search-terms.json")
