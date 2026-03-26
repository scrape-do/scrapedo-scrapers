import requests
import urllib.parse
import csv
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
search_results = soup.find_all("div", class_=lambda x: x and "Ww4FFb" in x)

results = []
for position, result in enumerate(search_results, 1):
    title_tag = result.find("h3")
    link_tag = result.find("a")
    desc_tag = result.find(class_="VwiC3b")

    results.append({
        "position": position,
        "title": title_tag.get_text(strip=True) if title_tag else None,
        "url": link_tag.get("href") if link_tag else None,
        "description": desc_tag.get_text(strip=True) if desc_tag else None,
    })

with open("first-page-results.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["position", "title", "url", "description"])
    writer.writeheader()
    writer.writerows(results)

for r in results:
    print(f"{r['position']}. {r['title']}")
    print(f"   URL: {r['url']}")
    print(f"   Description: {r['description']}")
    print()

print(f"Saved {len(results)} results to first-page-results.csv")
