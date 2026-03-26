import requests
import json

token = "<your_token>"
query = "wireless gaming headset"

# The AI Mode endpoint returns AI-generated product recommendations
# with text_blocks, references, and sometimes shopping_results.
url = f"https://api.scrape.do/plugin/google/search/ai-mode?token={token}&q={query}&hl=en&gl=us"

response = requests.get(url, timeout=60)

if response.status_code != 200:
    print(f"Request failed: {response.status_code}")
    exit()

data = response.json()

# Shopping results with pricing, ratings, and source links
shopping = data.get("shopping_results", [])
print(f"Shopping results: {len(shopping)}")
for item in shopping:
    print(f"\n  {item.get('title', 'N/A')}")
    print(f"    Price: {item.get('price', 'N/A')}")
    print(f"    Source: {item.get('source', 'N/A')}")

# AI-generated text blocks (recommendations, comparisons).
# Each block has a type, snippet, and optional reference_indexes.
text_blocks = data.get("text_blocks", [])
print(f"\nAI text blocks: {len(text_blocks)}")
for block in text_blocks[:5]:
    snippet = block.get("snippet", "")
    if snippet:
        print(f"  [{block.get('type', '?')}] {snippet[:120]}")

# References cited by the AI
references = data.get("references", [])
print(f"\nReferences: {len(references)}")
for ref in references[:5]:
    print(f"  {ref.get('title', 'N/A')} ({ref.get('source', 'N/A')})")
    print(f"    {ref.get('link', 'N/A')}")

with open("serp-api-shopping-results.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"\nSaved to serp-api-shopping-results.json")
