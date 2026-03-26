import requests
import json

token = "<your_token>"
query = "python web scraping"

# The SERP API returns structured JSON for all Google Search result types:
# organic results, ads, FAQs (People Also Ask), and related searches.
url = f"https://api.scrape.do/plugin/google/search?token={token}&q={query}&hl=en&gl=us"

response = requests.get(url, timeout=60)

if response.status_code != 200:
    print(f"Request failed: {response.status_code}")
    exit()

data = response.json()

# Organic results
organic = data.get("organic_results", [])
print(f"Organic results: {len(organic)}")
for r in organic[:5]:
    print(f"  {r['position']}. {r['title']} - {r['link']}")

# Paid ads (top and bottom)
top_ads = data.get("top_ads", [])
bottom_ads = data.get("bottom_ads", [])
print(f"\nTop ads: {len(top_ads)}, Bottom ads: {len(bottom_ads)}")
for ad in top_ads:
    print(f"  [{ad['position']}] {ad['title']} - {ad['url']}")

# People Also Ask
related_questions = data.get("related_questions", [])
print(f"\nPeople Also Ask: {len(related_questions)}")
for q in related_questions:
    print(f"  - {q['question']}")

# Related searches
related_searches = data.get("related_searches", [])
print(f"\nRelated searches: {len(related_searches)}")
for s in related_searches:
    print(f"  - {s['query']}")

# Save full response
with open("serp-api-search-results.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"\nFull SERP data saved to serp-api-search-results.json")
