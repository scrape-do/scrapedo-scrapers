const axios = require('axios');
const cheerio = require('cheerio');
const createCsvWriter = require('csv-writer').createObjectCsvWriter;

// Configuration
const token = "<SDO-token>";
const asins = ["B0BLRJ4R8F", "B081YXWDTQ", "B07D74DT3B"]; // Change these to any product ASINs
const geocode = "us";
const zipcode = "10001";

async function scrapeSingleProducts() {
    const allProducts = [];

    // Loop through all ASINs
    for (const asin of asins) {
        // Build product URL from ASIN
        const targetUrl = `https://www.amazon.com/dp/${asin}`;

        // Make API request
        const encodedUrl = encodeURIComponent(targetUrl);
        const apiUrl = `https://api.scrape.do/plugin/amazon/?token=${token}&url=${encodedUrl}&geocode=${geocode}&zipcode=${zipcode}&output=html`;

        try {
            const response = await axios.get(apiUrl);
            const $ = cheerio.load(response.data);

            // Extract product details
            const nameElem = $('#productTitle');
            const name = nameElem.text().trim();

            if (!name) {
                console.log(`Error scraping ${asin}: Product title not found`);
                continue;
            }

            // Extract price
            let price;
            if ($('#outOfStockBuyBox_feature_div').length > 0) {
                price = 'Out of Stock';
            } else {
                const whole = $('.a-price-whole').first().text();
                const fraction = $('.a-price-fraction').first().text();
                price = whole && fraction ? `$${whole}${fraction}` : 'N/A';
            }

            // Extract image
            const imageElem = $('#landingImage');
            const image = imageElem.attr('src') || 'N/A';

            // Extract rating
            const ratingElem = $('.AverageCustomerReviews');
            const ratingText = ratingElem.text().trim();
            const rating = ratingText ? ratingText.split(' out of')[0] : 'N/A';

            allProducts.push({
                ASIN: asin,
                Name: name,
                Price: price,
                Image: image,
                Rating: rating
            });

            console.log(`Scraped: ${asin} - ${name.substring(0, 50)}...`);
        } catch (e) {
            console.log(`Error scraping ${asin}: ${e.message}`);
            continue;
        }
    }

    // Export to CSV
    const csvWriter = createCsvWriter({
        path: 'singleProduct.csv',
        header: [
            { id: 'ASIN', title: 'ASIN' },
            { id: 'Name', title: 'Name' },
            { id: 'Price', title: 'Price' },
            { id: 'Image', title: 'Image' },
            { id: 'Rating', title: 'Rating' }
        ]
    });

    await csvWriter.writeRecords(allProducts);

    console.log(`\nScraped ${allProducts.length} products`);
    console.log('Data exported to singleProduct.csv');
}

scrapeSingleProducts().catch(console.error);
