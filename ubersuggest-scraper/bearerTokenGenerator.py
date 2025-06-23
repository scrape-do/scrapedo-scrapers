import requests

# Scrape.do token and target URL
scrape_token = "<your-token>"
target_url = "https://app.neilpatel.com/api/get_token"

# Scrape.do wrapper URL
api_url = f"https://api.scrape.do/?token={scrape_token}&url={target_url}"

# Send the request
response = requests.get(api_url)
response.raise_for_status()

# Parse and print the token
data = response.json()
print("Token:", data["token"])
