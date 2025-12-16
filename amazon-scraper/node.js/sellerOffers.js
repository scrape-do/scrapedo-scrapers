const axios = require('axios');
const cheerio = require('cheerio');
const createCsvWriter = require('csv-writer').createObjectCsvWriter;

// Configuration
const token = "<SDO-token>";
const asin = "B0DZDBWM5B"; // Change this to any product ASIN
const geocode = "us";

// Build seller offers URL from ASIN
const targetUrl = `https://www.amazon.com/gp/product/ajax/aodAjaxMain/?asin=${asin}`;

// Make API request
const encodedUrl = encodeURIComponent(targetUrl);
const apiUrl = `https://api.scrape.do/?token=${token}&url=${encodedUrl}&geoCode=${geocode}`;

async function scrapeSellerOffers() {
    const response = await axios.get(apiUrl);
    const $ = cheerio.load(response.data);

    const offers = [];

    $('#aod-offer-soldBy').each((index, element) => {
        const soldBy = $(element);

        // Find parent container with price
        let container = soldBy.parent();
        while (container.length && !container.find('span.a-price-whole').length) {
            container = container.parent();
        }
        if (!container.length) return;

        // Price
        const whole = container.find('span.a-price-whole').first();
        const frac = container.find('span.a-price-fraction').first();
        const price = whole.length ? `$${whole.text().replace('.', '')}.${frac.text().trim()}` : 'N/A';

        // Seller
        const sellerLink = soldBy.find('a[href*="/gp/aag/main"]').first();
        const seller = sellerLink.length ? sellerLink.text().trim() : 'Amazon.com';

        // Seller rating
        const ratingDiv = soldBy.find('#aod-offer-seller-rating');
        const ratingAlt = ratingDiv.find('span.a-icon-alt').text().trim();
        const countElem = ratingDiv.find('span[id*="seller-rating-count"]');
        const countText = countElem.text().trim();

        // Extract rating value
        const ratingMatch = ratingAlt.match(/(\d+\.?\d*) out of 5/);
        const sellerRating = ratingMatch ? ratingMatch[1] : 'N/A';

        // Extract rating count
        const countMatch = countText.match(/\((\d[\d,]*)\s*ratings\)/);
        const ratingCount = countMatch ? countMatch[1] : 'N/A';

        // Extract positive percentage
        const positiveMatch = countText.match(/(\d+)%\s*positive/);
        const positivePct = positiveMatch ? `${positiveMatch[1]}%` : 'N/A';

        // Ships from
        const shipsDiv = container.find('#aod-offer-shipsFrom');
        const shipsElem = shipsDiv.find('span.a-color-base').first();
        const shipsFrom = shipsElem.length ? shipsElem.text().trim().replace(/\s+/g, ' ') : 'N/A';

        // Condition
        const conditionDiv = container.find('#aod-offer-heading');
        const condition = conditionDiv.length ? conditionDiv.text().trim().replace(/\s+/g, ' ') : 'New';

        // Delivery
        const deliveryDiv = container.find('div[id*="DELIVERY"]').first();
        let delivery = deliveryDiv.length ? deliveryDiv.text().trim().replace(/\s+/g, ' ') : 'N/A';
        delivery = delivery.substring(0, 80);

        offers.push({
            ASIN: asin,
            Price: price,
            Condition: condition,
            Seller: seller,
            'Seller Rating': sellerRating,
            'Rating Count': ratingCount,
            Positive: positivePct,
            'Ships From': shipsFrom,
            Delivery: delivery
        });
    });

    console.log(`Found ${offers.length} seller offers for ASIN: ${asin}`);

    // Export to CSV
    const csvWriter = createCsvWriter({
        path: 'sellerOffers.csv',
        header: [
            { id: 'ASIN', title: 'ASIN' },
            { id: 'Price', title: 'Price' },
            { id: 'Condition', title: 'Condition' },
            { id: 'Seller', title: 'Seller' },
            { id: 'Seller Rating', title: 'Seller Rating' },
            { id: 'Rating Count', title: 'Rating Count' },
            { id: 'Positive', title: 'Positive' },
            { id: 'Ships From', title: 'Ships From' },
            { id: 'Delivery', title: 'Delivery' }
        ]
    });

    await csvWriter.writeRecords(offers);
    console.log('Data exported to sellerOffers.csv');
}

scrapeSellerOffers().catch(console.error);
