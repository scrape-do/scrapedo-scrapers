const axios = require('axios');
const cheerio = require('cheerio');
const createCsvWriter = require('csv-writer').createObjectCsvWriter;

// Configuration
const token = "<SDO-token>";
const searchQuery = "laptop stands"; // Change this to any search term
const geocode = "us";
const zipcode = "10001";
const maxPages = 4; // Number of result pages to scrape

async function scrapeSearchResults() {
    const allProducts = [];

    // Loop through all result pages
    for (let page = 1; page <= maxPages; page++) {
        console.log(`Scraping page ${page}...`);

        // Build search URL with page number
        const targetUrl = `https://www.amazon.com/s?k=${encodeURIComponent(searchQuery)}&page=${page}`;

        // Make API request
        const encodedUrl = encodeURIComponent(targetUrl);
        const apiUrl = `https://api.scrape.do/plugin/amazon/?token=${token}&url=${encodedUrl}&geocode=${geocode}&zipcode=${zipcode}&output=html`;
        const response = await axios.get(apiUrl);

        const $ = cheerio.load(response.data);

        // Parse products on the current page
        let pageCount = 0;

        $('div.s-result-item').each((index, element) => {
            try {
                const product = $(element);

                // Extract product details
                const nameElem = product.find('h2 span');
                const name = nameElem.text();

                if (!name) return;

                // Price extraction
                let price = 'N/A';
                const priceHtml = product.find('span.a-price').html();
                if (priceHtml) {
                    const priceMatch = priceHtml.match(/a-offscreen">([^<]+)</);
                    if (priceMatch) price = priceMatch[1];
                }

                const linkElem = product.find('.a-link-normal').first();
                const link = linkElem.attr('href') || '';

                const imgElem = product.find('img').first();
                const image = imgElem.attr('src') || '';

                allProducts.push({
                    Name: name,
                    Price: price,
                    Link: link,
                    Image: image
                });
                pageCount++;
            } catch (e) {
                // Continue on error
            }
        });

        console.log(`  Found ${pageCount} products on page ${page}`);
    }

    // Export to CSV
    const csvWriter = createCsvWriter({
        path: 'searchResults.csv',
        header: [
            { id: 'Name', title: 'Name' },
            { id: 'Price', title: 'Price' },
            { id: 'Link', title: 'Link' },
            { id: 'Image', title: 'Image' }
        ]
    });

    await csvWriter.writeRecords(allProducts);

    console.log(`\nTotal products scraped: ${allProducts.length}`);
    console.log('Data exported to searchResults.csv');
}

scrapeSearchResults().catch(console.error);
