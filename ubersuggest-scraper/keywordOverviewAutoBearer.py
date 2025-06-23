import requests
import urllib.parse

# Scrape.do token
scrape_token = "<your-token>"

# Keyword API and Token API URLs
keyword_url = "https://app.neilpatel.com/api/keyword_info?keyword=ubersuggest&language=en&locId=2840&withGlobalSVBreakdown=true"
token_url = "https://app.neilpatel.com/api/get_token"

# Encode keyword URL
encoded_keyword_url = urllib.parse.quote_plus(keyword_url)
scrape_keyword_api = f"https://api.scrape.do/?token={scrape_token}&url={encoded_keyword_url}&extraHeaders=true"

# Function to fetch fresh token
def fetch_token():
    token_api = f"https://api.scrape.do/?token={scrape_token}&url={token_url}"
    resp = requests.get(token_api)
    resp.raise_for_status()
    return resp.json()["token"]

# Function to get keyword data
def get_keyword_data(bearer_token):
    headers = {"sd-Authorization": f"Bearer {bearer_token}"}
    resp = requests.get(scrape_keyword_api, headers=headers)
    if resp.status_code != 200:
        raise RuntimeError(f"Request failed with status {resp.status_code}")
    return resp.json()

# Run with token handling
cached_token = None
try:
    if cached_token is None:
        cached_token = fetch_token()
    data = get_keyword_data(cached_token)
except Exception:
    cached_token = fetch_token()
    data = get_keyword_data(cached_token)

# Extract and print volume and CPC
keyword_info = data.get("keywordInfo", {})
volume = keyword_info.get("volume")
cpc = keyword_info.get("cpc")

print("Search Volume:", volume)
print("CPC:", cpc)
