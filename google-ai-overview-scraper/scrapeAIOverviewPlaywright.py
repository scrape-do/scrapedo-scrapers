import json
import urllib.parse
from playwright.sync_api import sync_playwright

# Configuration
token = "<your_token>"
query = "how does photosynthesis work"

encoded_query = urllib.parse.quote_plus(query)

# Try with standard URL first, then with US geolocation parameters
google_urls = [
    f"https://www.google.com/search?q={encoded_query}&hl=en&gl=us",
    f"https://www.google.com/search?q={encoded_query}&hl=en&gl=us&uule=w+CAIQICIYV2VzdCBOZXcgWW9yaywgTmV3IEplcnNleQ",
]

# Scrape.do proxy routes browser traffic through residential proxies,
# bypassing Google's bot detection while Playwright renders the JS.
proxy_config = {
    "server": "http://proxy.scrape.do:8080",
    "username": token,
    "password": "super=true",
}


def detect_aio(page):
    """Check if the AI Overview heading exists on the page."""
    return page.evaluate("""() => {
        const headings = document.querySelectorAll('h1, h2, div.Fzsovc, div.YzCcne');
        for (const h of headings) {
            if (h.textContent.trim() === 'AI Overview') return true;
        }
        return false;
    }""")


def get_aio_container(page):
    """Get a handle to the AI Overview content container."""
    return page.evaluate_handle("""() => {
        const headings = document.querySelectorAll('h1, h2, div.Fzsovc, div.YzCcne');
        for (const h of headings) {
            if (h.textContent.trim() === 'AI Overview') {
                let el = h;
                for (let i = 0; i < 10; i++) {
                    el = el.parentElement;
                    if (!el) break;
                    if (el.classList.contains('Kevs9')) return el;
                }
                return h.parentElement?.parentElement || h.parentElement;
            }
        }
        return null;
    }""")


def extract_text_blocks(page, container):
    """Extract text paragraphs from the AIO container."""
    return page.evaluate("""(container) => {
        const blocks = [];
        const seen = new Set();
        const skipPatterns = [
            /^Show (more|all|less)$/i,
            /^\\+\\d+$/,
            /^AI Overview$/i,
            /not available/i,
            /try again later/i,
        ];

        function shouldSkip(text) {
            return skipPatterns.some(p => p.test(text));
        }

        // Primary: Y3BBE divs hold the main AIO paragraphs
        for (const div of container.querySelectorAll('div.Y3BBE')) {
            // Remove inline style tags and reference badge elements
            const clone = div.cloneNode(true);
            clone.querySelectorAll('style, .WTfRgd, .wJwe6c, .iFMVXd').forEach(e => e.remove());
            let text = clone.textContent.trim();
            // Strip any CSS that leaked in (e.g., ".SGF5Lb{display:...")
            text = text.replace(/\.[A-Za-z0-9_]+\{[^}]*\}/g, '').trim();
            // Strip inline reference badges like "Science News Explores +3"
            text = text.replace(/\s*[A-Z][a-zA-Z\s]+\+\d+\s*$/, '').trim();
            if (text.length > 15 && !seen.has(text) && !shouldSkip(text)) {
                seen.add(text);
                blocks.push({ type: 'paragraph', text });
            }
        }

        // Fallback: jsname=KFl8ub wrapper children
        if (blocks.length === 0) {
            const wrapper = container.querySelector('[jsname="KFl8ub"]');
            if (wrapper) {
                for (const child of wrapper.children) {
                    if (child.classList.contains('WTfRgd')) continue;
                    if (child.classList.contains('alk4p')) continue;
                    const text = child.textContent.trim();
                    if (text.length > 15 && !seen.has(text) && !shouldSkip(text)) {
                        seen.add(text);
                        blocks.push({ type: 'paragraph', text });
                    }
                }
            }
        }

        // Second fallback: substantial leaf-node text
        if (blocks.length === 0) {
            for (const el of container.querySelectorAll('span, div, p')) {
                if (el.querySelector('span, div, p, ul, ol')) continue;
                const text = el.textContent.trim();
                if (text.length > 50 && !seen.has(text) && !shouldSkip(text)) {
                    seen.add(text);
                    blocks.push({ type: 'paragraph', text });
                }
            }
        }

        return blocks;
    }""", container)


def extract_references(page, container):
    """Extract source references from AIO reference cards."""
    return page.evaluate("""(container) => {
        const refs = [];
        const seen = new Set();

        // Primary: reference cards in li.jydCyd
        for (const card of container.querySelectorAll('li.jydCyd')) {
            const titleEl = card.querySelector('.Nn35F');
            const linkEl = card.querySelector('a[href^="http"]');
            const snippetEl = card.querySelector('.VwiC3b');

            const title = titleEl ? titleEl.textContent.trim() : '';
            const url = linkEl ? linkEl.getAttribute('href') : '';
            const snippet = snippetEl ? snippetEl.textContent.trim() : '';

            if (url && !url.includes('google.com') && !seen.has(url)) {
                seen.add(url);
                refs.push({ title: title || url, url, snippet });
            }
        }

        // Fallback: walk up to #Odp5De and find external links
        if (refs.length === 0) {
            let searchEl = container;
            for (let i = 0; i < 5; i++) {
                if (!searchEl.parentElement) break;
                searchEl = searchEl.parentElement;
                if (searchEl.id === 'Odp5De') break;
            }

            for (const a of searchEl.querySelectorAll('a[href^="http"]')) {
                const url = a.getAttribute('href');
                if (url.includes('google.com') || seen.has(url)) continue;
                seen.add(url);

                let title = a.textContent.trim();
                if (!title || title.length <= 3) {
                    const parent = a.closest('li') || a.closest('div');
                    const titleEl = parent && parent.querySelector('.Nn35F, .LC20lb');
                    title = titleEl ? titleEl.textContent.trim() : url;
                }
                if (title.length > 3) {
                    refs.push({ title, url, snippet: '' });
                }
            }
        }

        return refs;
    }""", container)


with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        proxy=proxy_config,
    )
    context = browser.new_context(
        ignore_https_errors=True,
        viewport={"width": 1280, "height": 900},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    )
    page = context.new_page()

    aio_found = False
    for attempt, url in enumerate(google_urls):
        label = "standard" if attempt == 0 else "US geocode (uule)"
        print(f"Attempt {attempt + 1}: {label}")

        page.goto(url, timeout=60000, wait_until="networkidle")
        page.wait_for_timeout(8000)

        # Save rendered HTML for debugging
        with open("response-rendered.html", "w", encoding="utf-8") as f:
            f.write(page.content())

        if detect_aio(page):
            print("AI Overview detected.")
            aio_found = True
            break
        else:
            print("No AI Overview found, trying next approach...")

    if not aio_found:
        print("\nNo AI Overview found after all attempts.")
        print("Google may not trigger AIO for this query from this location.")
        print("Rendered HTML saved to response-rendered.html for inspection.")
        browser.close()
        exit()

    aio_container = get_aio_container(page)
    text_blocks = extract_text_blocks(page, aio_container)
    references = extract_references(page, aio_container)

    browser.close()

result = {
    "query": query,
    "ai_overview_found": True,
    "text_blocks": text_blocks,
    "references": references,
}

output_file = "ai-overview-results.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2, ensure_ascii=False)

print(f"\nAI Overview extracted for: '{query}'")
print(f"  {len(text_blocks)} text blocks, {len(references)} references")
for block in text_blocks:
    preview = block["text"][:100].encode("ascii", "replace").decode()
    print(f"  [{block['type']}] {preview}...")
for ref in references:
    title = ref["title"][:60].encode("ascii", "replace").decode()
    url = ref["url"][:60]
    print(f"  [ref] {title} -> {url}")
print(f"Saved to {output_file}")
