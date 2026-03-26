import json
import urllib.parse
import requests
from bs4 import BeautifulSoup
import time

TOKEN = "<your_token>"
AUTHOR_URL = "https://scholar.google.com/citations?user=qNuSIPAAAAAJ"

# Scholar needs super=true for bot protection. No render needed:
# the profile data is all in the initial server-side HTML.
api_url = f"http://api.scrape.do/?token={TOKEN}&url={urllib.parse.quote(AUTHOR_URL)}&super=true"
response = requests.get(api_url, timeout=60)
soup = BeautifulSoup(response.text, "html.parser")

# The author's name, affiliation, and email verification are all neatly
# organized in the profile header section.
name = soup.find("div", id="gsc_prf_in")
name = name.get_text(strip=True) if name else None

affiliation_elem = soup.find("div", class_="gsc_prf_il")
affiliation = affiliation_elem.get_text(strip=True) if affiliation_elem else None

email_elem = soup.find("div", id="gsc_prf_ivh")
verified_email = email_elem.get_text(strip=True) if email_elem else None

# The stats table has three rows (Citations, h-index, i10-index) with
# columns for "All" and "Since 2020". We're focused on the citation numbers.
total_citations = None
citations_since_2020 = None
citation_table = soup.find("table", id="gsc_rsb_st")

if citation_table:
    for row in citation_table.find_all("tr"):
        cells = row.find_all("td")
        if len(cells) >= 3 and "Citations" in cells[0].get_text():
            total_citations = cells[1].get_text(strip=True)
            citations_since_2020 = cells[2].get_text(strip=True)

print(f"Name: {name}")
print(f"Affiliation: {affiliation}")
print(f"Verified Email: {verified_email}")
print(f"Total Citations: {total_citations}")
print(f"Citations Since 2020: {citations_since_2020}")

# Google Scholar's author page loads 20 articles by default, with a "Show More"
# button that triggers AJAX calls. Instead of simulating clicks, we'll use the
# cstart and pagesize URL parameters to paginate server-side. We request 100
# articles per page and keep going until there are no more rows to collect.
all_articles = []
PAGE_SIZE = 100
start = 0

while True:
    print(f"\nFetching articles starting from index {start}...")
    page_url = f"{AUTHOR_URL}&cstart={start}&pagesize={PAGE_SIZE}"
    api_url = f"http://api.scrape.do/?token={TOKEN}&url={urllib.parse.quote(page_url)}&super=true"
    response = requests.get(api_url, timeout=60)
    page_soup = BeautifulSoup(response.text, "html.parser")

    # Each article sits in a table row with class gsc_a_tr.
    article_rows = page_soup.find_all("tr", class_="gsc_a_tr")
    if not article_rows:
        break

    for row in article_rows:
        title_elem = row.find("a", class_="gsc_a_at")
        if not title_elem:
            continue

        title = title_elem.get_text(strip=True)
        href = title_elem.get("href", "")
        article_link = f"https://scholar.google.com{href}" if href else None

        # The gray-text divs hold authors (first) and journal/venue (second).
        gray_divs = row.find_all("div", class_="gs_gray")
        authors = gray_divs[0].get_text(strip=True) if len(gray_divs) > 0 else None
        journal = gray_divs[1].get_text(strip=True) if len(gray_divs) > 1 else None

        citations_elem = row.find("a", class_="gsc_a_ac")
        year_elem = row.find("span", class_="gsc_a_h")

        all_articles.append({
            "title": title,
            "authors": authors,
            "journal": journal,
            "citations": citations_elem.get_text(strip=True) if citations_elem else "0",
            "year": year_elem.get_text(strip=True) if year_elem else None,
            "link": article_link,
        })

    print(f"  Collected {len(article_rows)} articles from this page.")

    if len(article_rows) < PAGE_SIZE:
        break

    start += PAGE_SIZE
    time.sleep(1)

# An article is "available" if it has a valid Scholar link pointing to its
# detail page. Articles without links are citation-only entries.
available = sum(1 for a in all_articles if a["link"])
unavailable = len(all_articles) - available

print(f"\nTotal Articles: {len(all_articles)}")
print(f"Available (with detail link): {available}")
print(f"Unavailable (citation-only): {unavailable}")

for i, article in enumerate(all_articles, 1):
    print(f"\n--- Article {i} ---")
    print(f"Title: {article['title']}")
    print(f"Authors: {article['authors']}")
    print(f"Journal: {article['journal']}")
    print(f"Citations: {article['citations']}")
    print(f"Year: {article['year']}")
    print(f"Link: {article['link']}")

with open("scholar_author_articles.json", "w", encoding="utf-8") as f:
    json.dump(all_articles, f, indent=2, ensure_ascii=False)

print(f"\nSaved {len(all_articles)} articles to scholar_author_articles.json")
