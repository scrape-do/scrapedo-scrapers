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

# Find all related search terms
related_searches = soup.find_all('div', class_='b2Rnsc vIifob')

print(f"Found {len(related_searches)} related search terms")

# Extract related search terms
for position, search_term in enumerate(related_searches, 1):
    term_text = search_term.get_text(strip=True)
    print(f"{position}. {term_text}")
