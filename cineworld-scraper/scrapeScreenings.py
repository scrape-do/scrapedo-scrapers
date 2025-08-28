import requests
import urllib.parse
import time
import re
import json
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

# Scrape.do API token
TOKEN = "<your-token>"
cinema_name = "aberdeen-union-square"
cinema_id = "074"
start_date = "2025-09-04"
end_date = "2025-09-08"

# Generate date range
s = datetime.strptime(start_date, "%Y-%m-%d")
e = datetime.strptime(end_date, "%Y-%m-%d")
dates = [(s + timedelta(days=i)).strftime("%Y-%m-%d") for i in range((e - s).days + 1)]

# Today for comparison
today_str = datetime.now().strftime("%Y-%m-%d")

screening_list = []

for current_date in dates:
    listing_url = (
        f"https://www.cineworld.co.uk/cinemas/{cinema_name}/{cinema_id}"
        f"#/buy-tickets-by-cinema?in-cinema={cinema_id}&at={current_date}&view-mode=list"
    )
    encoded = urllib.parse.quote_plus(listing_url)
    api_url = (
        f"https://api.scrape.do/?token={TOKEN}&url={encoded}"
        f"&geoCode=gb&super=true&render=true"
    )

    html = None
    attempt = 0
    max_retries = 2
    
    # Retry logic for failed requests
    while attempt <= max_retries:
        attempt += 1
        r = requests.get(api_url)
        soup = BeautifulSoup(r.text, "html.parser")

        # Check if listings exist
        movie_rows = soup.select(".movie-row")
        if movie_rows:
            html = r.text
            break

        print(f"No listings for {current_date} on attempt {attempt}, retrying...")
        time.sleep(2)

    if not html:
        continue

    # Parse HTML for this date
    soup = BeautifulSoup(html, "html.parser")

    # Check calendar widget to verify correct date
    cal = soup.select_one(".qb-calendar-widget h5")
    if cal:
        calendar_text = cal.get_text(" ", strip=True)
        m = re.search(r'(\d{2})/(\d{2})/(\d{4})', calendar_text)
        if m:
            dd, mm, yyyy = m.groups()
            returned_date = f"{yyyy}-{mm}-{dd}"
            # Skip if wrong date returned
            if returned_date == today_str and current_date != today_str:
                print(f"Defaulted to today, no shows for {current_date}")
                continue
            if returned_date and returned_date != current_date:
                print(f"Got {returned_date} instead of {current_date}, skipping")
                continue

    seen = set()

    # Extract movie rows
    for row in soup.select(".movie-row"):
        title_el = row.select_one("h3.qb-movie-name")
        movie_name = title_el.get_text(strip=True) if title_el else ""

        # Find screening buttons
        for btn in row.select("a.btn-lg"):
            href_val = btn.get("href", "")
            if href_val == "#" and btn.has_attr("data-url"):
                data_url = btn["data-url"]
                
                # Extract vista ID from data-url
                parsed = urllib.parse.urlparse(data_url)
                qs = urllib.parse.parse_qs(parsed.query)
                vista = qs.get("id", [None])[0]
                if not vista:
                    # Fallback regex
                    m = re.search(r'(?:\?|&)id=([^&]+)', data_url)
                    vista = m.group(1) if m else None
                
                if not vista:
                    continue
                    
                key = (vista, current_date)
                if key in seen:
                    continue
                seen.add(key)
                
                screening_list.append({
                    "Movie Name": movie_name,
                    "Date": current_date,
                    "Cinema": cinema_name,
                    "Time": btn.get_text(strip=True),
                    "id": vista
                })

# Save to JSON file
with open("screenings.json", "w", encoding="utf-8") as f:
    json.dump(screening_list, f, ensure_ascii=False, indent=2)

print(f"Saved {len(screening_list)} screenings to screenings.json")