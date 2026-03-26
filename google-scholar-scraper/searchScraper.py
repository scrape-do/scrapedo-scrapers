import json
import os
import urllib.parse
import requests
from bs4 import BeautifulSoup
import time

TOKEN = "<your_token>"
SEARCH_QUERY = "breakfast in the morning"
TARGET_URL = f"https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&q={urllib.parse.quote_plus(SEARCH_QUERY)}&btnG="
MAX_PAGES = 3

all_results = []

# Google Scholar serves 10 results per page. We'll crawl through 3 pages
# using the `start` parameter to offset our position in the result set.
for page_num in range(MAX_PAGES):
    start_index = page_num * 10
    page_url = TARGET_URL if page_num == 0 else f"{TARGET_URL}&start={start_index}"

    print(f"Scraping page {page_num + 1}/{MAX_PAGES}...")

    # Google Scholar has solid bot detection, so super=true is our go-to here.
    # No need for render since Scholar is fully server-side rendered.
    api_url = f"http://api.scrape.do/?token={TOKEN}&url={urllib.parse.quote(page_url)}&super=true"
    response = requests.get(api_url, timeout=60)
    soup = BeautifulSoup(response.text, "html.parser")

    # Each search result lives inside a div.gs_ri container.
    # We're after three things: the paper title, its snippet, and the direct link.
    for result in soup.find_all("div", class_="gs_ri"):
        title_elem = result.find("h3", class_="gs_rt")
        if not title_elem:
            continue

        # The title heading wraps an <a> tag with the actual link to the paper.
        # Some results (like citations or books) might not have a clickable link.
        link_elem = title_elem.find("a")
        title = link_elem.get_text(strip=True) if link_elem else title_elem.get_text(strip=True)
        link = link_elem.get("href") if link_elem else None

        snippet_elem = result.find("div", class_="gs_rs")
        author_elem = result.find("div", class_="gs_a")

        all_results.append({
            "title": title,
            "description": snippet_elem.get_text(strip=True) if snippet_elem else None,
            "authors": author_elem.get_text(strip=True) if author_elem else None,
            "link": link
        })

    time.sleep(1)

with open("scholar_search_results.json", "w", encoding="utf-8") as f:
    json.dump(all_results, f, indent=2, ensure_ascii=False)

for i, r in enumerate(all_results, 1):
    print(f"\n--- Result {i} ---")
    print(f"Title: {r['title']}")
    print(f"Authors: {r['authors']}")
    print(f"Link: {r['link']}")

print(f"\nTotal: {len(all_results)} results saved to scholar_search_results.json")


# =============================================================================
# BONUS: Download extracted article links as Markdown
# =============================================================================
# Download each article as Markdown using Scrape.do's output=markdown feature.
# Progressive fallback strategy:
#   1. Try a basic request (cheapest, fastest)
#   2. If that fails, escalate to super=true
#   3. Still no luck? Go full power with super=true & render=true

os.makedirs("scholar_articles", exist_ok=True)

strategies = [
    ("basic", ""),
    ("super", "&super=true"),
    ("super+render", "&super=true&render=true"),
]

for i, r in enumerate(all_results):
    if not r["link"]:
        continue

    print(f"\n[{i + 1}/{len(all_results)}] Downloading: {r['title'][:60]}...")
    content = None

    for strategy_name, params in strategies:
        try:
            print(f"    Trying {strategy_name}...", end=" ")
            api_url = f"http://api.scrape.do/?token={TOKEN}&url={urllib.parse.quote(r['link'])}&output=markdown{params}"
            resp = requests.get(api_url, timeout=90)
            if resp.status_code == 200 and len(resp.text.strip()) > 100:
                print("Success!")
                content = resp.text
                break
            print(f"Failed (status: {resp.status_code})")
        except Exception as e:
            print(f"Error: {e}")

    if content:
        safe_name = "".join(c if c.isalnum() or c in " -_" else "" for c in r["title"])[:80].strip()
        with open(f"scholar_articles/{i + 1:02d}_{safe_name}.md", "w", encoding="utf-8") as f:
            f.write(content)
    else:
        print("    Could not download this article with any strategy.")

    time.sleep(1)

print(f"\nArticles saved to 'scholar_articles/' folder.")
