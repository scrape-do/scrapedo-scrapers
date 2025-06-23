import requests
import urllib.parse

# Scrape.do token and Bearer token
scrape_token = "<your-token>"
bearer_token = "app#unlogged__XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"  # Replace with real token

# Target API URL
target_url = "https://app.neilpatel.com/api/keyword_info?keyword=ubersuggest&language=en&locId=2840&withGlobalSVBreakdown=true"
encoded_url = urllib.parse.quote_plus(target_url)

# Scrape.do API call with Authorization header
api_url = f"https://api.scrape.do/?token={scrape_token}&url={encoded_url}&extraHeaders=true"
headers = {
    "sd-Authorization": f"Bearer {bearer_token}"
}

# Make request and parse response
response = requests.get(api_url, headers=headers)
data = response.json()

# Extract and print volume and CPC
keyword_info = data.get("keywordInfo", {})
volume = keyword_info.get("volume")
cpc = keyword_info.get("cpc")

print("Search Volume:", volume)
print("CPC:", cpc)
