import requests
import json

token = "<your_token>"
query = "why is pickleball so popular"

# Step 1: Send a standard SERP API request
response = requests.get(
    "https://api.scrape.do/plugin/google/search",
    params={"token": token, "q": query, "gl": "us", "hl": "en"},
    timeout=60,
)
response.raise_for_status()
serp_data = response.json()

# Step 2: Check AI Overview state
ai_overview = serp_data.get("ai_overview")

if ai_overview is None:
    print("No AI Overview returned for this query.")
elif ai_overview["state"] == "complete":
    print("AI Overview returned inline (state: complete).")
elif ai_overview["state"] == "deferred":
    print("AI Overview deferred. Fetching via async endpoint (5 credits)...")
    session_key = ai_overview["session_key"]

    # Fetch the deferred AI Overview within 60 seconds
    aio_response = requests.get(
        "https://api.scrape.do/plugin/google/search/ai-overview",
        params={"token": token, "session_key": session_key},
        timeout=60,
    )
    aio_response.raise_for_status()
    ai_overview = aio_response.json()
    print("AI Overview fetched from async endpoint.")

# Step 3: Extract and save AI Overview data
result = {
    "query": query,
    "ai_overview_state": ai_overview["state"] if ai_overview else None,
    "text_blocks": ai_overview.get("text_blocks", []) if ai_overview else [],
    "references": ai_overview.get("references", []) if ai_overview else [],
}

with open("serp-api-ai-overview.json", "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2, ensure_ascii=False)

print(f"\nQuery: '{query}'")
print(f"State: {result['ai_overview_state']}")
print(f"Text blocks: {len(result['text_blocks'])}")
print(f"References: {len(result['references'])}")
for ref in result["references"][:3]:
    print(f"  - {ref['title']} ({ref.get('source', '')})")
print("Saved to serp-api-ai-overview.json")
