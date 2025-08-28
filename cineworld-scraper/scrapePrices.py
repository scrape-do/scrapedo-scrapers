import json
import csv
import urllib.parse
import requests
import secrets

# Scrape.do API token
TOKEN = "<your-token>"
cinema_id = "074"
cart_id = "RWEB" + secrets.token_hex(8)

# Load screenings from JSON file
with open("screenings.json", "r", encoding="utf-8") as f:
    sessions = json.load(f)
print(f"Loaded {len(sessions)} sessions from screenings.json")

# Get ticket prices for each session
all_tickets = []
for s in sessions:
    session_id = s["id"]
    date_str = s["Date"]

    target_url = (
        "https://experience.cineworld.co.uk/api/GetTicketsForSession"
        f"?theatreCode={cinema_id}"
        f"&vistaSession={session_id}"
        f"&date={date_str}"
        f"&cartId={cart_id}"
        "&sessionToken=false"
    )
    encoded = urllib.parse.quote_plus(target_url)
    api_url = f"https://api.scrape.do/?token={TOKEN}&url={encoded}&geoCode=gb&super=true"

    r = requests.get(api_url)
    try:
        data = json.loads(r.text)
    except json.JSONDecodeError:
        print(f"Invalid JSON for session {session_id}")
        continue

    # Extract ticket information
    for t in data.get("Tickets", []):
        # Convert price from cents to pounds
        price_in_cents = t.get("PriceInCents")
        try:
            price = f"£{int(price_in_cents) / 100:.2f}"
        except Exception:
            price = None
            
        all_tickets.append({
            "Movie Name": s["Movie Name"],
            "Date": s["Date"],
            "Cinema": s["Cinema"],
            "Time": s["Time"],
            "TicketTypeCode": t.get("TicketTypeCode"),
            "LongDescription": t.get("LongDescription"),
            "Price": price
        })

print(f"Collected {len(all_tickets)} ticket rows")

# Save to CSV file
with open("ticket_prices.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=[
            "Movie Name", "Date", "Cinema", "Time",
            "TicketTypeCode", "LongDescription", "Price"
        ]
    )
    writer.writeheader()
    writer.writerows(all_tickets)

print(f"Wrote {len(all_tickets)} rows to ticket_prices.csv")