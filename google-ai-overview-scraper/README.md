# Google AI Overview Scraper

Extract Google's AI-generated overview summaries — the text blocks and source references that appear at the top of search results. Two approaches: a SERP API script that handles the tricky deferred-state problem automatically, and a Playwright script that renders the actual SERP and extracts from the DOM.

[Find the full technical guide here. 📘](https://scrape.do/blog/scrape-google-ai-overview/)

## What's Included

* `scrapeAIOverviewSerpApi.py`: Calls Scrape.do's SERP API, handles both `complete` and `deferred` AI Overview states, flattens nested text blocks, and normalizes references. Pure `requests` — no browser needed.
* `scrapeAIOverviewPlaywright.py`: Launches Chromium through Scrape.do's residential proxy, renders the full SERP, detects the AI Overview container, and extracts text + references from the live DOM. Falls back to a US-geolocated URL (via `uule`) if the first attempt doesn't trigger an AI Overview.

## Requirements

* Python 3.7+
* `requests` library<br>`pip install requests`
* `playwright` library (only for the Playwright script)<br>`pip install playwright && playwright install chromium`
* A [Scrape.do API token](https://dashboard.scrape.do/signup) (free 1000 credits/month)

## How to Use: `scrapeAIOverviewSerpApi.py`

1. Set your query:

   ```python
   token = "<your_token>"
   query = "how does photosynthesis work"
   ```

2. Run: `python scrapeAIOverviewSerpApi.py`

Output → `ai-overview-serp-api-results.json`:

```yaml
query: "how does photosynthesis work"
ai_overview_found: true
state: complete
text_blocks:
  - type: paragraph
    text: "Photosynthesis is the process by which plants..."
  - type: list_item
    text: "Light-dependent reactions occur in the thylakoid..."
references:
  - title: "Photosynthesis - Khan Academy"
    url: "https://..."
    source: "khanacademy.org"
```

## How to Use: `scrapeAIOverviewPlaywright.py`

1. Set your query:

   ```python
   token = "<your_token>"
   query = "how does photosynthesis work"
   ```

2. Run: `python scrapeAIOverviewPlaywright.py`

Output → `ai-overview-results.json` with text blocks and references. Also saves `response-rendered.html` for debugging.

## How It Works

### The Deferred State Problem

AI Overviews don't always arrive in the initial response. Google returns them in one of three states:

- **Complete**: Full content inline — parse it and you're done
- **Deferred**: Google says "I'll have it ready in a moment" and gives you a `session_key`. You get ~60 seconds to call a follow-up endpoint before the key expires. It's single-use.
- **Absent**: No AI Overview for this query (common for navigational or ambiguous searches)

The SERP API script detects the deferred state and automatically makes the follow-up call. The Playwright script sidesteps the problem entirely — the browser waits for the AI Overview to render in the DOM.

### SERP API Approach

Calls `/plugin/google/search` which returns structured JSON. For deferred responses, follows up with `/plugin/google/search/ai-overview` using the session key. Text blocks come in a nested structure (paragraphs with inline lists), so the script flattens them into a simple `[{type, text}]` array. The deferred follow-up costs 5 additional credits.

### Playwright Approach

Routes Chromium through Scrape.do's residential proxy (`proxy.scrape.do:8080`, username = token, password = `super=true`). The script:

1. Tries a standard Google URL (`hl=en&gl=us`)
2. If no AI Overview detected, retries with a US geolocation parameter (`uule`)
3. Waits for `networkidle` + 8 seconds for the content to render
4. Looks for the "AI Overview" heading, walks up to the `Kevs9` container
5. Extracts text from `div.Y3BBE` (with fallbacks to `jsname="KFl8ub"` and leaf-node text)
6. Extracts references from `li.jydCyd` (with fallback to `#Odp5De` parent)

All of these selectors can change — the script has multiple fallback layers built in.

## Watch Out For

- **Not all queries trigger AI Overviews**: Informational queries ("how does X work", "what is Y") are the most reliable triggers. Navigational queries ("facebook login") almost never get one.
- **Session key expiry**: Deferred keys expire in ~60 seconds and are single-use. The SERP API script handles this automatically, but don't add long delays between the initial request and the follow-up if you modify the code.
- **DOM class name churn**: Google changes AI Overview selectors regularly. The Playwright script has three layers of fallback selectors, but may need updating if Google redesigns the component.
- **Geographic variance**: AI Overviews appear more frequently for US-based searches. The Playwright script's `uule` fallback helps, but some queries only trigger AIO from specific regions.

## Output Files

| Script | Output | Contents |
|--------|--------|----------|
| `scrapeAIOverviewSerpApi.py` | `ai-overview-serp-api-results.json` | query, state, text_blocks (type + text), references (title, url, source) |
| `scrapeAIOverviewPlaywright.py` | `ai-overview-results.json` | query, text_blocks (type + text), references (title, url, snippet) |
| `scrapeAIOverviewPlaywright.py` | `response-rendered.html` | debug: full rendered page HTML |

---

**Scrape.do** provides the residential proxies and SERP API that make AI Overview extraction reliable. [Get your free API token](https://dashboard.scrape.do/signup) (1000 credits/month).
