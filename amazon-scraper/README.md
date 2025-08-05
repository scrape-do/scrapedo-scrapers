# Amazon Scraper

This scraper uses __Python 3.8__, __Python Requests__, and __Beautiful Soup__ to scrape product information from Amazon.com.

 __[Scrape.do](https://scrape.do/)__'s web scraping API is used to bypass Amazon's anti-bot protections and interact with the website.
  

[Find the full tutorial here.](https://scrape.do/blog/amazon-scraping/)

  
The scraping code consists of 3 files which is used for 3 different tasks.

- single.py // To scrape key product data from product pages.

- sizes.py // To scrape product data from products that have different prices for different sizes.

- categories.py // To scrape Amazon search results and categories, which work the same way.

  

## Setup and Use


1. Ensure you have the latest version of __Python__ (3.8 at the time of development) on your system.

2. Clone and install Python environment:

```shell

$ git clone https://github.com/scrape-do/scrapedo-scrapers-temp.git

```

3. [Register for Scrape.do's free plan](https://dashboard.scrape.do/signup) (1000 monthly credits) and generate your API token. Replace `<your_token>` with your generated API token on all three files.

4. Run example scrape:

```shell

$ python single.py

```


If you run into any issues with this library, it might be a good idea to use the original environment that this code was written in using [poetry Python package manager](https://python-poetry.org/docs/#installation), which is defined in the "_poetry.toml_" document.