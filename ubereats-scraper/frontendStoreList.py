import requests
import urllib.parse
import csv
import json
from bs4 import BeautifulSoup

# --- Scrape.do token and Uber Eats frontend URL ---
scrape_token = "<your-token>"
# 'pl' parameter encodes the location; extract from Uber Eats URL after you select an address
ubereats_pl = "<your-pl>" # e.g.JTdCJTIyYWRkcmVzcyUyMiUzQSUyMkNlbnRyYWwlMjBQYXJrJTIyJTJDJTIycmVmZXJlbmNlJTIyJTNBJTIyQ2hJSjR6R0ZBWnBZd29rUkdVR3BoM01mMzdrJTIyJTJDJTIycmVmZXJlbmNlVHlwZSUyMiUzQSUyMmdvb2dsZV9wbGFjZXMlMjIlMkMlMjJsYXRpdHVkZSUyMiUzQTQwLjc4MjU1NDclMkMlMjJsb25naXR1ZGUlMjIlM0EtNzMuOTY1NTgzNCU3RA==
ubereats_url = f"https://www.ubereats.com/feed?diningMode=DELIVERY&pl={ubereats_pl}"

# --- Browser automation sequence for Scrape.do (clicks 'Show more' repeatedly until no more found) ---
play_with_browser = [
    {"action": "WaitSelector", "timeout": 30000, "waitSelector": "button, div, span"},
    {"action": "Execute", "execute": "(async()=>{let attempts=0;while(attempts<20){let btn=Array.from(document.querySelectorAll('button, div, span')).filter(e=>e.textContent.trim()==='Show more')[0];if(!btn)break;btn.scrollIntoView({behavior:'smooth'});btn.click();await new Promise(r=>setTimeout(r,1800));window.scrollTo(0,document.body.scrollHeight);await new Promise(r=>setTimeout(r,1200));attempts++;}})();"},
    {"action": "Wait", "timeout": 3000}
]

# --- Prepare Scrape.do API URL ---
jsonData = urllib.parse.quote_plus(json.dumps(play_with_browser))
api_url = (
    f"https://api.scrape.do/?url={urllib.parse.quote_plus(ubereats_url)}"
    f"&token={scrape_token}"
    f"&super=true"
    f"&render=true"
    f"&playWithBrowser={jsonData}"
)

# --- Fetch the rendered Uber Eats page ---
response = requests.get(api_url)

# --- Parse the HTML with BeautifulSoup ---
soup = BeautifulSoup(response.text, "html.parser")
store_cards = soup.find_all('div', {'data-testid': 'store-card'})

# --- Helper to get first text from selectors ---
def get_first_text(element, selectors):
    for sel in selectors:
        found = element.select_one(sel)
        if found and found.get_text(strip=True):
            return found.get_text(strip=True)
    return ''

# --- Extract store data from each card ---
results = []
for card in store_cards:
    a_tag = card.find('a', {'data-testid': 'store-card'})
    href = a_tag['href'] if a_tag and a_tag.has_attr('href') else ''
    h3 = a_tag.find('h3').get_text(strip=True) if a_tag and a_tag.find('h3') else ''
    promo = ''
    promo_div = card.select_one('div.ag.mv.mw.al.bh.af')
    if not promo_div:
        promo_div = card.find('span', {'data-baseweb': 'tag'})
    if promo_div:
        promo = ' '.join(promo_div.stripped_strings)
    rating = get_first_text(card, [
        'span.bo.ej.ds.ek.b1',
        'span[title][class*=b1]'
    ])
    review_count = ''
    for span in card.find_all('span'):
        txt = span.get_text(strip=True)
        if txt.startswith('(') and txt.endswith(')'):
            review_count = txt
            break
    if not review_count:
        review_count = get_first_text(card, [
            'span.bo.ej.bq.dt.nq.nr',
            'span[class*=nq][class*=nr]'
        ])
    results.append({
        'href': href,
        'name': h3,
        'promotion': promo,
        'rating': rating,
        'review_count': review_count
    })

# --- Write results to CSV ---
with open('ubereats_store_cards.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['href', 'name', 'promotion', 'rating', 'review_count']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for row in results:
        writer.writerow(row)
print(f"Wrote {len(results)} store cards to ubereats_store_cards.csv")
