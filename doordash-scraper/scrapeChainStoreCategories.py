import requests
import json
import csv

# Scrape.do API token and DoorDash GraphQL endpoint
TOKEN = "<your-token>"
TARGET_URL = "https://www.doordash.com/graphql/categorySearch?operation=categorySearch"
SESSION_ID = "<session-id>"
STORE_ID = "<store-id>"
CATEGORY_ID = "<category-id>"

# Build the Scrape.do API URL
API_URL = f"http://api.scrape.do/?token={TOKEN}&super=true&url={TARGET_URL}&sessionId={SESSION_ID}"

# GraphQL query for fetching category products
QUERY = """query categorySearch($storeId: ID!, $categoryId: ID!, $subCategoryId: ID, $limit: Int, $cursor: String, $filterKeysList: [String!], $sortBysList: [RetailSortByOption!]!, $filterQuery: String, $aggregateStoreIds: [String!]) { retailStoreCategoryFeed(storeId: $storeId l1CategoryId: $categoryId l2CategoryId: $subCategoryId limit: $limit cursor: $cursor filterKeysList: $filterKeysList sortBysList: $sortBysList filterQuery: $filterQuery aggregateStoreIds: $aggregateStoreIds) { legoRetailItems { custom } pageInfo { cursor hasNextPage } } }"""

# Helper to parse product fields from the GraphQL response
# Extracts name, price, reviews, stock, image, and description
def parse_product_fields(facet):
    try:
        custom = json.loads(facet.get('custom', '{}'))
    except Exception:
        custom = {}
    item_data = custom.get('item_data', {})
    price_name_info = custom.get('price_name_info', {}).get('default', {}).get('base', {})
    logging_info = custom.get('logging', {})
    image_url = custom.get('image', {}).get('remote', {}).get('uri', '')

    name = item_data.get('item_name') or price_name_info.get('name')
    price = item_data.get('price', {}).get('display_string') or price_name_info.get('price', {}).get('default', {}).get('price')
    reviews_count = logging_info.get('item_num_of_reviews') or price_name_info.get('ratings', {}).get('count_of_reviews')
    reviews_avg = logging_info.get('item_star_rating') or price_name_info.get('ratings', {}).get('average')
    stock = item_data.get('stock_level') or logging_info.get('product_badges')
    image = image_url
    description = logging_info.get('description')

    return [name, price, reviews_count, reviews_avg, stock, image, description]

# Main scraping logic
# Paginates through all category products and writes them to CSV
def main():
    cursor = ""
    page_num = 1
    products = []
    while True:
        # Build the GraphQL payload for the current page
        payload = {
            "query": QUERY,
            "variables": {
                "storeId": STORE_ID,
                "categoryId": CATEGORY_ID,
                "sortBysList": ["UNSPECIFIED"],
                "cursor": cursor,
                "limit": 500,
                "filterQuery": "",
                "filterKeysList": [],
                "aggregateStoreIds": []
            }
        }
        print(f"Requesting page {page_num}...")
        try:
            response = requests.post(API_URL, data=json.dumps(payload))
            response.raise_for_status()
            data = response.json()
        except Exception as e:
            print(f"Request or JSON decode failed: {e}")
            break
        # Parse the product feed and extract product data
        feed = data.get("data", {}).get("retailStoreCategoryFeed", {})
        lego_items = feed.get("legoRetailItems", [])
        for facet in lego_items:
            prod = parse_product_fields(facet)
            if prod[0]:
                products.append(prod)
        # Check for next page
        page_info = feed.get("pageInfo", {})
        next_cursor = page_info.get("cursor")
        has_next = page_info.get("hasNextPage")
        if not has_next or not next_cursor or next_cursor == cursor:
            break
        cursor = next_cursor
        page_num += 1
    # Write all products to CSV file
    with open("doordash_category_products.csv", 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['name', 'price', 'reviews_count', 'reviews_avg', 'stock', 'image_url', 'description'])
        writer.writerows(products)
    print(f"Extracted {len(products)} products to doordash_category_products.csv")

if __name__ == "__main__":
    main()
