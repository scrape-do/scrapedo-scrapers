#!/bin/bash

# =============================================================================
# Amazon Search Results - Scrape.do Amazon API
# =============================================================================
# This script fetches structured search results from Amazon using Scrape.do's
# Amazon API. Returns JSON with product listings including titles, prices,
# ratings, Prime status, sponsored flags, and position rankings.
#
# Endpoint: GET https://api.scrape.do/plugin/amazon/search
# Documentation: https://scrape.do/documentation/amazon-scraper-api/
# =============================================================================

# Configuration
TOKEN="<SDO-token>"
KEYWORD="laptop%20stands"  # URL-encoded search query
GEOCODE="us"
ZIPCODE="10001"
PAGE="1"

# Output file
OUTPUT_FILE="../output/SDOsearch.json"

# Build API URL
API_URL="https://api.scrape.do/plugin/amazon/search?token=${TOKEN}&keyword=${KEYWORD}&geocode=${GEOCODE}&zipcode=${ZIPCODE}&page=${PAGE}"

echo "Fetching search results..."
echo "Keyword: laptop stands"
echo "Page: $PAGE"
echo ""

# Make the request and save to file
curl -s "$API_URL" | python3 -m json.tool > "$OUTPUT_FILE"

echo "Data exported to $OUTPUT_FILE"
