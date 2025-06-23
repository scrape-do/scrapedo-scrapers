import requests
import urllib.parse
from bs4 import BeautifulSoup

# Your Scrape.do token and search query
scrape_token = "<your-token>"
query = "python web scraping"

# Encode the search query and build Google URL
encoded_query = urllib.parse.quote_plus(query)
google_url = f"https://www.google.com/search?q={encoded_query}&start=0"  # start=0 for first page

# Scrape.do wrapper URL - properly encode the Google URL
api_url = f"https://api.scrape.do/?token={scrape_token}&url={urllib.parse.quote(google_url, safe='')}"

# Send the request
response = requests.get(api_url)
response.raise_for_status()

# Parse the HTML
soup = BeautifulSoup(response.text, 'html.parser')

# Find all search results with Ww4FFb class
search_results = soup.find_all('div', class_=lambda x: x and 'Ww4FFb' in x)

# Extract data from each result
for position, result in enumerate(search_results, 1):
    # Get title from h3 tag
    title = result.find('h3').get_text(strip=True)

    # Get URL from link
    url = result.find('a').get('href')

    # Get description/snippet
    desc_element = result.find(class_='VwiC3b')
    description = desc_element.get_text(strip=True) if desc_element else "No description"

    print(f"{position}. {title}")
    print(f"   URL: {url}")
    print(f"   Description: {description}")
    print()
