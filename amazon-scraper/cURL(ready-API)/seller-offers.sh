#!/bin/bash

# =============================================================================
# Amazon Seller Offers (All Offers) - Scrape.do Amazon API
# =============================================================================
# This script fetches all seller listings for a product from Amazon using
# Scrape.do's Amazon API. Returns JSON with pricing, shipping costs, seller
# information, and Buy Box status.
#
# Endpoint: GET https://api.scrape.do/plugin/amazon/offer-listing
# Documentation: https://scrape.do/documentation/amazon-scraper-api/
# =============================================================================

# Configuration
TOKEN="<SDO-token>"
ASIN="B0DGJ7HYG1"  # Change this to any product ASIN
GEOCODE="us"
ZIPCODE="10001"

# Output file
OUTPUT_FILE="../output/SDOsellerOffers.json"

# Build API URL
API_URL="https://api.scrape.do/plugin/amazon/offer-listing?token=${TOKEN}&asin=${ASIN}&geocode=${GEOCODE}&zipcode=${ZIPCODE}"

echo "Fetching seller offers..."
echo "ASIN: $ASIN"
echo ""

# Make the request and save to file
curl -s "$API_URL" | python3 -m json.tool > "$OUTPUT_FILE"

echo "Data exported to $OUTPUT_FILE"
