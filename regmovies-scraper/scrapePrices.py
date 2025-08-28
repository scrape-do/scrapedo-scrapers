import urllib.parse
import requests
import json
import csv

# Scrape.do API token
TOKEN = "<your-token>"
cinema_id = "0147"

# Load screenings from JSON file
with open("screenings.json", "r", encoding="utf-8") as f:
    screening_list = json.load(f)

all_tickets = []

for i, session in enumerate(screening_list, 1):
    print(f"Processing {i}/{len(screening_list)}: {session['Movie Name']}")

    # Create order session
    order_url = f"https://www.regmovies.com/api/createOrder"
    encoded_order_url = urllib.parse.quote_plus(order_url)
    order_api_url = f"https://api.scrape.do/?token={TOKEN}&url={encoded_order_url}&geoCode=us&super=true"
    order_response = requests.post(order_api_url, json={"cinemaId": "0147"})

    cart_id = json.loads(order_response.text).get("order").get("userSessionId")
    session_id = session["id"]

    # Get ticket prices for this session
    tickets_url = f"https://www.regmovies.com/api/getTicketsForSession?theatreCode={cinema_id}&vistaSession={session_id}&cartId={cart_id}&sessionToken=false"
    encoded_tickets_url = urllib.parse.quote_plus(tickets_url)
    tickets_api_url = f"https://api.scrape.do/?token={TOKEN}&url={encoded_tickets_url}&geoCode=us&super=true"
    tickets_response = requests.get(tickets_api_url)

    try:
        data = json.loads(tickets_response.text)
    except json.JSONDecodeError:
        print(f"Invalid JSON for session {session_id}")
        continue

    # Extract ticket information
    tickets = data.get("Tickets", [])
    for ticket in tickets:
        # Convert price from cents to USD
        price_in_cents = ticket.get("PriceInCents")
        try:
            price = f"${int(price_in_cents) / 100:.2f}"
        except (ValueError, TypeError):
            price = None
            
        all_tickets.append({
            "Movie Name": session["Movie Name"],
            "Date": session["Date"],
            "Cinema": session["Cinema"],
            "Time": session["Time"],
            "TicketTypeCode": ticket.get("TicketTypeCode"),
            "LongDescription": ticket.get("LongDescription"),
            "Price": price
        })

# Save to CSV file
with open("ticket_prices.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=["Movie Name", "Date", "Cinema", "Time", "TicketTypeCode", "LongDescription", "Price"])
    writer.writeheader()
    writer.writerows(all_tickets)

print(f"Saved {len(all_tickets)} ticket entries to ticket_prices.csv")
