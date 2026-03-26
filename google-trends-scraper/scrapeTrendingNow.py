import requests
import urllib.parse
import json
import re
from bs4 import BeautifulSoup

# Configuration
token = "<your_token>"
geo = "US"
hours = 24  # 4, 24, 48, or 168 (7 days)
fetch_articles = True  # Set False to skip detail extraction (saves API credits)
max_details = 5  # Number of trends to fetch articles for (each costs 1 API call)

target_url = f"https://trends.google.com/trending?geo={geo}&hours={hours}"
encoded_url = urllib.parse.quote_plus(target_url)


def build_api_url(actions):
    encoded_actions = urllib.parse.quote_plus(json.dumps(actions))
    return (
        f"http://api.scrape.do/?token={token}"
        f"&url={encoded_url}&render=true&super=true"
        f"&playWithBrowser={encoded_actions}"
    )


def parse_trends_table(soup):
    trends = []
    for row in soup.select("table tbody tr"):
        cells = row.find_all("td")
        if len(cells) < 5:
            continue

        name_div = cells[1].select_one("div.mZ3RIc")
        if not name_div:
            continue

        vol_text = cells[2].get_text(" ", strip=True)
        vol_match = re.match(r"([\d,]+K?\+?)", vol_text)
        change_match = re.search(r"([\d,]+%)", vol_text)

        started_text = cells[3].get_text(" ", strip=True)
        started_match = re.match(r"([\d]+ \w+ ago)", started_text)

        skip_words = {"Search term", "query_stats", "Explore", ""}
        related = []
        for text_node in cells[4].find_all(string=True):
            t = text_node.strip()
            if t and t not in skip_words and len(t) > 2 and not t.startswith("+"):
                if t not in related:
                    related.append(t)

        trends.append({
            "name": name_div.get_text(strip=True),
            "search_volume": vol_match.group(1) if vol_match else "N/A",
            "volume_change": change_match.group(1) if change_match else "N/A",
            "started": started_match.group(1) if started_match else "N/A",
            "status": "Active" if "Active" in started_text else "Ended",
            "related_queries": related[:5],
            "articles": [],
        })
    return trends


def extract_articles(soup):
    articles = []
    panel = soup.select_one("div.EMz5P")
    if not panel:
        return articles
    for a in panel.find_all("a", href=True):
        href = a["href"]
        if not href.startswith("http") or "google" in href or "gstatic" in href:
            continue
        title_el = a.select_one("div.QbLC8c")
        meta_el = a.select_one("div.pojp0c")
        title = title_el.get_text(strip=True) if title_el else a.get_text(strip=True)
        meta = meta_el.get_text(strip=True) if meta_el else ""
        source, time_ago = "", ""
        if meta:
            parts = meta.split("\u25cf")
            time_ago = parts[0].strip() if parts else ""
            source = parts[1].strip() if len(parts) > 1 else ""
        if title:
            articles.append({"title": title, "url": href, "source": source, "time": time_ago})
    return articles


# Step 1: Fetch the trending table
print(f"Fetching trending topics for geo={geo}, hours={hours}...")
actions = [
    {"Action": "Wait", "Timeout": 5000},
    {"Action": "Wait Selector", "Selector": "table tbody tr"},
]
response = requests.get(build_api_url(actions), timeout=120)

if response.status_code != 200:
    print(f"Request failed: {response.status_code}")
    exit()

soup = BeautifulSoup(response.text, "html.parser")
trends = parse_trends_table(soup)
print(f"Found {len(trends)} trending topics")

# Step 2: Fetch articles for each trend by clicking its row
if fetch_articles and trends:
    limit = min(max_details, len(trends))
    print(f"\nFetching news articles for top {limit} trends...")
    for i, trend in enumerate(trends[:limit]):
        actions = [
            {"Action": "Wait", "Timeout": 5000},
            {"Action": "Wait Selector", "Selector": "table tbody tr[data-row-id]"},
            {"Action": "Click", "Selector": f'table tbody tr[data-row-id="{i}"]'},
            {"Action": "Wait", "Timeout": 3000},
        ]
        resp = requests.get(build_api_url(actions), timeout=120)
        if resp.status_code == 200:
            detail_soup = BeautifulSoup(resp.text, "html.parser")
            trend["articles"] = extract_articles(detail_soup)
        print(f"  [{i+1}/{limit}] {trend['name']}: {len(trend['articles'])} articles")

# Save results
output_file = "trending-now.json"
result = {"geo": geo, "hours": hours, "total_trends": len(trends), "trends": trends}

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2, ensure_ascii=False)

print(f"\nExtracted {len(trends)} trending topics")
for t in trends[:5]:
    related = ", ".join(t["related_queries"][:3])
    arts = f", {len(t['articles'])} articles" if t["articles"] else ""
    print(f"  {t['name']} ({t['search_volume']}, +{t['volume_change']}){arts} - {related}")
print(f"\nSaved to {output_file}")
