import urllib.parse
import requests
import json
from datetime import datetime, timedelta

# Scrape.do API token
TOKEN = "<your-token>"
cinema_id = "0147"
cinema_name = "Regal Village Park"
start_date = "10-07-2025"
end_date = "10-09-2025"

# Generate date range
start = datetime.strptime(start_date, "%m-%d-%Y")
end = datetime.strptime(end_date, "%m-%d-%Y")
delta = end - start
dates = [(start + timedelta(days=i)).strftime("%m-%d-%Y") for i in range(delta.days + 1)]

screening_list = []

for date in dates:
    print(f"Scraping screenings from {date}")
    listing_url = f"https://www.regmovies.com/api/getShowtimes?theatres={cinema_id}&date={date}&hoCode=&ignoreCache=false&moviesOnly=false"
    encoded_listing_url = urllib.parse.quote_plus(listing_url)
    listing_api_url = f"https://api.scrape.do/?token={TOKEN}&url={encoded_listing_url}&geoCode=us&super=true&render=true"

    listings_response = requests.get(listing_api_url)
    listings_json = json.loads(listings_response.text.split("<pre>")[1].split("</pre>")[0])

    shows = listings_json.get("shows")
    if len(shows):
        movies = shows[0].get("Film", [])

        for movie in movies:
            movie_name = movie.get('Title')
            performances = movie.get('Performances', [])
            for performance in performances:
                vista_id = performance.get('PerformanceId')
                show_time = performance.get('CalendarShowTime').split("T")[1]
                screening_list.append({
                    "Movie Name": movie_name,
                    "Date": date,
                    "Cinema": cinema_name,
                    "Time": show_time,
                    "id": vista_id
                })

# Save to JSON file
with open("screenings.json", "w", encoding="utf-8") as f:
    json.dump(screening_list, f, ensure_ascii=False, indent=4)

print(f"Extracted {len(screening_list)} screenings from {len(dates)} days")
