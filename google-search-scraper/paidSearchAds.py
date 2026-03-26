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
search_ads = soup.find_all("div", class_="uEierd")

ads = []
for position, ad in enumerate(search_ads, 1):
    url_elem = ad.find("a")
    url = url_elem.get("href") if url_elem else None

    # Title from heading tags or known ad title classes
    title_elem = ad.find(["h3", "div"], class_=lambda x: x and any(c in str(x) for c in ["CCgQ5", "vCa9Yd", "QfkTvb"]))
    if not title_elem:
        title_elem = ad.find(["h1", "h2", "h3", "h4", "h5", "h6"])
    title = title_elem.get_text(strip=True) if title_elem else None

    # Description from known ad description classes
    desc_elem = ad.find("div", class_=lambda x: x and any(c in str(x) for c in ["Va3FIb", "r025kc", "lVm3ye"]))
    if desc_elem:
        description = desc_elem.get_text(strip=True)
    else:
        spans = [s.get_text(strip=True) for s in ad.find_all("span") if len(s.get_text(strip=True)) > 20 and s.get_text(strip=True) not in ["Sponsored", "Ad"]]
        description = " ".join(spans) if spans else None

    # Display URL
    display_elem = ad.find("span", class_=lambda x: x and "qzEoUe" in str(x))
    display_url = display_elem.get_text(strip=True) if display_elem else None

    ads.append({"position": position, "title": title, "url": url, "description": description, "display_url": display_url})

with open("paid-search-ads.json", "w", encoding="utf-8") as f:
    json.dump(ads, f, indent=2, ensure_ascii=False)

for ad in ads:
    print(f"\n--- Ad {ad['position']} ---")
    print(f"Title: {ad['title']}")
    print(f"URL: {ad['url']}")
    print(f"Description: {ad['description']}")
    print(f"Display URL: {ad['display_url']}")

print(f"\nFound {len(ads)} ads. Saved to paid-search-ads.json")
