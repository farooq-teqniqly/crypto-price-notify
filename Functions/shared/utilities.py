import requests
import sys
from bs4 import BeautifulSoup
from price_parser import Price


def make_soup(url):
    response = requests.get(url)
    return BeautifulSoup(response.text, 'html.parser')


def get_price(soup, currency):
    all_links_soup = [a for a in soup.find_all('a') if a['href'].endswith(currency)]
    price_soup = all_links_soup[0].parent.parent.next_sibling
    price_str = price_soup.find('div').text
    return Price.fromstring(price_str, '$').amount_float


def main(args):
    soup = make_soup('https://crypto.com/price')

    pass


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
