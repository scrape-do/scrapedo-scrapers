import requests
from bs4 import BeautifulSoup

# Our token provided by 'Scrape.do'
token = "<your-token>"

# Amazon product urls
targetUrls = ["https://us.amazon.com/Amazon-Basics-Portable-Adjustable-Notebook/dp/B0BLRJ4R8F/",
              "https://us.amazon.com/Urmust-Ergonomic-Adjustable-Ultrabook-Compatible/dp/B081YXWDTQ/",
              "https://us.amazon.com/Ergonomic-Compatible-Notebook-Soundance-LS1/dp/B07D74DT3B/"]

for targetUrl in targetUrls:
    # Use scrape.do to get contents using your token
    apiUrl = "http://api.scrape.do?token={}&url={}".format(token, targetUrl)
    response = requests.request("GET", apiUrl)

    # Parse the request using BS
    soup = BeautifulSoup(response.text, "html.parser")

    name = soup.find(id="productTitle").text.strip()
    price = soup.find(class_="priceToPay").text.strip()
    image = soup.find("img", {"id": "landingImage"})["src"]
    rating = soup.find(class_="AverageCustomerReviews").text.strip().split(" out of")[0]
    with open("output.csv", "a") as f:
        f.write('"' + name + '", "' + price + '", "' + image + '","' + rating + '" \n')


