#!/bin/bash

# =============================================================================
# Amazon Product Detail Page (PDP) - Scrape.do Amazon API
# =============================================================================
# This script fetches structured product data from Amazon using Scrape.do's
# Amazon API. Returns JSON with product title, pricing, ratings, images,
# best seller rankings, and technical specifications.
#
# Endpoint: GET https://api.scrape.do/plugin/amazon/pdp
# Documentation: https://scrape.do/documentation/amazon-scraper-api/
# =============================================================================

# Configuration
TOKEN="<SDO-token>"
ASIN="B0C7BKZ883"  # Change this to any product ASIN
GEOCODE="us"
ZIPCODE="10001"

# Output file
OUTPUT_FILE="../output/SDOpdp.json"

# Build API URL
API_URL="https://api.scrape.do/plugin/amazon/pdp?token=${TOKEN}&asin=${ASIN}&geocode=${GEOCODE}&zipcode=${ZIPCODE}"

echo "Fetching product data..."
echo "ASIN: $ASIN"
echo ""

# Make the request and save to file
curl -s "$API_URL" | python3 -m json.tool > "$OUTPUT_FILE"

echo "Data exported to $OUTPUT_FILE"
