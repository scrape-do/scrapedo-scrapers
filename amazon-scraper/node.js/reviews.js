const axios = require('axios');
const cheerio = require('cheerio');
const createCsvWriter = require('csv-writer').createObjectCsvWriter;

// Configuration
const token = "<SDO-token>";
const asin = "B07TCJS1NS"; // Change this to any product ASIN
const geocode = "us";

// Build product URL from ASIN
const targetUrl = `https://www.amazon.com/dp/${asin}`;

// Make API request
const encodedUrl = encodeURIComponent(targetUrl);
const apiUrl = `https://api.scrape.do/?token=${token}&url=${encodedUrl}&geoCode=${geocode}`;

async function scrapeReviews() {
    const response = await axios.get(apiUrl);
    const $ = cheerio.load(response.data);

    const reviews = [];

    $('li[data-hook="review"]').each((index, element) => {
        const review = $(element);

        // Get star rating
        const ratingElem = review.find('i[data-hook="review-star-rating"]').first() ||
                          review.find('i[class*="a-icon-star"]').first();
        const ratingText = ratingElem.find('span.a-icon-alt').text();
        const rating = ratingText ? ratingText.split(' ')[0] : 'N/A';

        // Get review date (remove country prefix)
        const dateElem = review.find('span[data-hook="review-date"]');
        const dateText = dateElem.text();
        const date = dateText ? dateText.replace(/Reviewed in .* on /, '') : 'N/A';

        // Get review content
        const contentElem = review.find('span[data-hook="review-body"]');
        const content = contentElem.text().trim() || 'N/A';

        // Get helpful votes count
        const helpfulElem = review.find('span[data-hook="helpful-vote-statement"]');
        const helpfulText = helpfulElem.text();
        const helpfulMatch = helpfulText.match(/\d+/);
        const helpful = helpfulMatch ? helpfulMatch[0] : '0';

        reviews.push({
            review_id: review.attr('id') || '',
            rating: rating,
            date: date,
            content: content,
            helpful: helpful
        });
    });

    // Export to CSV
    const csvWriter = createCsvWriter({
        path: 'reviews.csv',
        header: [
            { id: 'review_id', title: 'review_id' },
            { id: 'rating', title: 'rating' },
            { id: 'date', title: 'date' },
            { id: 'content', title: 'content' },
            { id: 'helpful', title: 'helpful' }
        ]
    });

    await csvWriter.writeRecords(reviews);

    console.log(`Found ${reviews.length} reviews`);
    console.log('Data exported to reviews.csv');
}

scrapeReviews().catch(console.error);
