from bs4 import BeautifulSoup
import requests

# New Egg Internal SSD url
url = 'https://www.newegg.com/Internal-SSDs/SubCategory/ID-636'
# Send request to website
web_page = requests.get(url)
# Show HTML (text)
web_page_html = web_page.text
# Create BeautifulSoup object
soup = BeautifulSoup(web_page_html, 'lxml')

# Containers that contain the items inside (outermost HTML wrapper)
containers = soup.find_all("div", {"class": "item-container"})

# Loop through all containers and find relevant information
for container in containers:
    product_title = container.a.img['title']

    price = container.find_all('li', {'class': 'price-current'})
    try:
        product_strong = price[0].strong.text
        product_sup = price[0].sup.text
        product_price = product_strong + product_sup
    except AttributeError:
        pass
    

