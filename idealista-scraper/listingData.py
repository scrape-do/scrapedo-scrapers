from bs4 import BeautifulSoup
import requests
import urllib.parse
import re

# Our token provided by Scrape.do
token = "<your_token>"

# Target Idealista listing URL
target_url = urllib.parse.quote_plus("<target_property_url>")  # Example: https://www.idealista.com/inmueble/107795847/

# Optional parameters
render = "true"
geo_code = "es"
super_mode = "true"

# Scrape.do API endpoint
url = f"https://api.scrape.do/?token={token}&url={target_url}&geoCode={geo_code}&render={render}&super={super_mode}"

# Send the request
response = requests.request("GET", url)

# Parse the response using BeautifulSoup
soup = BeautifulSoup(response.text, "html.parser")

# Extract property title
title = soup.find("span", class_="main-info__title-main").text.strip()

# Extract location and split into neighborhood and city
location = soup.find("span", class_="main-info__title-minor").text.strip()
neighborhood, city = location.split(", ")

# Extract property price
price = soup.find("span", class_="info-data-price").text.strip()

# Extract square size and bedroom count from info-features
info_features = soup.find("div", class_="info-features")
feature_spans = info_features.find_all("span", recursive=False)
square_size = feature_spans[0].text.strip() if len(feature_spans) > 0 else ""
bedroom_count = feature_spans[1].text.strip() if len(feature_spans) > 1 else ""

# Extract full address from location section
ubicacion_h2 = soup.find("h2", class_="ide-box-detail-h2", string="Ubicación")
if ubicacion_h2:
    ul_element = ubicacion_h2.find_next("ul")
    if ul_element:
        address_parts = []
        for li in ul_element.find_all("li", class_="header-map-list"):
            address_parts.append(li.text.strip())
        full_address = ", ".join(address_parts)
    else:
        full_address = ""
else:
    full_address = ""

# Extract last updated days
date_update_text = soup.find("p", class_="date-update-text")
if date_update_text:
    update_text = date_update_text.text.strip()
    days_match = re.search(r'hace (\d+) días?', update_text)
    last_updated_days = days_match.group(1) if days_match else ""
else:
    last_updated_days = ""

# Extract advertiser name
advertiser_name_element = soup.find("a", class_="about-advertiser-name")
advertiser_name = advertiser_name_element.text.strip() if advertiser_name_element else ""

# Parse property title to extract type and for status
title_parts = title.split(" en ")
property_type = title_parts[0].strip()
for_status = "en " + title_parts[1].strip() if len(title_parts) > 1 else ""

# Print extracted data
print("Property Type:", property_type)
print("For:", for_status)
print("Square Size:", square_size)
print("Bedroom Count:", bedroom_count)
print("Neighborhood:", neighborhood)
print("City:", city)
print("Full Address:", full_address)
print("Last Updated Days:", last_updated_days)
print("Advertiser Name:", advertiser_name)
print("Price:", price)