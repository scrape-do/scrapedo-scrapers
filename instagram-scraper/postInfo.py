import requests
import urllib.parse
import json
from datetime import datetime

# Required parameters
doc_id = "8845758582119845"  # GraphQL query ID for fetching post details
shortcode = "DG8BLeyR8Hc"  # Replace with the target post’s shortcode
token = "<your-token>"

# Construct GraphQL variables string
variables_str = f'{{"shortcode":"{shortcode}"}}'
encoded_vars = urllib.parse.quote_plus(variables_str)

# Instagram GraphQL API URL
instagram_url = f"https://www.instagram.com/graphql/query?doc_id={doc_id}&variables={encoded_vars}"

# Encode the URL for Scrape.do
encoded_instagram_url = urllib.parse.quote_plus(instagram_url)
api_url = f"https://api.scrape.do/?token={token}&url={encoded_instagram_url}"

# Send the request through Scrape.do
response = requests.get(api_url)
data = response.json()

# Extract post data
post_data = data["data"]["xdt_shortcode_media"]

post_id = post_data["id"]
shortcode = post_data["shortcode"]
account_name = post_data["owner"]["username"]
like_count = post_data["edge_media_preview_like"]["count"]
comment_count = post_data["edge_media_to_parent_comment"]["count"]
is_video = post_data["is_video"]
video_url = post_data.get("video_url", "N/A") if is_video else "N/A"

# Extract caption
caption_edges = post_data["edge_media_to_caption"]["edges"]
caption_text = caption_edges[0]["node"]["text"] if caption_edges else ""

# Extract location (if available)
location = post_data["location"]["name"] if post_data.get("location") else "N/A"

# Convert timestamp to readable format
published_time = datetime.fromtimestamp(post_data["taken_at_timestamp"]).strftime("%Y-%m-%d %H:%M:%S")

# Display post details
print("=== Post Details ===")
print("Post ID:", post_id)
print("Shortcode:", shortcode)
print("Account Name:", account_name)
print("Like Count:", like_count)
print("Comment Count:", comment_count)
print("Caption:", caption_text)
print("Location:", location)
print("Published Time:", published_time)
print("Is Video:", is_video)
print("Video URL:", video_url)
