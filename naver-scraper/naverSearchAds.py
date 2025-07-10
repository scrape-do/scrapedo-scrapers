import requests
import urllib.parse
from bs4 import BeautifulSoup
import csv

# Your Scrape.do token
token = "<your_token>"

# Search query
query = "<search_query>"

# Build the Naver search ads URL
target_url = f"https://ad.search.naver.com/search.naver?where=ad&query={urllib.parse.quote(query)}"
encoded_url = urllib.parse.quote_plus(target_url)

# Scrape.do API endpoint with South Korean IP addresses, enable super=true on Scrape.do API for better results
api_url = f"https://api.scrape.do?token={token}&url={encoded_url}&geoCode=kr"

# Send the request
response = requests.get(api_url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all ad containers (li elements with data-index)
    ad_containers = soup.find_all('li', attrs={'data-index': True})
    
    ads_data = []
    
    for container in ad_containers:
        try:
            # Find the tit_wrap link within this ad container
            tit_wrap = container.find('a', class_='tit_wrap')
            if not tit_wrap:
                continue
                
            # Extract the URL from the tit_wrap link
            url = tit_wrap.get('href', '')
            # Clean up the URL if it's a relative path
            if url.startswith('/'):
                url = f"https://search.naver.com{url}"
            
            # Extract the title (all text from tit_wrap)
            title = tit_wrap.get_text(strip=True)
            
            # Find the description from the desc_area within this container
            desc_area = container.find('div', class_='desc_area')
            if desc_area:
                description = desc_area.get_text(strip=True)
            else:
                description = "No description available"
            
            # Add to results
            ads_data.append([title, url, description])
            
        except Exception as e:
            print(f"Error processing ad container: {e}")
            continue
    
    # Export to CSV
    with open("naver_ads_data.csv", "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["Title", "URL", "Description"])
        writer.writerows(ads_data)
    
    print(f"✅ Found {len(ads_data)} ads")
    print("✅ Data saved to naver_ads_data.csv")

else:
    print(f"❗ Request failed with status code {response.status_code}")
    print("Check if your token is valid and geo-restrictions are handled.")
