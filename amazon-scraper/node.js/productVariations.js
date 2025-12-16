const axios = require('axios');
const cheerio = require('cheerio');
const createCsvWriter = require('csv-writer').createObjectCsvWriter;

// Configuration
const token = "<SDO-token>";
const asin = "B0CG84XR6N"; // Change this to any product ASIN with variations
const geocode = "us";
const zipcode = "10001";

// Build product URL from ASIN
const targetUrl = `https://www.amazon.com/dp/${asin}`;

const scraped = new Set();
const results = [];
let dimNames = [];
let headers = [];

async function fetchPage(url) {
    const encodedUrl = encodeURIComponent(url);
    const apiUrl = `https://api.scrape.do/plugin/amazon/?token=${token}&url=${encodedUrl}&geocode=${geocode}&zipcode=${zipcode}&output=html`;
    const response = await axios.get(apiUrl);
    return cheerio.load(response.data);
}

function extractDimensions($) {
    const dimensions = {};
    $('div[id^="inline-twister-row-"]').each((i, row) => {
        const dimName = $(row).attr('id').replace('inline-twister-row-', '').replace('_name', '');
        const options = [];

        $(row).find('li[data-asin]').each((j, option) => {
            const optAsin = $(option).attr('data-asin');
            const isUnavailable = $(option).attr('data-initiallyunavailable') === 'true';

            if (optAsin && !isUnavailable) {
                const swatch = $(option).find('span.swatch-title-text-display');
                const img = $(option).find('img');
                const button = $(option).find('span.a-button-text');

                let optionName = 'Unknown';
                if (swatch.length) {
                    optionName = swatch.text().trim();
                } else if (img.length && img.attr('alt')) {
                    optionName = img.attr('alt').trim();
                } else if (button.length && button.text().trim() !== 'Select') {
                    optionName = button.text().trim();
                }

                options.push({ name: optionName, asin: optAsin });
            }
        });

        if (options.length) {
            dimensions[dimName] = options;
        }
    });
    return dimensions;
}

async function scrapeVariations(variationAsin, dimIndex = 0, prefix = '') {
    if (scraped.has(variationAsin)) return;

    const url = `https://www.amazon.com/dp/${variationAsin}/?th=1&psc=1`;
    const $ = await fetchPage(url);

    const titleElem = $('#productTitle');
    if (!titleElem.length) {
        console.log(`${prefix}[SKIP] ${variationAsin}: Product page not available`);
        scraped.add(variationAsin);
        return;
    }
    const name = titleElem.text().trim();

    // Price extraction
    let price;
    if ($('#outOfStockBuyBox_feature_div').length) {
        price = 'Out of Stock';
    } else {
        const whole = $('.a-price-whole').first().text();
        const fraction = $('.a-price-fraction').first().text();
        price = whole && fraction ? `$${whole}${fraction}` : 'N/A';
    }

    const pageDims = extractDimensions($);

    // End of recursion - collect final data
    if (dimIndex >= dimNames.length || Object.keys(pageDims).length === 0) {
        scraped.add(variationAsin);
        const selections = {};

        for (const dimName of dimNames) {
            const rowIds = [`inline-twister-row-${dimName}_name`, `inline-twister-row-${dimName}`];
            for (const rowId of rowIds) {
                const row = $(`#${rowId}`);
                if (row.length) {
                    const selected = row.find('span[class*="a-button-selected"]');
                    if (selected.length) {
                        const swatch = selected.find('span.swatch-title-text-display');
                        const img = selected.find('img');
                        if (swatch.length) {
                            selections[dimName] = swatch.text().trim();
                        } else if (img.length && img.attr('alt')) {
                            selections[dimName] = img.attr('alt').trim();
                        } else {
                            const text = selected.text().trim();
                            selections[dimName] = text.includes('Select') ? 'N/A' : text;
                        }
                        break;
                    } else {
                        const matchOption = row.find(`li[data-asin="${variationAsin}"]`);
                        if (matchOption.length) {
                            const swatch = matchOption.find('span.swatch-title-text-display');
                            const button = matchOption.find('span.a-button-text');
                            if (swatch.length) {
                                selections[dimName] = swatch.text().trim();
                            } else if (button.length && !button.text().includes('Select')) {
                                selections[dimName] = button.text().trim();
                            }
                            break;
                        }
                    }
                    break;
                }
            }
        }

        const row = [variationAsin, name, ...dimNames.map(dim => selections[dim] || 'N/A'), price];
        results.push(row);

        const selStr = Object.entries(selections).map(([k, v]) => `${k}:${v}`).join(', ');
        console.log(`${prefix}[OK] ${variationAsin}: ${price} | ${selStr}`);
        return;
    }

    // Continue recursion through dimensions
    const currentDim = dimNames[dimIndex];
    if (pageDims[currentDim]) {
        const options = pageDims[currentDim];
        if (dimIndex === 0) {
            console.log(`${prefix}Found ${options.length} ${currentDim} options`);
        }

        for (let i = 0; i < options.length; i++) {
            const option = options[i];
            if (dimIndex === 0) {
                console.log(`${prefix}${currentDim} ${i + 1}/${options.length}: ${option.name}`);
            }
            await scrapeVariations(option.asin, dimIndex + 1, prefix + '    ');
        }
    } else {
        await scrapeVariations(variationAsin, dimIndex + 1, prefix);
    }
}

async function main() {
    // Initial page scrape to find dimensions
    const $ = await fetchPage(targetUrl);
    const dimensions = extractDimensions($);

    console.log(`Found dimensions: ${Object.keys(dimensions).join(', ')}`);
    for (const [dimName, options] of Object.entries(dimensions)) {
        console.log(`  ${dimName}: ${options.length} options`);
    }

    // Setup dimension traversal order and CSV headers
    const priority = ['color', 'size', 'style', 'pattern', 'material', 'fit'];
    dimNames = Object.keys(dimensions).sort((a, b) => {
        const aIdx = priority.indexOf(a.toLowerCase());
        const bIdx = priority.indexOf(b.toLowerCase());
        return (aIdx === -1 ? priority.length : aIdx) - (bIdx === -1 ? priority.length : bIdx);
    });
    headers = ['ASIN', 'Product Name', ...dimNames, 'Price'];

    console.log(`\nDimension traversal order: ${dimNames.join(', ')}`);
    console.log('\nStarting variation crawling...');

    await scrapeVariations(asin);

    // Export to CSV
    const csvWriter = createCsvWriter({
        path: 'productVariations.csv',
        header: headers.map(h => ({ id: h, title: h }))
    });

    // Convert results array to objects
    const records = results.map(row => {
        const obj = {};
        headers.forEach((h, i) => obj[h] = row[i]);
        return obj;
    });

    await csvWriter.writeRecords(records);

    console.log(`\nDone! Scraped ${results.length} unique variations`);
    console.log('Data exported to productVariations.csv');
}

main().catch(console.error);
