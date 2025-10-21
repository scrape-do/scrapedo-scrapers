import requests
import csv
import urllib.parse
from bs4 import BeautifulSoup

# Configuration
token = "<your-token>"
query = "when was coffee invented"
max_pages = 10

all_results = []
page = 0
empty_count = 0

print(f"Starting scrape for: '{query}'")
print(f"Max pages: {max_pages}\n")

while page < max_pages:
    # Calculate offset (page 0 = no first param, page 1 = first=11, page 2 = first=21, etc.)
    if page == 0:
        page_url = f"https://www.bing.com/search?q={query}"
    else:
        first = 1 + (page * 10)
        page_url = f"https://www.bing.com/search?q={query}&first={first}"
    
    # URL encode the target URL for Scrape.do
    encoded_url = urllib.parse.quote(page_url, safe='')
    api_url = f"http://api.scrape.do?token={token}&url={encoded_url}&geoCode=us"
    
    offset_str = "first page" if page == 0 else f"first={first}"
    print(f"Page {page + 1} ({offset_str})...", end=" ")
    
    # Send request
    response = requests.get(api_url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Extract results from this page
    page_results = []
    for result in soup.find_all("li", class_="b_algo"):
        try:
            # Extract title and link
            h2_tag = result.find("h2")
            title = h2_tag.get_text(strip=True)
            link = h2_tag.find("a")["href"]
            
            # Extract description (may not always exist)
            desc_tag = result.find("p", class_="b_lineclamp2")
            description = desc_tag.get_text(strip=True) if desc_tag else ""
            
            page_results.append({
                "title": title,
                "url": link,
                "description": description
            })
        except:
            continue
    
    # Check if we found results
    if len(page_results) == 0:
        empty_count += 1
        print(f"No results (empty count: {empty_count}/2)")
        
        # Stop if we get 2 consecutive empty pages
        if empty_count >= 2:
            print("No more results found (confirmed with 2 retries)")
            break
    else:
        empty_count = 0
        all_results.extend(page_results)
        print(f"Found {len(page_results)} results (total: {len(all_results)})")
    
    page += 1

# Save all results to CSV
print(f"\nSaving {len(all_results)} results to CSV...")
with open("bing_search_results.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["title", "url", "description"])
    writer.writeheader()
    writer.writerows(all_results)

print(f"Done! Extracted {len(all_results)} results across {page} pages -> bing_search_results.csv")
