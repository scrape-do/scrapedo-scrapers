import requests
import re
import csv
import json
from bs4 import BeautifulSoup

TOKEN = "<your-token>"
STORE_URL = "<store-url>"
API_URL = f"http://api.scrape.do/?token={TOKEN}&super=true&url={STORE_URL}"

response = requests.get(API_URL)
soup = BeautifulSoup(response.text, 'html.parser')

# Assume the menu script and embedded data always exist
menu_script = next(script.string for script in soup.find_all('script') if script.string and 'self.__next_f.push' in script.string and 'itemLists' in script.string)
embedded_str = re.search(r'self\.__next_f\.push\(\[1,"(.*?)"\]\)', menu_script, re.DOTALL).group(1).encode('utf-8').decode('unicode_escape')
start_idx = embedded_str.find('"itemLists":')
array_start = embedded_str.find('[', start_idx)
bracket_count = 0
for i in range(array_start, len(embedded_str)):
    if embedded_str[i] == '[':
        bracket_count += 1
    elif embedded_str[i] == ']':
        bracket_count -= 1
        if bracket_count == 0:
            array_end = i + 1
            break
itemlists_json = embedded_str[array_start:array_end].replace('\\u0026', '&')
itemlists = json.loads(itemlists_json)

all_items = []
for category in itemlists:
    for item in category.get('items', []):
        name = item.get('name')
        desc = item.get('description', '').strip() or None
        price = item.get('displayPrice')
        img = item.get('imageUrl')
        rating = review_count = None
        rds = item.get('ratingDisplayString')
        if rds:
            m2 = re.match(r'(\d+)%\s*\((\d+)\)', rds)
            if m2:
                rating = int(m2.group(1))
                review_count = int(m2.group(2))
        all_items.append({
            'name': name,
            'description': desc,
            'price': price,
            'rating_%': rating,
            'review_count': review_count,
            'image_url': img
        })

with open('menu_items.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile,
        fieldnames=['name','description','price','rating_%','review_count','image_url'])
    writer.writeheader()
    writer.writerows(all_items)

print(f"Extracted {len(all_items)} items to menu_items.csv")