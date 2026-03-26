import requests
import json

token = "<your_token>"
query = "artificial intelligence news"

# The SERP API returns top_stories for news-related queries.
# Each top_stories entry has a headline and an items array with the
# individual news articles (title, link, source).
url = f"https://api.scrape.do/plugin/google/search?token={token}&q={query}&hl=en&gl=us"

response = requests.get(url, timeout=60)

if response.status_code != 200:
    print(f"Request failed: {response.status_code}")
    exit()

data = response.json()

# Top stories (news carousel). Each entry groups related articles
# under a headline, with individual items inside an "items" array.
top_stories = data.get("top_stories", [])
all_articles = []
for group in top_stories:
    for item in group.get("items", []):
        if not item.get("link") or "google.com" in item.get("link", ""):
            continue
        all_articles.append({
            "title": item.get("title", "N/A"),
            "source": item.get("source", "N/A"),
            "link": item.get("link", "N/A"),
        })

print(f"News articles from top stories: {len(all_articles)}")
for article in all_articles:
    print(f"\n  {article['title']}")
    print(f"    Source: {article['source']}")
    print(f"    Link: {article['link']}")

# Discussions and forums (Reddit, Quora, etc.)
discussions = data.get("discussions_and_forums", [])
if discussions:
    print(f"\nDiscussions & forums: {len(discussions)}")
    for d in discussions[:3]:
        print(f"  - {d.get('title', 'N/A')} ({d.get('source', 'N/A')})")

with open("serp-api-news-results.json", "w", encoding="utf-8") as f:
    json.dump({"articles": all_articles, "discussions_and_forums": discussions}, f, indent=2, ensure_ascii=False)

print(f"\nSaved to serp-api-news-results.json")
