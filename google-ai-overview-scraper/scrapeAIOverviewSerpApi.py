import requests
import json
import urllib.parse

# Configuration
token = "<your_token>"
query = "how does photosynthesis work"

# Scrape.do's Google Search API returns structured JSON including
# an ai_overview field when Google shows one for the query.
encoded_query = urllib.parse.quote_plus(query)
url = f"https://api.scrape.do/plugin/google/search?token={token}&q={encoded_query}&hl=en&gl=us"

response = requests.get(url, timeout=60)

if response.status_code != 200:
    print(f"Request failed: {response.status_code}")
    exit()

data = response.json()
ai_overview = data.get("ai_overview")

if not ai_overview:
    print(f"No AI Overview returned for: '{query}'")
    exit()

# The ai_overview field has two possible states:
# "complete" - full content available immediately
# "deferred" - content loads async, requires a follow-up call
state = ai_overview.get("state")
print(f"AI Overview state: {state}")

if state == "deferred":
    # Fetch the deferred content using the session key.
    # Session keys expire after 60 seconds and are single-use.
    session_key = ai_overview.get("session_key")
    print(f"Fetching deferred AI Overview (session: {session_key[:8]}...)")

    aio_url = f"https://api.scrape.do/plugin/google/search/ai-overview?token={token}&session_key={session_key}"
    aio_response = requests.get(aio_url, timeout=30)

    if aio_response.status_code != 200:
        print(f"Deferred fetch failed: {aio_response.status_code}")
        exit()

    ai_overview = aio_response.json().get("ai_overview") or {}


# The text_blocks array contains paragraphs and lists. Paragraph blocks
# may have a "snippet" key, or be empty placeholders. List blocks nest
# their content inside a "list" array with "snippet" fields.
def flatten_blocks(blocks):
    flat = []
    for block in blocks:
        btype = block.get("type", "paragraph")
        snippet = block.get("snippet", "")
        if snippet:
            flat.append({"type": btype, "text": snippet})
        for item in block.get("list", []):
            item_text = item.get("snippet", "")
            if item_text:
                flat.append({"type": "list_item", "text": item_text})
            for sub in item.get("list", []):
                sub_text = sub.get("snippet", "")
                if sub_text:
                    flat.append({"type": "list_item", "text": sub_text})
    return flat


raw_blocks = ai_overview.get("text_blocks", [])
text_blocks = flatten_blocks(raw_blocks)
references = ai_overview.get("references", [])

result = {
    "query": query,
    "ai_overview_found": True,
    "state": state,
    "text_blocks": text_blocks,
    "references": [
        {"title": ref.get("title", ""), "url": ref.get("link", ""), "source": ref.get("source", "")}
        for ref in references
    ],
}

output_file = "ai-overview-serp-api-results.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2, ensure_ascii=False)

print(f"AI Overview extracted for: '{query}'")
print(f"  {len(text_blocks)} text blocks, {len(references)} references")
print(f"Saved to {output_file}")
