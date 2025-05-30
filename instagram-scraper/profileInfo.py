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

# Extract user data from the JSON response
user_data = data["data"]["user"]

# Print detailed Instagram profile information
print("=== Detailed Instagram Profile Information ===")
print("Username:", user_data["username"])  # The Instagram handle of the user
print("Full Name:", user_data["full_name"])  # The full name of the user
print("Biography:", user_data["biography"])  # The bio text from the profile

# Extract biography with any embedded entities (e.g., mentions, hashtags)
print("Biography with Entities:", user_data["biography_with_entities"]["raw_text"])

# External URL (e.g., website link in profile)
print("External URL:", user_data["external_url"])

# High-resolution profile picture URL
print("Profile Picture URL:", user_data["profile_pic_url_hd"])

# Business-related information
print("Business Category:", user_data["business_category_name"])  # Business category if applicable
print("Category Name:", user_data["category_name"])  # General category associated with the profile
print("Is Business Account:", user_data["is_business_account"])  # Boolean flag for business accounts

# Privacy and verification status
print("Is Private:", user_data["is_private"])  # Boolean flag for private accounts
print("Is Verified:", user_data["is_verified"])  # Boolean flag for verified accounts

# Engagement statistics
print("Follower Count:", user_data["edge_followed_by"]["count"])  # Number of followers
print("Following Count:", user_data["edge_follow"]["count"])  # Number of people the account follows
print("Total Posts Count:", user_data["edge_owner_to_timeline_media"]["count"])  # Total number of posts
