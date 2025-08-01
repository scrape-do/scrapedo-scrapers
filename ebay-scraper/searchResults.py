import requests
import urllib.parse
from bs4 import BeautifulSoup
import csv

# Your Scrape.do token
TOKEN = "<your-token"
results = []
current_url = "<product-url>"

while current_url:
    encoded_url = urllib.parse.quote_plus(current_url)
    api_url = f"https://api.scrape.do/?token={TOKEN}&url={encoded_url}&geocode=us&super=true&render=true"

    response = requests.get(api_url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Detect which layout is being used
    if soup.select("li.s-card"):
        items = soup.select("li.s-card")
        layout = "s-card"
    elif soup.select("li.s-item"):
        items = soup.select("li.s-item")
        layout = "s-item"
    else:
        break

    for item in items:
        try:
            title = item.select_one(".s-card__title" if layout == "s-card" else ".s-item__title").get_text(strip=True)
        except:
            title = None

        try:
            price_spans = item.select(".s-card__price" if layout == "s-card" else ".s-item__price")
            if len(price_spans) > 1:
                price = " ".join([span.get_text(strip=True) for span in price_spans])
            elif price_spans:
                price = price_spans[0].get_text(strip=True)
            else:
                price = None
        except:
            price = None

        try:
            image_url = item.select_one(".s-card__image" if layout == "s-card" else ".s-item__image-img")["src"]
        except:
            image_url = None

        try:
            link = item.select_one("a.su-link" if layout == "s-card" else "a.s-item__link")["href"]
        except:
            link = None

        results.append({
            "title": title,
            "price": price,
            "image_url": image_url,
            "link": link
        })

    try:
        next_link = soup.select_one("a.pagination__next")["href"]
        current_url = next_link
    except:
        current_url = None

# Export to CSV
with open("ebay_search_results.csv", mode="w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["title", "price", "image_url", "link"])
    writer.writeheader()
    for row in results:
        writer.writerow(row)

print("Scraping completed. Results saved to ebay_search_results.csv.")
