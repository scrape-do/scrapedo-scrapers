import requests
import urllib.parse
from bs4 import BeautifulSoup
import csv
import time
import re
import json

# Your Scrape.do token
token = "<your_token>"

# Search query
query = "<search_query>"

def scrape_page(page_num, start_num):
    """Scrape a single page of organic search results"""
    
    # Build URL with pagination, enable super=true on Scrape.do API for better results
    target_url = f"https://search.naver.com/search.naver?where=web&query={urllib.parse.quote(query)}&page={page_num}&start={start_num}"
    api_url = f"https://api.scrape.do?token={token}&url={urllib.parse.quote_plus(target_url)}&geoCode=kr&super=true"
    
    response = requests.get(api_url)
    if response.status_code != 200:
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    results = []
    
    # Extract search results from JavaScript data
    script_tags = soup.find_all('script')
    for script in script_tags:
        if script.string and 'entry.bootstrap' in script.string:
            try:
                script_content = script.string
                
                # Find the JSON object passed to entry.bootstrap
                start_pos = script_content.find('entry.bootstrap(')
                if start_pos == -1:
                    continue
                
                # Find the first opening brace after the function call
                brace_start = script_content.find('{', start_pos)
                if brace_start == -1:
                    continue
                
                # Count braces to find the matching closing brace
                brace_count = 0
                end_pos = brace_start
                for i, char in enumerate(script_content[brace_start:], brace_start):
                    if char == '{':
                        brace_count += 1
                    elif char == '}':
                        brace_count -= 1
                        if brace_count == 0:
                            end_pos = i
                            break
                
                json_str = script_content[brace_start:end_pos + 1]
                
                # Parse the JSON data
                data = json.loads(json_str)
                
                # Extract search results from the data structure
                if 'body' in data and 'props' in data['body'] and 'children' in data['body']['props']:
                    children = data['body']['props']['children']
                    if len(children) > 0 and 'props' in children[0] and 'children' in children[0]['props']:
                        search_items = children[0]['props']['children']
                        
                        for item in search_items:
                            if 'props' in item:
                                props = item['props']
                                
                                # Extract title, URL, and description
                                title = props.get('title', 'No title')
                                url = props.get('href', '')
                                body_text = props.get('bodyText', 'No description available')
                                
                                # Clean up HTML markup from title and description
                                title = re.sub(r'<[^>]+>', '', title).strip()
                                body_text = re.sub(r'<[^>]+>', '', body_text).strip()
                                
                                # Only add if we have a valid URL
                                if url and url.startswith('http'):
                                    results.append([title, url, body_text])
                
                break  # Found the data, no need to check other scripts
                
            except (json.JSONDecodeError, KeyError, IndexError) as e:
                print(f"Error parsing JavaScript data on page {page_num}: {e}")
                continue
    
    return results

# Main scraping
all_results = []
page_num = 1

print(f"🔍 Scraping: {query}")

while page_num <= 10:
    start_num = (page_num - 1) * 15 + 1
    print(f"📄 Page {page_num}...")
    
    page_results = scrape_page(page_num, start_num)
    retry_count = 0
    
    # Retry logic for pages 1-9
    while not page_results and retry_count < 2 and page_num < 10:
        retry_count += 1
        print(f"🔄 Retrying page {page_num}... ({retry_count}/2)")
        time.sleep(5)
        page_results = scrape_page(page_num, start_num)
    
    if not page_results:
        print(f"📄 No more results on page {page_num}")
        break
    
    all_results.extend(page_results)
    print(f"✅ {len(page_results)} results")
    
    page_num += 1
    time.sleep(2)

# Save results
if all_results:
    with open("naver_organic_results.csv", "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["Title", "URL", "Description"])
        writer.writerows(all_results)
    
    print(f"✅ Total: {len(all_results)} results across {page_num - 1} pages")
    print("✅ Saved to naver_organic_results.csv")
else:
    print("❗ No results found")