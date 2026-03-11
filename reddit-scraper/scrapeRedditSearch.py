import requests
from urllib.parse import quote
from bs4 import BeautifulSoup
import csv
import re

token = "<your_token>"
query = "best fishing rod"

# Sort options:
#   "relevance" - most relevant results first (default)
#   "hot"       - currently trending results
#   "new"       - most recent results first
#   "top"       - highest scoring results (use with time_filter)
#   "comments"  - most commented results first
sort = "relevance"

# Time filter (only applies when sort="top"):
#   "hour", "day", "week", "month", "year", "all"
time_filter = "year"

# Number of pages to scrape
max_pages = 3

# Build the initial search URL
search_params = f"q={quote(query)}"
if sort != "relevance":
    search_params += f"&sort={sort}"
if sort == "top":
    search_params += f"&t={time_filter}"

all_results = []

for page in range(max_pages):
    target_url = f"https://www.reddit.com/search/?{search_params}"
    api_url = f"http://api.scrape.do?token={token}&url={quote(target_url)}&super=true"

    response = requests.get(api_url)
    if response.status_code != 200:
        print(f"Page {page + 1} failed: {response.status_code}")
        break

    soup = BeautifulSoup(response.text, "html.parser")

    # Search results use the sdui-post-unit container
    results = soup.find_all(attrs={"data-testid": "sdui-post-unit"})

    if not results:
        print(f"No more results on page {page + 1}")
        break

    for result in results:
        title_el = result.find(attrs={"data-testid": "post-title-text"})
        title = title_el.get_text(strip=True) if title_el else ""

        subreddit = ""
        for link in result.find_all("a"):
            href = link.get("href", "")
            if href.startswith("/r/") and href.endswith("/") and "/comments/" not in href:
                subreddit = link.get_text(strip=True)
                break

        post_url = ""
        post_link = result.find("a", href=lambda h: h and "/comments/" in h)
        if post_link:
            post_url = "https://www.reddit.com" + post_link.get("href", "")

        all_results.append({
            "title": title,
            "subreddit": subreddit,
            "url": post_url,
        })

    print(f"Page {page + 1}: {len(results)} results")

    # Extract cursor and iId for pagination
    cursor_match = re.search(r'cursor=([^&"\s]+)', response.text)
    iid_match = re.search(r'iId=([^&"\s]+)', response.text)

    if not cursor_match:
        print("No more pages available")
        break

    cursor = cursor_match.group(1)
    iid = iid_match.group(1) if iid_match else ""

    # Build next page URL using the Shreddit search API
    search_params = f"q={quote(query)}&cursor={cursor}&iId={iid}"
    if sort != "relevance":
        search_params += f"&sort={sort}"
    if sort == "top":
        search_params += f"&t={time_filter}"

with open("search-results.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["title", "subreddit", "url"])
    writer.writeheader()
    writer.writerows(all_results)

print(f"\nTotal: {len(all_results)} results saved to search-results.csv")
