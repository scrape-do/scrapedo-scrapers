import requests
import urllib.parse
from bs4 import BeautifulSoup

# Your Scrape.do token and search query
scrape_token = "<your-token>"
query = "python web scraping"

# Encode the search query and build Google URL
encoded_query = urllib.parse.quote_plus(query)
google_url = f"https://www.google.com/search?q={encoded_query}"

# Scrape.do wrapper URL - properly encode the Google URL
api_url = f"https://api.scrape.do/?token={scrape_token}&url={urllib.parse.quote(google_url, safe='')}"

# Send the request
response = requests.get(api_url)
response.raise_for_status()

# Parse the HTML
soup = BeautifulSoup(response.text, 'html.parser')

# Find all FAQ sections with yEVEwb
faq_results = soup.find_all('div', jsname='yEVEwb')

# Extract FAQ questions
for position, faq in enumerate(faq_results, 1):
    question_element = faq.find('span')
    if question_element:
        question = question_element.get_text(strip=True)
        print(f"{position}. {question}")
