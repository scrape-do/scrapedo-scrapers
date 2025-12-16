const axios = require('axios');
const cheerio = require('cheerio');
const createCsvWriter = require('csv-writer').createObjectCsvWriter;

// Configuration
const token = "<SDO-token>";
const category = "electronics"; // Change this to any best sellers category
const geocode = "us";
const maxPages = 2; // Best sellers shows 50 products per page

// Build base URL
const baseUrl = `https://www.amazon.com/Best-Sellers-Electronics/zgbs/${category}/`;

// playWithBrowser actions: scroll to pagination to load all products
const playActions = [
    { "Action": "ScrollTo", "Selector": ".a-pagination" },
    { "Action": "Wait", "Timeout": 3000 }
];
const encodedActions = encodeURIComponent(JSON.stringify(playActions));

async function scrapeBestSellers() {
    const allProducts = [];

    // Loop through pages
    for (let page = 1; page <= maxPages; page++) {
        console.log(`Scraping page ${page}...`);

        // Build URL for current page
        let targetUrl;
        if (page === 1) {
            targetUrl = baseUrl;
        } else {
            targetUrl = `${baseUrl}ref=zg_bs_pg_${page}_${category}?_encoding=UTF8&pg=${page}`;
        }

        // Make API request
        const encodedUrl = encodeURIComponent(targetUrl);
        const apiUrl = `https://api.scrape.do/?token=${token}&url=${encodedUrl}&geoCode=${geocode}&render=true&playWithBrowser=${encodedActions}`;
        const response = await axios.get(apiUrl);

        const $ = cheerio.load(response.data);

        // Find all product items
        const productItems = $('.zg-no-numbers');
        let pageCount = 0;

        productItems.each((index, element) => {
            try {
                const item = $(element);

                // Ranking
                const ranking = String(index + 1 + (page - 1) * 50);

                // ASIN
                const asinElem = item.find('[data-asin]').first();
                const asin = asinElem.attr('data-asin') || '';

                // Image
                const imgTag = item.find('img').first();
                const image = imgTag.attr('src') || '';

                // Name & Link
                let name = '';
                let link = '';
                item.find('a.a-link-normal').each((i, aTag) => {
                    const href = $(aTag).attr('href') || '';
                    const text = $(aTag).text().trim();
                    if (href.includes('/dp/') && text && !text.startsWith('EUR') && !text.startsWith('$')) {
                        link = href.startsWith('http') ? href : `https://www.amazon.com${href}`;
                        name = text;
                        return false; // break
                    }
                });

                // Price
                const priceTag = item.find('span[class*="p13n-sc-price"]').first();
                const price = priceTag.text().trim() || 'N/A';

                // Rating & Review Count
                let rating = '';
                let reviewCount = '';
                const starIcon = item.find('i[class*="a-icon-star"]').first();
                if (starIcon.length) {
                    const parentLink = starIcon.closest('a');
                    const ariaLabel = parentLink.attr('aria-label') || '';
                    if (ariaLabel.includes('stars')) {
                        const parts = ariaLabel.split('stars');
                        rating = parts[0] ? parts[0].trim() + ' stars' : '';
                        if (parts[1]) {
                            const reviewPart = parts[1].trim().replace(/^,/, '').trim();
                            reviewCount = reviewPart.replace(' ratings', '');
                        }
                    }
                }

                if (name) {
                    allProducts.push({
                        Ranking: ranking,
                        ASIN: asin,
                        Name: name,
                        Price: price,
                        Rating: rating,
                        'Review Count': reviewCount,
                        Link: link,
                        Image: image
                    });
                    pageCount++;
                }
            } catch (e) {
                // Continue on error
            }
        });

        console.log(`  Found ${pageCount} products on page ${page}`);
    }

    // Export to CSV
    const csvWriter = createCsvWriter({
        path: 'bestSellers.csv',
        header: [
            { id: 'Ranking', title: 'Ranking' },
            { id: 'ASIN', title: 'ASIN' },
            { id: 'Name', title: 'Name' },
            { id: 'Price', title: 'Price' },
            { id: 'Rating', title: 'Rating' },
            { id: 'Review Count', title: 'Review Count' },
            { id: 'Link', title: 'Link' },
            { id: 'Image', title: 'Image' }
        ]
    });

    await csvWriter.writeRecords(allProducts);

    console.log(`\nTotal products scraped: ${allProducts.length}`);
    console.log('Data exported to bestSellers.csv');
}

scrapeBestSellers().catch(console.error);
