import requests
import urllib.parse

# Your Scrape.do API token
token = "<your-token>"

# The Instagram username we want to scrape
username = "bkbagelny"

# Construct the Instagram API URL for fetching profile information
profile_url = f"https://www.instagram.com/api/v1/users/web_profile_info/?username={username}"

# Encode the URL so it can be safely passed as a parameter
encoded_url = urllib.parse.quote_plus(profile_url)

# Construct the Scrape.do request URL to avoid blocks and login restrictions
api_url = f"https://api.scrape.do/?token={token}&url={encoded_url}"

# Send the request through Scrape.do
response = requests.get(api_url)

# Parse the JSON response
data = response.json()

# Extract posts data
posts = data["data"]["user"]["edge_owner_to_timeline_media"]["edges"]

# Display all posts found
print("\n=== Extracted Posts ===")

for i, post in enumerate(posts, 1):
    post_data = post["node"]

    # Get the text of the first caption edge if it exists
    caption = post_data["edge_media_to_caption"]["edges"][0]["node"]["text"] \
              if post_data["edge_media_to_caption"]["edges"] else "No caption"

    # This is the unique piece of the link you can use:
    # instagram.com/p/<shortcode> or instagram.com/reel/<shortcode>
    shortcode = post_data.get("shortcode", "N/A")

    print(f"\nPost #{i}")
    print("Shortcode (for link):", shortcode)
    print("Caption:", caption)
    print("Media URL:", post_data["display_url"])
    print("Likes:", post_data["edge_liked_by"]["count"])
    print("Comments:", post_data["edge_media_to_comment"]["count"])
