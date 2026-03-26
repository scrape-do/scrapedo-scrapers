import requests
import urllib.parse
import json
from bs4 import BeautifulSoup

token = "<your_token>"
query = "python web scraping"

encoded_query = urllib.parse.quote_plus(query)
google_url = f"https://www.google.com/search?q={encoded_query}&hl=en&gl=us"
api_url = f"http://api.scrape.do/?token={token}&url={urllib.parse.quote(google_url, safe='')}&super=true"

response = requests.get(api_url, timeout=60)

if response.status_code != 200:
    print(f"Request failed: {response.status_code}")
    exit()

soup = BeautifulSoup(response.text, "html.parser")
faq_results = soup.find_all("div", jsname="yEVEwb")

questions = []
for position, faq in enumerate(faq_results, 1):
    question_elem = faq.find("span")
    if question_elem:
        questions.append({
            "position": position,
            "question": question_elem.get_text(strip=True),
        })

with open("faq-results.json", "w", encoding="utf-8") as f:
    json.dump(questions, f, indent=2, ensure_ascii=False)

for q in questions:
    print(f"{q['position']}. {q['question']}")

print(f"\nFound {len(questions)} FAQ questions. Saved to faq-results.json")
