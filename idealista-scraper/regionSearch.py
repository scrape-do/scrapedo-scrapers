from bs4 import BeautifulSoup
import requests
import urllib.parse
import csv

# Our token provided by Scrape.do
token = "<your_token>"

# Target Idealista search URL
base_url = "<target_search_url>"  # Example: https://www.idealista.com/venta-viviendas/santa-cruz-de-tenerife/la-palma/con-chalets/

# Optional parameters
render = "true"
geo_code = "es"
super_mode = "true"

# Initialize data storage
all_properties = []
page = 1

while True:
    # Construct URL for current page
    if page == 1:
        current_url = base_url
    else:
        current_url = base_url + f"pagina-{page}.htm"
    
    print(f"Scraping page {page}...")
    
    # Scrape.do API endpoint
    url = f"https://api.scrape.do/?token={token}&url={urllib.parse.quote_plus(current_url)}&geoCode={geo_code}&render={render}&super={super_mode}"
    
    # Send the request
    response = requests.request("GET", url)
    
    # Parse the response using BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Find all property listings
    listings = soup.find_all("article", class_="item")
    
    # If no listings found, we've reached the end
    if not listings:
        print(f"No more listings found on page {page}. Stopping.")
        break
    
    for listing in listings:
        # Extract property price
        price_element = listing.find("span", class_="item-price")
        price = price_element.text.strip() if price_element else ""
        
        # Extract property title and parse type + location
        title_element = listing.find("a", class_="item-link")
        if title_element:
            title = title_element.text.strip()
            title_parts = title.split(" en ")
            property_type = title_parts[0].strip()
            location = title_parts[1].strip() if len(title_parts) > 1 else ""
            
            # Extract listing URL
            listing_url = "https://www.idealista.com" + title_element.get("href", "")
        else:
            title = property_type = location = listing_url = ""
        
        # Extract bedroom count and square meters
        details = listing.find_all("span", class_="item-detail")
        bedroom_count = ""
        square_meters = ""
        
        for detail in details:
            text = detail.text.strip()
            if "hab." in text:
                bedroom_count = text
            elif "m²" in text:
                square_meters = text
        
        # Store property data
        all_properties.append({
            "Price": price,
            "Property Type": property_type,
            "Location": location,
            "Bedrooms": bedroom_count,
            "Square Meters": square_meters,
            "URL": listing_url
        })
    
    print(f"Found {len(listings)} listings on page {page}")
    page += 1

# Save extracted data to CSV
with open("idealista_properties.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=["Price", "Property Type", "Location", "Bedrooms", "Square Meters", "URL"])
    writer.writeheader()
    writer.writerows(all_properties)

print(f"\nScraping complete! Found {len(all_properties)} total properties.")
print("Data saved to idealista_properties.csv")