import requests
import re
import json

# Our token provided by Scrape.do
token = "<your_token>"

# Target Ticketmaster URL
target_url = "<target_artist_url>"  # Example: https://www.ticketmaster.com/post-malone-tickets/artist/2119390

# Optional parameters
render = "false"
geo_code = "us"
super_mode = "true"

# Scrape.do API endpoint
url = f"https://api.scrape.do/?token={token}&url={target_url}&render={render}&geoCode={geo_code}&super={super_mode}"

# Send the request
response = requests.get(url)

# Extract JSON data using regex
match = re.search(r'<script type="application/ld\+json">(.*?)</script>', response.text, re.DOTALL)
json_data = json.loads(match.group(1) if match else "[]")

# Loop through all events and extract details
for event in json_data:
    print(f"Event: {event['name']}")
    print(f"Date: {event['startDate']}")
    print(f"Venue: {event['location']['name']}")
    print(f"Location: {event['location']['address']['addressLocality']}, {event['location']['address']['addressRegion']}\n")