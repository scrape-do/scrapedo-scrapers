import requests
import urllib.parse
import json
import csv


token = "<your_token>"
query = "<search_query>"

# Number of images to display (max 500)
display_count = 30

# Build the Naver image search API URL
# This endpoint returns JSONP data for image search results
url = f"https://s.search.naver.com/p/c/image/search.naver?json_type=6&query={urllib.parse.quote(query)}&_callback=getPhoto&display={display_count}"

# Scrape.do API endpoint with South Korean IP address, enable super=true on Scrape.do API for better results
api_url = f"https://api.scrape.do?token={token}&url={urllib.parse.quote_plus(url)}&geoCode=kr"

# Send the request
resp = requests.get(api_url)

# Check if the request was successful
if resp.status_code == 200:
    content = resp.text
    # Remove the JSONP callback wrapper: getPhoto(...)
    if content.startswith('getPhoto('):
        start = 9  # Length of 'getPhoto('
        end = content.rfind(')')
        json_content = content[start:end] if end > start else content[start:]
    else:
        json_content = content
    try:
        # Parse the JSON data
        data = json.loads(json_content)
        items = data.get('items', [])
        # Extract title, link, and original image URL for each result
        results = [[item.get('title', ''), item.get('link', ''), item.get('originalUrl', '')] for item in items]
        # Export to CSV
        with open("naver_images_results.csv", "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow(["Title", "Link", "Original URL"])
            writer.writerows(results)
        print(f"✅ Found {len(results)} images\n✅ Data saved to naver_images_results.csv")
    except json.JSONDecodeError as e:
        print(f"❗ JSON parsing error: {e}\nResponse content: {content[:500]}")
else:
    print(f"❗ Request failed with status code {resp.status_code}\nCheck if your token is valid and geo-restrictions are handled.")