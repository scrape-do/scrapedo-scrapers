import requests
import csv
import urllib.parse
import json
from bs4 import BeautifulSoup

# Configuration
token = "<your-token>"
query = "coffee"
max_results = 100

all_images = []
first = 1

print(f"Starting image scrape for: '{query}'")
print(f"Target: {max_results} images\n")

while len(all_images) < max_results:
    # Build URL
    page_url = f"https://www.bing.com/images/async?q={query}&first={first}&mmasync=1"
    encoded_url = urllib.parse.quote(page_url, safe='')
    api_url = f"http://api.scrape.do?token={token}&url={encoded_url}&geoCode=us"
    
    print(f"Fetching images (first={first})...", end=" ")
    
    # Send request
    response = requests.get(api_url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Extract images from this page
    page_images = []
    
    for img_link in soup.find_all("a"):
        m_data = img_link.get("m", "")
        
        try:
            data = json.loads(m_data)
            
            page_images.append({
                "title": data.get("t", ""),
                "image_url": data.get("murl", ""),
                "source_url": data.get("purl", ""),
                "thumbnail_url": data.get("turl", "")
            })
        except:
            continue
    
    # Stop if no images found
    if not page_images:
        print("No more images found")
        break
    
    all_images.extend(page_images)
    print(f"Found {len(page_images)} images (total: {len(all_images)})")
    
    # Next page
    first += len(page_images)

# Trim to max_results
all_images = all_images[:max_results]

# Save to CSV
print(f"\nSaving {len(all_images)} images to CSV...")
with open("bing_image_results.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["title", "image_url", "source_url", "thumbnail_url"])
    writer.writeheader()
    writer.writerows(all_images)

print(f"Done! Extracted {len(all_images)} images -> bing_image_results.csv")

# ===== DOWNLOAD IMAGES SECTION (Comment/Uncomment this entire block) =====
# import os
# download_folder = "downloaded_images"
# 
# # Create download folder
# if not os.path.exists(download_folder):
#     os.makedirs(download_folder)
# 
# # Download all images
# print(f"\nDownloading {len(all_images)} images...")
# for idx, img in enumerate(all_images):
#     try:
#         img_url = img["image_url"]
#         img_response = requests.get(img_url, timeout=10)
#         
#         # Get file extension from URL
#         ext = img_url.split(".")[-1].split("?")[0]
#         if ext not in ["jpg", "jpeg", "png", "gif", "webp"]:
#             ext = "jpg"
#         
#         # Save image
#         filename = f"{download_folder}/{query}_{idx + 1}.{ext}"
#         with open(filename, "wb") as f:
#             f.write(img_response.content)
#         
#         if (idx + 1) % 10 == 0:
#             print(f"Downloaded {idx + 1}/{len(all_images)} images...")
#     except:
#         continue
# 
# print(f"Download complete! Images saved to {download_folder}/")
# ===== END DOWNLOAD SECTION =====
