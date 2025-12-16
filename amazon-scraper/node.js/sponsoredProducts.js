const axios = require('axios');
const cheerio = require('cheerio');
const fs = require('fs');

// Configuration
const token = "<SDO-token>";
const searchQuery = "gaming headsets"; // Change this to any search term
const geocode = "us";
const zipcode = "10001";

// Build search URL
const targetUrl = `https://www.amazon.com/s?k=${encodeURIComponent(searchQuery)}`;

// Make API request
const encodedUrl = encodeURIComponent(targetUrl);
const apiUrl = `https://api.scrape.do/plugin/amazon/?token=${token}&url=${encodedUrl}&geocode=${geocode}&zipcode=${zipcode}&output=html`;

async function scrapeSponsoredProducts() {
    const response = await axios.get(apiUrl);
    const $ = cheerio.load(response.data);

    // Initialize output structure
    const sponsoredData = {
        video_ads: [],
        in_search: [],
        carousels: [],
        featured_brands: []
    };

    // =============================================================================
    // 1. VIDEO ADS - Top featured + VIDEO_SINGLE_PRODUCT
    // =============================================================================

    // Extract top featured video ad (sb-video-product-collection-desktop)
    $('div[cel_widget_id*="sb-video-product-collection-desktop"]').each((i, widget) => {
        try {
            const $widget = $(widget);

            // Find brand and headline
            const brandImg = $widget.find('img[alt]').first();
            const brandName = brandImg.attr('alt') || '';

            const headlineElem = $widget.find('a[data-elementid="sb-headline"]');
            let headline = '';
            if (headlineElem.length) {
                const truncate = headlineElem.find('span.a-truncate-full');
                headline = truncate.text().trim();
            }

            // Extract products from carousel within video ad
            const products = [];
            $widget.find('li.a-carousel-card').each((j, item) => {
                const asinDiv = $(item).find('div[data-asin]').first();
                const asin = asinDiv.attr('data-asin');
                if (asin) {
                    const img = $(item).find('img').first();
                    products.push({
                        asin: asin,
                        image: img.attr('src') || ''
                    });
                }
            });

            sponsoredData.video_ads.push({
                type: 'top_featured',
                brand: brandName,
                headline: headline,
                products: products
            });
        } catch (e) {
            // Continue on error
        }
    });

    // Extract VIDEO_SINGLE_PRODUCT items
    $('div[class*="VIDEO_SINGLE_PRODUCT"]').each((i, videoItem) => {
        try {
            const $item = $(videoItem);
            const component = $item.find('span[data-component-type="sbv-video-single-product"]');

            if (component.length && component.attr('data-component-props')) {
                const props = JSON.parse(component.attr('data-component-props'));

                // Extract product link and ASIN
                const videoLink = $item.find('a.sbv-desktop-video-link').first();
                const href = videoLink.attr('href') || '';
                const asinMatch = href.match(/\/dp\/([A-Z0-9]{10})/);

                sponsoredData.video_ads.push({
                    type: 'video_single_product',
                    video_url: props.videoSrc || '',
                    thumbnail: props.videoPreviewImageSrc || '',
                    asin: asinMatch ? asinMatch[1] : '',
                    campaign_id: props.campaignId || '',
                    ad_id: props.adId || '',
                    link: href
                });
            }
        } catch (e) {
            // Continue on error
        }
    });

    // =============================================================================
    // 2. IN-SEARCH ADS - AdHolder with actual ASINs
    // =============================================================================

    $('div[class*="AdHolder"]').each((i, ad) => {
        const $ad = $(ad);
        const asin = $ad.attr('data-asin');

        if (asin && $ad.attr('data-component-type') === 's-search-result') {
            try {
                const nameElem = $ad.find('h2 span').first();
                const name = nameElem.text().trim();

                // Price extraction
                let price = 'Price not available';
                const priceHtml = $ad.find('span.a-price').html();
                if (priceHtml) {
                    const priceMatch = priceHtml.match(/a-offscreen">([^<]+)</);
                    if (priceMatch) price = priceMatch[1];
                }

                const linkElem = $ad.find('.a-link-normal').first();
                const link = linkElem.attr('href') || '';

                const imgElem = $ad.find('img').first();
                const image = imgElem.attr('src') || '';

                if (name) {
                    sponsoredData.in_search.push({
                        asin: asin,
                        name: name,
                        price: price,
                        link: link,
                        image: image
                    });
                }
            } catch (e) {
                // Continue on error
            }
        }
    });

    // =============================================================================
    // 3. CAROUSELS - Themed collection (brand + products)
    // =============================================================================

    let themedCollections = $('div[class*="sb-desktop"][id*="CardInstance"]');
    if (!themedCollections.length) {
        themedCollections = $('div[data-slot="desktop-inline"]');
    }

    themedCollections.each((i, collection) => {
        try {
            const $collection = $(collection);

            // Skip if it's a video single product (already captured)
            if ($collection.attr('class')?.includes('VIDEO_SINGLE_PRODUCT')) return;

            // Extract brand name
            const brandImg = $collection.find('img[alt]').first();
            const brandName = brandImg.attr('alt') || '';

            // Extract headline
            const headlineElem = $collection.find('a[data-elementid="sb-headline"]');
            let headline = '';
            if (headlineElem.length) {
                const truncate = headlineElem.find('span.a-truncate-full');
                headline = truncate.text().trim();
            }

            // Extract products from carousel
            const products = [];
            $collection.find('li.a-carousel-card').each((j, item) => {
                const asinDiv = $(item).find('div[data-asin]').first();
                const asin = asinDiv.attr('data-asin');
                if (asin) {
                    const img = $(item).find('img[alt]').first();
                    products.push({
                        asin: asin,
                        name: img.attr('alt') || '',
                        image: img.attr('src') || ''
                    });
                }
            });

            if (brandName || products.length) {
                sponsoredData.carousels.push({
                    brand: brandName,
                    headline: headline,
                    products: products
                });
            }
        } catch (e) {
            // Continue on error
        }
    });

    // =============================================================================
    // 4. FEATURED BRANDS - "Brands related to your search"
    // =============================================================================

    $('div[cel_widget_id*="multi-brand-creative-desktop"]').each((i, section) => {
        try {
            const $section = $(section);
            const adFeedback = $section.find('div[data-ad-creative-list]').first();

            if (adFeedback.length) {
                const creativeList = JSON.parse(adFeedback.attr('data-ad-creative-list') || '[]');

                for (const brand of creativeList) {
                    const brandName = brand.title || '';
                    const brandImg = $section.find(`img[alt="${brandName}"]`).first();

                    sponsoredData.featured_brands.push({
                        brand: brandName,
                        campaign_id: brand.campaignId || '',
                        ad_id: brand.adId || '',
                        image: brandImg.attr('src') || ''
                    });
                }
            }
        } catch (e) {
            // Continue on error
        }
    });

    // =============================================================================
    // OUTPUT
    // =============================================================================

    // Print summary
    console.log('=== Sponsored Products Summary ===');
    console.log(`Video Ads: ${sponsoredData.video_ads.length}`);
    console.log(`In-Search Ads: ${sponsoredData.in_search.length}`);
    console.log(`Carousels: ${sponsoredData.carousels.length}`);
    console.log(`Featured Brands: ${sponsoredData.featured_brands.length}`);

    // Export to JSON
    const outputFile = 'sponsoredProducts.json';
    fs.writeFileSync(outputFile, JSON.stringify(sponsoredData, null, 2), 'utf-8');

    console.log(`\nData exported to ${outputFile}`);
}

scrapeSponsoredProducts().catch(console.error);
