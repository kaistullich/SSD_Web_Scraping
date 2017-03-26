import csv
import sqlite3

import requests
from bs4 import BeautifulSoup

db = 'SSD_PRODUCTS.sqlite'
conn = sqlite3.connect(db)
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS ssd_products
              (product_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                price REAL,
                shipping TEXT,
                saving TEXT)
            ''')


def scraping(bs):
    # Containers that contain the items inside (outermost HTML wrapper)
    containers = bs.find_all("div", {"class": "item-container"})

    # Lists where information will be stored
    titles = []
    prices = []
    shipping = []
    savings = []

    # Loop through all containers and find relevant information
    for container in containers:
        # Product description
        product_title = container.a.img['title']
        titles.append(product_title)

        # Product Price
        price = container.find_all('li', {'class': 'price-current'})
        price_strong = price[0].strong.text
        price_sup = price[0].sup.text
        product_price = price_strong + price_sup
        prices.append(product_price)

        # Product shipping information
        ship = container.find_all('li', {'class': 'price-ship'})
        product_shipping = ship[0].text.strip()
        shipping.append(product_shipping)

        # If product has any special deals currently
        save = container.find_all('li', {'class': 'price-save'})
        # If a product does not have any special deals
        if save[0].strong is None:
            product_saving = 'No savings currently'
            savings.append(product_saving)
        else:
            # Product has a special deal
            product_saving = save[0].strong.text
            savings.append(product_saving)

    return titles, prices, shipping, savings

if __name__ == '__main__':
    # New Egg Internal SSD url
    url = 'https://www.newegg.com/Internal-SSDs/SubCategory/ID-636'
    # Send request to website
    web_page = requests.get(url)
    # Show HTML (text)
    web_page_html = web_page.text
    # Create BeautifulSoup object
    soup = BeautifulSoup(web_page_html, 'lxml')
    # All products are stored in this object
    products = scraping(soup)
    # Creating .CSV file
    with open('ssd_products.csv', 'w') as f:
        file = csv.writer(f)
        file.writerows(products)
    # Inserting into DB
    cur.executemany('INSERT INTO ssd_products VALUES (?, ?, ?, ?, ?)', products)
    conn.commit()
    # Close connection to DB
    conn.close()
