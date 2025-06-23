import requests
import urllib.parse
from bs4 import BeautifulSoup

# Your Scrape.do token and search query
scrape_token = "<your-token>"
query = "python web scraping"

# Encode the search query and build Google URL
encoded_query = urllib.parse.quote_plus(query)
google_url = f"https://www.google.com/search?q={encoded_query}"

# Scrape.do wrapper URL
api_url = f"https://api.scrape.do/?token={scrape_token}&url={urllib.parse.quote(google_url, safe='')}"

# Send the request
response = requests.get(api_url)
response.raise_for_status()

# Parse the HTML
soup = BeautifulSoup(response.text, 'html.parser')

# Find all search ads using uEierd class
search_ads = soup.find_all('div', class_='uEierd')

print(f"Found {len(search_ads)} search ads")

# Extract ad information
for position, ad in enumerate(search_ads, 1):
    print(f"\n--- Ad {position} ---")

    # Extract URL
    url_element = ad.find('a')
    url = url_element.get('href') if url_element else "URL: Not found"
    print(f"URL: {url}")

    # Extract title
    title_element = ad.find(['h3', 'div'], class_=lambda x: x and any(cls in str(x) for cls in ['CCgQ5', 'vCa9Yd', 'QfkTvb']))
    if not title_element:
        title_element = ad.find(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    title = title_element.get_text(strip=True) if title_element else "Title: Not found"
    print(f"Title: {title}")

    # Extract description
    description_element = ad.find('div', class_=lambda x: x and any(cls in str(x) for cls in ['Va3FIb', 'r025kc', 'lVm3ye']))
    if not description_element:
        description_spans = ad.find_all('span')
        description_texts = [
            span.get_text(strip=True)
            for span in description_spans
            if len(span.get_text(strip=True)) > 20 and span.get_text(strip=True) not in ['Sponsored', 'Ad']
        ]
        description = ' '.join(description_texts) if description_texts else "Description: Not found"
    else:
        description = description_element.get_text(strip=True)
    print(f"Description: {description}")

    # Extract displayed (vanity) URL
    display_url_element = ad.find('span', class_=lambda x: x and 'qzEoUe' in str(x))
    display_url = display_url_element.get_text(strip=True) if display_url_element else "Display URL: Not found"
    print(f"Display URL: {display_url}")
