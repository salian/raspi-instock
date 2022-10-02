import time
from datetime import datetime
import cloudscraper
from bs4 import BeautifulSoup
from mac_notifications import client
from functools import partial
import pprint
import webbrowser
from random import randrange
from requests.exceptions import ConnectionError

# ROBU_URL = 'https://robu.in/?s=raspberry+pi+kit&product_cat=raspberry-pi-kit&post_type=product'
# ROBU_URL = 'https://robu.in/?s=raspberry+pi&product_cat=official-boards-and-accessories&post_type=product'

ROBU_URL_LIST = [
    'https://robu.in/?s=raspberry+pi&product_cat=official-boards-and-accessories&post_type=product',
    'https://robu.in/?s=raspberry+pi+kit&product_cat=raspberry-pi-kit&post_type=product'
]

ROBOCRAZE_URL_LIST = [
    'https://robocraze.com/collections/boards-raspberry-pi'
]

ROBOMART_URL_LIST = [
    'https://www.robomart.com/raspberry-pi-india/raspberry-pi-boards',
    'https://www.robomart.com/raspberry-pi-india/raspberry-pi-starter-kits'
]

def fetch_results_robocraze(url: str) -> list[dict[str, float | bool]]:
    scraper = cloudscraper.create_scraper()
    
    try:
        page_html = scraper.get(url).text
    except ConnectionError:
        page_html = ''
    
    soup = BeautifulSoup(page_html, 'html.parser')
    
    products = soup.find_all('li', {'class': 'grid__item'})
    
    product_status_list = []
        
    for product in products:
        product_status = {}
        product_status['name'] = product.find('div', {'class': 'product-card__title'}).string
        product_status['sku'] = product.find_all('p', 'data-product-id'==True)[0]['data-product-id']
        product_status['price'] = float(product.find('span', {'class': 'price-item'}).text.replace('\n','').split(' ')[-1])

        if product.find('span', {'class':'atc_text'}):
            product_status['in_stock'] = True
        else:
            product_status['in_stock'] = False
        
        product_status_list.append(product_status)
        
    return product_status_list

def fetch_page(url: str) -> list[dict[str, float | bool]]:
    scraper = cloudscraper.create_scraper()
    try:
        page_html = scraper.get(url).text
    except ConnectionError:
        page_html = ''  # Connection Error, returning blank page
        # Perhaps notify here?
    soup = BeautifulSoup(page_html, 'html.parser')
    products = soup.find_all('li', {'class': 'product'})
    # print(soup.get_text())
    product_status_list = []
    for product in products:
        product_status = {}
        if product.find('a', {'class': 'add_to_cart_button'}):
            in_stock = True
        else:
            in_stock = False
        # print(product.h2.string, in_stock)

        product_status['name'] = product.h2.string
        product_status['sku'] = product.find('div', {'class': 'product-sku'}).string[5:]
        amount_tag = product.find('span', {'class': 'amount'}).bdi
        amount_tag.span.decompose()  # remove the extra span for currency symbol
        product_status['amount'] = float(amount_tag.string.strip().replace(",", ""))
        product_status['in_stock'] = in_stock
        product_status_list.append(product_status)
    return product_status_list

def fetch_results_robomart(url: str) -> list[dict[str, float | bool]]:
    scraper = cloudscraper.create_scraper()
    
    try:
        page_html = scraper.get(url).text
    except ConnectionError:
        page_html = ''
    
    soup = BeautifulSoup(page_html, 'html.parser')
    
    products = soup.find_all('li', {'class': 'product-layout'})
    
    product_status_list = []
        
    for product in products:
        product_status = {}
        product_status['name'] = product.find('div', {'class': 'item-title'}).text
        product_status['sku'] = product.find('strong').text.split(': ')[-1]
        product_status['price'] = float(product.find('span', {'class': 'price'}).text.replace(',','').split('.')[0])

        if product.find('div', {'class':'in-stock'}):
            product_status['in_stock'] = True
        else:
            product_status['in_stock'] = False

        product_status_list.append(product_status)

    return product_status_list

def open_url(url: str) -> None:
    webbrowser.open(url, new=0, autoraise=True)


def monitor_robu():
    for ROBU_URL in ROBU_URL_LIST:
        # fetch search result
        search_results = fetch_page(ROBU_URL)

        # uncomment for printing all search results
        pprint.pprint(search_results)

        # have a list of SKUs to track
        # interesting_skus = ['757102', '471149', '471148', '471147', '169868', '1124637', '10973', '785898', '57418', '84661']

        interesting_skus = ['757102', '471149', '471148', '471147', '169868', '1124637', '10973', '785898', '57418',
                            '84661', '1359500']

        blacklisted_skus = ['51590', '1363865', '722207', ]   # add to this list if you have unwanted SKUs triggering the alert

        notify_product_list = []
        for product in search_results:
            # Put your matching rules here

            # Match the SKU from a preset list
            if product['sku'] in interesting_skus and product['in_stock']:
                notify_product_list.append(product)

            # Match part of the product name
            if 'Raspberry Pi 4' in product['name'] and product['in_stock'] and product['sku'] not in blacklisted_skus:
                notify_product_list.append(product)

            # Match part of the product name
            if 'Raspberry Pi Zero' in product['name'] and product['in_stock'] and product['sku'] not in blacklisted_skus:
                notify_product_list.append(product)

            # # Match product price
            # if product['amount'] > 4500 and product['in_stock']:
            #     notify_product_list.append(product)

            # ... add any other conditions here

        # remove duplicates where multiple rules have matched above
        notify_product_list_unique = []
        [notify_product_list_unique.append(x) for x in notify_product_list if x not in notify_product_list_unique]
        date_format = '%Y-%m-%d %H:%M:%S'
        # log_format = '%(asctime)s|%(levelname)8s| {%(module)s} [%(funcName)s] <%(processName)s> %(message)s'

        if len(notify_product_list_unique) > 0:
            # Open Robu.in in a browser
            open_url(ROBU_URL)
            datetime.now().strftime(date_format)
            print(datetime.now().strftime(date_format), 'Notify!', notify_product_list_unique, ROBU_URL)
            product_string = ", ".join([product['name'] for product in notify_product_list_unique])
            client.create_notification(
                title="Item back in stock at Robu",
                subtitle=product_string,
                action_button_str="Open Robu.in",
                action_callback=partial(open_url, url=ROBU_URL),
            )
            time.sleep(30)
            client.stop_listening_for_callbacks()
        else:
            out_of_stock_count = len(search_results)
            print(datetime.now().strftime(date_format), "Nothing in stock.", out_of_stock_count, "out of stock.")


if __name__ == '__main__':
    # randomize script start time to avoid extra load on server
    time.sleep(randrange(10))
    monitor_robu()
