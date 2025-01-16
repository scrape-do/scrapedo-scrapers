# G2 Scraper

This scraper uses __Python 3.8__, __Python Requests__, and __Beautiful Soup__ to scrape product information from G2.com.

 __[Scrape.do](https://scrape.do/)__'s web scraping API is used to bypass G2's anti-bot protections and interact with the website.
  

[Find the full tutorial here.]()

  
The scraping code consists of 3 different files which is used for 3 different tasks.

- main.py // To scrape key company/product data from company pages.

- reviews.py // To scrape reviews of a company/product.

- categories.py // To scrape G2 search results and categories.

  

## Setup and Use


1. Ensure you have the latest version of __Python__ (3.8 at the time of development) on your system.

2. Clone and install Python environment:

```shell

$ git clone https://github.com/scrape-do/scrapedo-scrapers-temp.git

```

3. [Register for Scrape.do's free plan](https://dashboard.scrape.do/signup) (1000 monthly credits) and generate your API token. Replace `<your_token>` with your generated API token on all three files.

4. Run example scrape:

```shell

$ python main.py

```


If you run into any issues with this library, it might be a good idea to use the original environment that this code was written in using [poetry Python package manager](https://python-poetry.org/docs/#installation), which is defined in the "_poetry.toml_" document.