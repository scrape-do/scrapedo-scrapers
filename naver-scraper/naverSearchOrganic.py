import requests
import urllib.parse
from bs4 import BeautifulSoup
import csv
import time

# Your Scrape.do token
token = "<your_token>"

# Search query
query = "<search_query>"

def scrape_page(page_num, start_num):
    """Scrape a single page of organic search results"""
    
    # Build URL with pagination, enable super=true on Scrape.do API for better results
    target_url = f"https://search.naver.com/search.naver?where=web&query={urllib.parse.quote(query)}&page={page_num}&start={start_num}"
    api_url = f"https://api.scrape.do?token={token}&url={urllib.parse.quote_plus(target_url)}&geoCode=kr"
    
    response = requests.get(api_url)
    if response.status_code != 200:
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    results = []
    
    for container in soup.find_all('li', class_='bx'):
        try:
            title_link = container.find('a', class_='link_tit')
            if not title_link:
                continue
            
            title = title_link.get_text(strip=True)
            url = title_link.get('href', '')
            
            # Try to find description with multiple selectors
            description = "No description available"
            
            # Try different description selectors
            desc_selectors = [
                'a.api_txt_lines.total_dsc',
                'div.total_dsc_wrap a',
                'div.total_dsc_wrap',
                'a.link_dsc',
                'div.dsc'
            ]
            
            for selector in desc_selectors:
                desc = container.select_one(selector)
                if desc:
                    description = desc.get_text(strip=True)
                    break
            
            # Fallback: try to get text from total_group
            if description == "No description available":
                total_group = container.find('div', class_='total_group')
                if total_group:
                    all_text = total_group.get_text(strip=True)
                    title_text = title_link.get_text(strip=True)
                    # Remove title from description
                    description = all_text.replace(title_text, '').strip()
                    if not description:
                        description = "No description available"
            
            results.append([title, url, description])
            
        except Exception as e:
            print(f"Error on page {page_num}: {e}")
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
