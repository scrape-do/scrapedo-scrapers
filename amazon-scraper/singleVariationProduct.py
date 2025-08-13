import requests
from bs4 import BeautifulSoup

# Our token provided by 'Scrape.do'
token = "<your-token>"

# Amazon product urls
targetUrls = ["https://us.amazon.com/Calvin-Klein-Classics-Multipack-T-Shirts/dp/B0DSJYYC7Z/",
              "https://us.amazon.com/Urmust-Ergonomic-Adjustable-Ultrabook-Compatible/dp/B081YXWDTQ/",
              "https://us.amazon.com/Ergonomic-Compatible-Notebook-Soundance-LS1/dp/B07D74DT3B/"]

for targetUrl in targetUrls:
    # Use scrape.do to get contents using your token
    apiUrl = "http://api.scrape.do?token={}&url={}".format(token, targetUrl)
    response = requests.request("GET", apiUrl)

    # Parse the request using BS
    soup = BeautifulSoup(response.text, "html.parser")

    name = soup.find(id="productTitle").text.strip()
    
    # Extract ASIN from URL
    asin = targetUrl.split("/dp/")[1].split("/")[0].split("?")[0]
    
    # Extract price
    if soup.find("div", id="outOfStockBuyBox_feature_div"):
        price = "Out of Stock"
    else:
        whole = soup.find(class_="a-price-whole")
        fraction = soup.find(class_="a-price-fraction")
        price = f"${whole.text}{fraction.text}"

    image = soup.find("img", {"id": "landingImage"})["src"]
    rating = soup.find(class_="AverageCustomerReviews").text.strip().split(" out of")[0]
    with open("outpu2t.csv", "a") as f:
        f.write('"' + asin + '", "' + name + '", "' + price + '", "' + image + '","' + rating + '" \n')