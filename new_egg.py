from bs4 import BeautifulSoup
import requests
import sqlite3

db = 'SSD_PRODUCTS.sqlite'
conn = sqlite3.connect(db)
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS ssd_products
              (product_id INTEGER PRIMARY KEY, name TEXT, price REAL, shipping TEXT, saving TEXT)''')

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
    try:
        # Product description
        product_title = container.a.img['title']
        # Product Price
        price = container.find_all('li', {'class': 'price-current'})
        price_strong = price[0].strong.text
        price_sup = price[0].sup.text
        product_price = price_strong + price_sup

        # Product shipping information
        shipping = container.find_all('li', {'class': 'price-ship'})
        product_shipping = shipping[0].text.strip()
        # If product has any special deals currently
        save = soup.find_all('li', {'class': 'price-save'})
        if save[0].strong is None:
            product_saving = 'No savings currently'
        else:
            product_saving = save[0].strong.text

        cur.execute('INSERT INTO ssd_products VALUES (?, ?, ?, ?, ?)', (product_title, product_price, product_shipping,
                    product_saving))
        conn.commit()
        conn.close()
        print('Brand: ', product_title)
        print('Price: ', product_price)
        print('Shipping: ', product_shipping)
        print('Savings: ', product_saving)

    except AttributeError:
        pass
