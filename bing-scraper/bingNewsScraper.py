import requests
import csv
import urllib.parse
from bs4 import BeautifulSoup

# Configuration
token = "<your-token>"
query = "tesla"
max_results = 100

all_news = []
first = 1  # Pagination starts at 1, increments by 10

print(f"Starting Bing News scrape for: '{query}'")
print(f"Target: {max_results} articles\n")

while len(all_news) < max_results:
    # Build URL for infinite scroll
    page_url = f"https://www.bing.com/news/infinitescrollajax?qft=sortbydate%3d%221%22&InfiniteScroll=1&q={urllib.parse.quote(query)}&first={first}"
    encoded_url = urllib.parse.quote(page_url, safe='')
    api_url = f"http://api.scrape.do?token={token}&url={encoded_url}&geoCode=us"
    
    print(f"Fetching articles (first={first})...", end=" ")
    
    # Send request
    response = requests.get(api_url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Extract news articles
    page_articles = []
    
    # News articles are in divs with class "news-card newsitem cardcommon"
    for article in soup.find_all("div", class_="news-card"):
        try:
            # Extract title
            title_tag = article.find("a", class_="title")
            title = title_tag.get_text(strip=True) if title_tag else ""
            
            # Extract URL
            url = article.get("data-url", "") or article.get("url", "")
            
            # Extract snippet/description
            snippet_tag = article.find("div", class_="snippet")
            snippet = snippet_tag.get_text(strip=True) if snippet_tag else ""
            
            # Extract source (data-author attribute)
            source = article.get("data-author", "")
            
            # Extract time (look for span with tabindex="0")
            time_tag = article.find("span", {"tabindex": "0"})
            published_time = time_tag.get_text(strip=True) if time_tag else ""
            
            if title:
                page_articles.append({
                    "title": title,
                    "url": url,
                    "snippet": snippet,
                    "source": source,
                    "published_time": published_time
                })
        except:
            continue
    
    # Stop if no articles found
    if not page_articles:
        print("No more articles found")
        break
    
    all_news.extend(page_articles)
    print(f"Found {len(page_articles)} articles (total: {len(all_news)})")
    
    # Next page - increment by 10
    first += 10

# Trim to max_results
all_news = all_news[:max_results]

# Save to CSV
print(f"\nSaving {len(all_news)} articles to CSV...")
with open("bing_news_results.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["title", "url", "snippet", "source", "published_time"])
    writer.writeheader()
    writer.writerows(all_news)

print(f"Done! Extracted {len(all_news)} articles -> bing_news_results.csv")
