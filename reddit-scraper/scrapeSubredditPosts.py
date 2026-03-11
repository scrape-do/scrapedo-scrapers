import requests
from urllib.parse import quote
from bs4 import BeautifulSoup
import csv
import re

token = "<your_token>"
subreddit = "fishing"

# Sort options:
#   "new"    - most recent posts first
#   "hot"    - currently trending posts (default Reddit view)
#   "top"    - highest scoring posts (use with time_filter)
#   "rising" - posts gaining traction right now
sort = "new"

# Time filter (only applies when sort="top"):
#   "hour", "day", "week", "month", "year", "all"
time_filter = "month"

# Number of pages to scrape (each page returns ~25 posts)
max_pages = 3

target_base = f"https://www.reddit.com/svc/shreddit/community-more-posts/{sort}/"
params = f"name={subreddit}"
if sort == "top":
    params += f"&t={time_filter}"

all_posts = []

for page in range(max_pages):
    target_url = f"{target_base}?{params}"
    api_url = f"http://api.scrape.do?token={token}&url={quote(target_url)}&super=true"

    response = requests.get(api_url)
    if response.status_code != 200:
        print(f"Page {page + 1} failed: {response.status_code}")
        break

    soup = BeautifulSoup(response.text, "html.parser")
    posts = soup.find_all("shreddit-post")

    if not posts:
        print(f"No more posts found on page {page + 1}")
        break

    for post in posts:
        all_posts.append({
            "title": post.get("post-title", ""),
            "author": post.get("author", ""),
            "score": post.get("score", ""),
            "comments": post.get("comment-count", ""),
            "timestamp": post.get("created-timestamp", ""),
            "permalink": "https://www.reddit.com" + post.get("permalink", ""),
        })

    print(f"Page {page + 1}: {len(posts)} posts")

    # Extract pagination token for the next page
    after_match = re.search(r'after=([^&"\s]+)', response.text)
    if not after_match:
        print("No more pages available")
        break

    after_token = after_match.group(1)
    params = f"after={after_token}&name={subreddit}"
    if sort == "top":
        params += f"&t={time_filter}"

with open("subreddit-posts.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["title", "author", "score", "comments", "timestamp", "permalink"])
    writer.writeheader()
    writer.writerows(all_posts)

print(f"\nTotal: {len(all_posts)} posts saved to subreddit-posts.csv")
