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

ROBU_URL = 'https://robu.in/?s=raspberry+pi&product_cat=official-boards-and-accessories&post_type=product'

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


def open_url(url: str) -> None:
    webbrowser.open(url, new=0, autoraise=True)


def monitor_robu():

    # fetch search result
    search_results = fetch_page(ROBU_URL)

    # uncomment for printing all search results
    pprint.pprint(search_results)

    # have a list of SKUs to track
    interesting_skus = ['757102', '471149', '471148', '471147', '169868', '1124637', '10973', '785898', '57418', '84661']

    notify_product_list = []
    for product in search_results:
        # Put your matching rules here

        # Match the SKU from a preset list
        if product['sku'] in interesting_skus and product['in_stock']:
            notify_product_list.append(product)


    # remove duplicates where multiple rules have matched above
    notify_product_list_unique = []
    [notify_product_list_unique.append(x) for x in notify_product_list if x not in notify_product_list_unique]
    date_format = '%Y-%m-%d %H:%M:%S'
    # log_format = '%(asctime)s|%(levelname)8s| {%(module)s} [%(funcName)s] <%(processName)s> %(message)s'

    if len(notify_product_list_unique) > 0:
        # Open Robu.in in a browser
        open_url(ROBU_URL)
    else:
        out_of_stock_count = len(search_results)
        print(datetime.now().strftime(date_format), "Nothing in stock.", out_of_stock_count, "out of stock.")


if __name__ == '__main__':
    # randomize script start time to avoid extra load on server
    time.sleep(randrange(10))
    monitor_robu()
