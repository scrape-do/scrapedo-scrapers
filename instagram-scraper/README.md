# Instagram Profile & Post Scraper

[Step-by-step guide to scraping Instagram ➡](https://scrape.do/blog/instagram-scraping/)

This repository provides Python scripts to scrape public Instagram profile details, recent posts, and top-level post comments using [Scrape.do](https://scrape.do) web scraping API to bypass blocks and restrictions from anti-bots.

All data is collected from publicly accessible endpoints. No login or session cookies required.

## What’s Included

* `profileInfo.py`: Scrapes profile information including bio, follower count, and category.
* `profileTopPosts.py`: Extracts metadata for the 12 most recent public posts from a profile.
* `postInfo.py`: Retrieves engagement metrics, caption, location, and video URL for a specific post.
* `postComments.py`: Scrapes top-level comments and threaded replies from a public post.

## Requirements

* Python 3.7+
* `requests` library<br> Install with:

  ```bash
  pip install requests
  ```
* A [Scrape.do API token](https://dashboard.scrape.do/signup) (**free** 1000 successful requests/month)
* (Free 1000 successful requests/month)

## 🔍 How to Use Each Script

### `profileInfo.py`

**Scrapes a public Instagram profile’s metadata (bio, followers, categories, etc.).**

1. Replace the username and token:

   ```python
   token = "<your-token>"
   username = "bkbagelny"
   ```
2. Run:

   ```bash
   python profileInfo.py
   ```

Outputs detailed profile data including follower count, bio, and business categories.

### `profileTopPosts.py`

**Extracts recent post metadata (shortcode, caption, likes, media URL) from a user’s profile.**

1. Replace the username and token:

   ```python
   token = "<your-token>"
   username = "bkbagelny"
   ```
2. Run:

   ```bash
   python profileInfo.py
   ```

Returns details of up to 12 top and recent public posts.

### `postInfo.py`

**Fetches full metadata for a specific post (caption, likes, video, location, timestamp).**

1. Find the `shortcode` from a post URL or from `profileTopPosts.py`:

   ```css
   https://www.instagram.com/p/DG8BLeyR8Hc/ → shortcode: DG8BLeyR8Hc
   ```
2. Replace in the script:

   ```python
   shortcode = "DG8BLeyR8Hc"
   token = "<your-token>"
   ```
3. Run:

   ```bash
   python postInfo.py
   ```

Returns complete post details including caption, likes, location, and whether it’s a video.

### `postComments.py`

**Scrapes top-level comments and replies on a specific post.**

1. Find the `shortcode` from a post URL or from `profileTopPosts.py`:

   ```css
   https://www.instagram.com/p/DG8BLeyR8Hc/ → shortcode: DG8BLeyR8Hc
   ```
2. Replace in the script:

   ```python
   shortcode = "DG8BLeyR8Hc"
   token = "<your-token>"
   ```
3. Run:

   ```bash
   python postComments.py
   ```

Returns a nested comment thread structure with timestamps and like counts.

## ⚠️ Legal & Ethical Notes

*To stay on the good side of the law and ethics while scraping:*

* All data scraped must be **publicly accessible without login**.
* Do **not** use real or fake logged-in accounts to scrape Instagram.
* Avoid scraping private content, full comment threads, or follower lists; doing so may violate Instagram's [Terms of Use](https://help.instagram.com/581066165581870).

## 📈 Why Scrape.do?

Scrape.do handles the heavy lifting while scraping:

* Proxy rotation & anti-bot bypass
* Automatic JavaScript rendering
* Support for GraphQL, REST, and dynamic endpoints
* Free tier available (1000 API credits/month)

[Get your free API token here](https://dashboard.scrape.do/signup).
