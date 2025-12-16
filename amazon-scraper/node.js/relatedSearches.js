const axios = require('axios');
const cheerio = require('cheerio');

// Configuration
const token = "<SDO-token>";
const searchQuery = "laptop stands"; // Change this to any search term
const geocode = "us";
const zipcode = "10001";

// Build search URL
const targetUrl = `https://www.amazon.com/s?k=${encodeURIComponent(searchQuery)}`;

// Make API request
const encodedUrl = encodeURIComponent(targetUrl);
const apiUrl = `https://api.scrape.do/plugin/amazon/?token=${token}&url=${encodedUrl}&geocode=${geocode}&zipcode=${zipcode}&output=html`;

async function scrapeRelatedSearches() {
    const response = await axios.get(apiUrl);
    const $ = cheerio.load(response.data);

    // Find all related search terms
    const relatedSearches = [];

    $('div.a-box-inner.a-padding-mini').each((index, element) => {
        const text = $(element).text().trim();
        if (text) {
            relatedSearches.push(text);
        }
    });

    console.log('Related searches:');
    relatedSearches.forEach((term, index) => {
        console.log(`  ${index + 1}. ${term}`);
    });
}

scrapeRelatedSearches().catch(console.error);
