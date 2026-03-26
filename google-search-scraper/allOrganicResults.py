import requests
import urllib.parse
import csv
import time
from bs4 import BeautifulSoup

token = "<your_token>"
query = "python web scraping"
MAX_PAGES = 5

encoded_query = urllib.parse.quote_plus(query)
all_results = []

for page in range(MAX_PAGES):
    start = page * 10
    print(f"Scraping page {page + 1} (start={start})...")

    google_url = f"https://www.google.com/search?q={encoded_query}&start={start}&hl=en&gl=us"
    api_url = f"http://api.scrape.do/?token={token}&url={urllib.parse.quote(google_url, safe='')}&super=true"

    response = requests.get(api_url, timeout=60)
    if response.status_code != 200:
        print(f"Request failed: {response.status_code}")
        break

    soup = BeautifulSoup(response.text, "html.parser")
    search_results = soup.find_all("div", class_=lambda x: x and "Ww4FFb" in x)

    if not search_results:
        print("No more results found.")
        break

    for result in search_results:
        title_tag = result.find("h3")
        link_tag = result.find("a")
        desc_tag = result.find(class_="VwiC3b")

        all_results.append({
            "position": len(all_results) + 1,
            "title": title_tag.get_text(strip=True) if title_tag else None,
            "url": link_tag.get("href") if link_tag else None,
            "description": desc_tag.get_text(strip=True) if desc_tag else None,
        })

    time.sleep(1)

with open("all-organic-results.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["position", "title", "url", "description"])
    writer.writeheader()
    writer.writerows(all_results)

print(f"\nFound {len(all_results)} results across {min(page + 1, MAX_PAGES)} pages.")
print(f"Saved to all-organic-results.csv")
