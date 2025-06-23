import requests
import urllib.parse
from bs4 import BeautifulSoup
import time

# Your Scrape.do token and search query
scrape_token = "<your-token>"
query = "python web scraping"

# Starting page
start = 0
all_results = []

while True:
    print(f"Scraping page {(start // 10) + 1} (results {start + 1}-{start + 10})...")

    # Encode the search query and build Google URL
    encoded_query = urllib.parse.quote_plus(query)
    google_url = f"https://www.google.com/search?q={encoded_query}&start={start}"

    # Scrape.do wrapper URL - properly encode the Google URL
    api_url = f"https://api.scrape.do/?token={scrape_token}&url={urllib.parse.quote(google_url, safe='')}"

    # Send the request
    response = requests.get(api_url)
    response.raise_for_status()

    # Parse the HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all search results with Ww4FFb class
    search_results = soup.find_all('div', class_=lambda x: x and 'Ww4FFb' in x)

    # Break if no results found
    if not search_results:
        print("No more results found!")
        break

    # Extract data from each result
    for result in search_results:
        title = result.find('h3').get_text(strip=True)
        url = result.find('a').get('href')
        desc_element = result.find(class_='VwiC3b')
        description = desc_element.get_text(strip=True) if desc_element else "No description"

        all_results.append({
            'position': len(all_results) + 1,
            'title': title,
            'url': url,
            'description': description
        })

    start += 10
    time.sleep(1)  # optional delay to mimic human browsing

# Print all results
print(f"\n=== Found {len(all_results)} total results ===\n")

for result in all_results:
    print(f"{result['position']}. {result['title']}")
    print(f"   URL: {result['url']}")
    print(f"   Description: {result['description']}")
    print()
