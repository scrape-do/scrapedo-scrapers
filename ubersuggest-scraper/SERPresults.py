import requests
import urllib.parse

# Scrape.do token and Bearer token
scrape_token = "<your-token>"
bearer_token = "app#unlogged__XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

# Target API URL
target_url = "https://app.neilpatel.com/api/serp_analysis?keyword=ubersuggest&locId=2840&language=en&refresh=false"
encoded_url = urllib.parse.quote_plus(target_url)

# Scrape.do API call with Authorization header
api_url = f"https://api.scrape.do/?token={scrape_token}&url={encoded_url}&extraHeaders=true"
headers = {
    "sd-Authorization": f"Bearer {bearer_token}"
}

# Make request and parse response
response = requests.get(api_url, headers=headers)
data = response.json()

# Extract and print structured search results
serp_entries = data.get("serpEntries", [])

for entry in serp_entries:
    print("—" * 60)
    print(f"Position: {entry.get('position')}")
    print(f"Title   : {entry.get('title') or 'N/A'}")
    print(f"Domain  : {entry.get('domain')}")
    print(f"URL     : {entry.get('url')}")
    print(f"Type    : {entry.get('type')}")
    
    clicks = entry.get("clicks")
    if clicks is not None:
        print(f"Clicks  : {clicks}")
        
    domain_authority = entry.get("domainAuthority")
    if domain_authority is not None:
        print(f"DA      : {domain_authority}")
