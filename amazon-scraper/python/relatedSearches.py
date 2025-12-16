import urllib.parse
import requests
from bs4 import BeautifulSoup

# Configuration
token = "<SDO-token>"
search_query = "laptop stands"  # Change this to any search term
geocode = "us"
zipcode = "10001"

# Build search URL
target_url = f"https://www.amazon.com/s?k={urllib.parse.quote_plus(search_query)}"

targetUrl = urllib.parse.quote(target_url)
apiUrl = "https://api.scrape.do/plugin/amazon/?token={}&url={}&geocode={}&zipcode={}&output=html".format(token, targetUrl, geocode, zipcode)
response = requests.request("GET", apiUrl)

soup = BeautifulSoup(response.text, "html.parser")

# Find all related search terms
related_searches = []

for div in soup.find_all("div", class_="a-box-inner a-padding-mini"):
    text = div.get_text(strip=True)
    if text:
        related_searches.append(text)

print(f"Related searches:")
for i, term in enumerate(related_searches, 1):
    print(f"  {i}. {term}")

