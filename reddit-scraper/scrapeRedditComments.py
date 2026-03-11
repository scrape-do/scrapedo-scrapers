import requests
from urllib.parse import quote
from bs4 import BeautifulSoup
import csv
import re

token = "<your_token>"
query = "best fishing rod"

# Sort options:
#   "relevance" - most relevant comments first (default)
#   "new"       - most recent comments first
#   "top"       - highest scoring comments (use with time_filter below)
sort = "relevance"

# Time filter (only applies when sort="top"):
#   "hour", "day", "week", "month", "year", "all"
time_filter = "all"

# Number of pages to scrape
max_pages = 3

# Build initial search URL for comments
search_params = f"q={quote(query)}&type=comments"
if sort != "relevance":
    search_params += f"&sort={sort}"
if sort == "top":
    search_params += f"&t={time_filter}"

all_comments = []

for page in range(max_pages):
    target_url = f"https://www.reddit.com/search/?{search_params}"
    api_url = f"http://api.scrape.do?token={token}&url={quote(target_url)}&super=true"

    response = requests.get(api_url)
    if response.status_code != 200:
        print(f"Page {page + 1} failed: {response.status_code}")
        break

    soup = BeautifulSoup(response.text, "html.parser")
    comments = soup.find_all(attrs={"data-testid": "search-sdui-comment-unit"})

    if not comments:
        print(f"No more comments on page {page + 1}")
        break

    for comment in comments:
        # Comment body
        content_el = comment.find(attrs={"data-testid": "search-comment-content"})
        body = content_el.get_text(strip=True) if content_el else ""

        # Author is a link with href="#"
        author = ""
        for link in comment.find_all("a"):
            if link.get("href") == "#" and link.get_text(strip=True):
                author = link.get_text(strip=True)
                break

        # Thread title and subreddit from links
        thread_title = ""
        subreddit = ""
        thread_url = ""
        for link in comment.find_all("a"):
            href = link.get("href", "")
            text = link.get_text(strip=True)
            if "/comments/" in href and text != "Go To Thread":
                thread_title = text
                thread_url = "https://www.reddit.com" + href
            elif href.startswith("/r/") and href.endswith("/"):
                subreddit = text

        all_comments.append({
            "author": author,
            "comment": body[:500],
            "thread_title": thread_title,
            "subreddit": subreddit,
            "thread_url": thread_url,
        })

    print(f"Page {page + 1}: {len(comments)} comments")

    # Extract cursor and iId for pagination
    cursor_match = re.search(r'cursor=([^&"\s]+)', response.text)
    iid_match = re.search(r'iId=([^&"\s]+)', response.text)

    if not cursor_match:
        print("No more pages available")
        break

    cursor = cursor_match.group(1)
    iid = iid_match.group(1) if iid_match else ""

    # Build next page URL
    search_params = f"q={quote(query)}&type=comments&cursor={cursor}&iId={iid}"
    if sort != "relevance":
        search_params += f"&sort={sort}"
    if sort == "top":
        search_params += f"&t={time_filter}"

with open("reddit-comments.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["author", "comment", "thread_title", "subreddit", "thread_url"])
    writer.writeheader()
    writer.writerows(all_comments)

print(f"\nTotal: {len(all_comments)} comments saved to reddit-comments.csv")
