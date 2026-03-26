import json
import os
import urllib.parse
import requests
from bs4 import BeautifulSoup
import time

TOKEN = "<your_token>"
SEARCH_QUERY = "artificial intelligence"
MIN_RESULTS = 20
MAX_PAGES = 5
BASE_URL = f"https://www.google.com/search?q={urllib.parse.quote_plus(SEARCH_QUERY)}&tbm=nws&hl=en"

all_results = []

# Google's News tab shows ~10 results per page. We paginate with the `start`
# parameter and keep going until we hit MIN_RESULTS or run out of pages.
for page_num in range(MAX_PAGES):
    if len(all_results) >= MIN_RESULTS:
        break

    start_index = page_num * 10
    page_url = BASE_URL if page_num == 0 else f"{BASE_URL}&start={start_index}"

    print(f"Scraping page {page_num + 1}/{MAX_PAGES}...")

    # Google's News tab needs super=true for bot protection. If that returns
    # nothing, we retry with render=true since some pages need full JS execution.
    api_url = f"http://api.scrape.do/?token={TOKEN}&url={urllib.parse.quote(page_url)}&super=true"
    response = requests.get(api_url, timeout=60)
    soup = BeautifulSoup(response.text, "html.parser")

    # Each news card sits inside a container div. We try multiple known selectors
    # because Google rotates class names between updates.
    containers = soup.select("div.SoaBEf, div.dbsr, div.Gx5Zad, div.xuvV6b")
    if not containers:
        containers = [tag.parent for tag in soup.find_all("div", {"role": "heading"}) if tag.parent]

    # If we still got nothing, retry the same page with render=true.
    if not containers:
        print("  No results with super=true, retrying with render=true...")
        api_url = f"http://api.scrape.do/?token={TOKEN}&url={urllib.parse.quote(page_url)}&super=true&render=true"
        response = requests.get(api_url, timeout=90)
        soup = BeautifulSoup(response.text, "html.parser")
        containers = soup.select("div.SoaBEf, div.dbsr, div.Gx5Zad, div.xuvV6b")
        if not containers:
            containers = [tag.parent for tag in soup.find_all("div", {"role": "heading"}) if tag.parent]

    if not containers:
        print("  No results found on this page, stopping pagination.")
        break

    page_count = 0
    for card in containers:
        link_elem = card.find("a", href=True)
        if not link_elem:
            continue

        # Google wraps article URLs in /url?q= redirects. Unwrap to get the real link.
        link = link_elem["href"]
        if link.startswith("/url?"):
            qs = urllib.parse.parse_qs(urllib.parse.urlparse(link).query)
            link = qs.get("q", [link])[0]
        if not link or "google.com" in link:
            continue

        title_elem = card.find("div", {"role": "heading"}) or card.find("h3")
        title = title_elem.get_text(strip=True) if title_elem else None
        if not title or len(title) < 5:
            continue

        # Source and date live in small text elements with varying class names.
        source = None
        for sel in ["div.MgUUmf", "span.MgUUmf", "div.CEMjEf span", "div.ca-authority"]:
            elem = card.select_one(sel)
            if elem:
                source = elem.get_text(strip=True)
                break

        date = None
        for sel in ["span.WG9SHc", "div.OSrXXb span", "time", "span.r0bn4c", "span.f"]:
            elem = card.select_one(sel)
            if elem:
                date = elem.get_text(strip=True)
                break
        if not date:
            time_elem = card.find("time")
            if time_elem:
                date = time_elem.get("datetime") or time_elem.get_text(strip=True)

        # The description is the longest text block that isn't the title, source, or date.
        description = None
        for elem in card.find_all(["div", "span"]):
            if elem.find(["div", "span", "a", "h3"]):
                continue
            text = elem.get_text(strip=True)
            if text and text != title and text != source and text != date and len(text) > 40:
                description = text
                break

        all_results.append({
            "title": title,
            "source": source,
            "date": date,
            "description": description,
            "link": link,
        })
        page_count += 1

    print(f"  Found {page_count} results (total: {len(all_results)})")
    time.sleep(1)

with open("news_search_results.json", "w", encoding="utf-8") as f:
    json.dump(all_results, f, indent=2, ensure_ascii=False)

for i, r in enumerate(all_results, 1):
    print(f"\n--- Result {i} ---")
    print(f"Title:       {r['title']}")
    print(f"Source:      {r['source']}")
    print(f"Date:        {r['date']}")
    print(f"Description: {r['description'][:100]}..." if r["description"] else "Description: N/A")
    print(f"Link:        {r['link']}")

print(f"\nTotal: {len(all_results)} news articles saved to news_search_results.json")


# =============================================================================
# BONUS: Download extracted article links as Markdown
# =============================================================================
# Same progressive fallback we use in the scholar scraper:
#   1. Try a basic request (cheapest, fastest)
#   2. If that fails, escalate to super=true
#   3. Still no luck? Go full power with super=true & render=true

os.makedirs("news_articles", exist_ok=True)

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
        with open(f"news_articles/{i + 1:02d}_{safe_name}.md", "w", encoding="utf-8") as f:
            f.write(content)
    else:
        print("    Could not download this article with any strategy.")

    time.sleep(1)

print(f"\nArticles saved to 'news_articles/' folder.")
