import requests
import urllib.parse
import json
from datetime import datetime

# Define variables
doc_id = "8845758582119845"  # GraphQL query ID for fetching post comments
shortcode = "DG8BLeyR8Hc"  # Replace with the target post’s shortcode
token = "<your-token>"

# Construct Instagram query URL
variables_str = f'{{"shortcode":"{shortcode}"}}'
encoded_vars = urllib.parse.quote_plus(variables_str)
instagram_url = f"https://www.instagram.com/graphql/query?doc_id={doc_id}&variables={encoded_vars}"

# Construct Scrape.do API request
encoded_instagram_url = urllib.parse.quote_plus(instagram_url)
api_url = f"https://api.scrape.do/?token={token}&url={encoded_instagram_url}"

# Send the GET request
response = requests.get(api_url)
data = response.json()
post_data = data["data"]["xdt_shortcode_media"]

# Extract comments
comment_edges = post_data["edge_media_to_parent_comment"]["edges"]

for edge in comment_edges:
    node = edge["node"]
    comment_id = node["id"]
    comment_text = node["text"]
    created_at = datetime.fromtimestamp(node["created_at"]).strftime("%Y-%m-%d %H:%M:%S")
    owner_username = node["owner"]["username"]
    like_count = node["edge_liked_by"]["count"]

    print("Comment ID:", comment_id)
    print("Text:", comment_text)
    print("Created At:", created_at)
    print("Owner Username:", owner_username)
    print("Likes:", like_count)

    # Check for replies
    if "edge_threaded_comments" in node and node["edge_threaded_comments"]["edges"]:
        for reply_edge in node["edge_threaded_comments"]["edges"]:
            reply_node = reply_edge["node"]
            reply_id = reply_node["id"]
            reply_text = reply_node["text"]
            reply_created_at = datetime.fromtimestamp(reply_node["created_at"]).strftime("%Y-%m-%d %H:%M:%S")
            reply_owner_username = reply_node["owner"]["username"]
            reply_like_count = reply_node["edge_liked_by"]["count"]

            # Print reply details
            print("   └ Reply ID:", reply_id)
            print("   └ Text:", reply_text)
            print("   └ Created At:", reply_created_at)
            print("   └ Owner Username:", reply_owner_username)
            print("   └ Likes:", reply_like_count)
            print("   ──────────")  # Small separator after each reply

    print("-" * 40)  # Separator for readability
