import requests
import urllib.parse
from bs4 import BeautifulSoup
import csv

# Configuration
TOKEN = "<your_token>"
target_urls = [
    "https://www.redfin.com/TX/Austin/7646-Elkhorn-Mountain-Trl-78729/home/32851263",
    "https://www.redfin.com/TX/Austin/6000-Shepherd-Mountain-Cv-78730/unit-2103/home/31123552",
    "https://www.redfin.com/NY/Queens/34-24-82nd-St-11372/unit-2/home/175087110"
]

all_properties = []

for target_url in target_urls:
    # Fetch page
    response = requests.get(f"https://api.scrape.do/?token={TOKEN}&url={urllib.parse.quote(target_url)}")
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Extract data
    property_data = {}
    
    # Basic info
    address_header = soup.find("h1", class_="full-address addressBannerRevamp street-address").get_text(strip=True)
    property_data['full_address'] = address_header
    property_data['price'] = soup.find("div", class_="statsValue price").get_text(strip=True)
    property_data['property_id'] = target_url.split('/home/')[1]
    
    # Address parsing
    address_parts = address_header.split(',')
    property_data['city'] = address_parts[1]
    state_zip = address_parts[2].split(' ')
    property_data['state'] = state_zip[1]
    property_data['zip_code'] = state_zip[2]
    
    # Property type
    key_details_rows = soup.find_all("div", class_="keyDetails-row")
    property_data['property_type'] = "Unknown"
    for row in key_details_rows:
        if "Property Type" in row.find("span", class_="valueType").get_text():
            property_data['property_type'] = row.find("span", class_="valueText").get_text(strip=True)
            break
    
    # Square feet
    property_data['square_feet'] = soup.find("span", class_="statsValue").get_text(strip=True) + " sq ft"
    
    # Image
    property_data['main_image_link'] = soup.find("img").get("src")
    
    # Agent info - COMMENTED OUT: Scraping personal info may be illegal and unethical
    # agent_content = soup.find("div", class_="agent-info-content")
    # property_data['listed_by'] = agent_content.find("span", class_="agent-basic-details--heading").find("span").get_text(strip=True)
    # broker_text = agent_content.find("span", class_="agent-basic-details--broker").get_text(strip=True)
    # property_data['broker'] = broker_text.replace('•', '').strip()
    # 
    # # Contact
    # contact_text = soup.find("div", class_="listingContactSection").get_text(strip=True)
    # property_data['contact_number'] = contact_text.split(':')[1]
    
    # Set empty values for personal information fields
    property_data['listed_by'] = ""
    property_data['broker'] = ""
    property_data['contact_number'] = ""
    
    # Last updated
    property_data['listing_last_updated'] = soup.find("div", class_="listingInfoSection").find("time").get_text(strip=True)
    
    all_properties.append(property_data)

# Save CSV
with open("redfin_property_details.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=all_properties[0].keys())
    writer.writeheader()
    writer.writerows(all_properties)

print(f"✓ {len(all_properties)} properties saved to redfin_property_details.csv")