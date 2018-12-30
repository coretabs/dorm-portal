"""
import requests
from bs4 import BeautifulSoup


def get_rates():
    request = requests.get('http://www.koopbank.com/inmotion/doviz/mobil.php?lang=tr-tr')
    soup = BeautifulSoup(request.text, 'html.parser')
    exchanges = soup.find(id='pagemain').find_all('div', {'class': 'mt2'})
    for exchange in exchanges:
        print(exchange.span)
"""
from djmoney.contrib.exchange.backends.base import SimpleExchangeBackend


class ExchangeRatesIOBackend(SimpleExchangeBackend):
    name = 'exchangeratesapi.io'
    url = 'https://api.exchangeratesapi.io/latest?base=USD'

    def __init__(self, url='https://api.exchangeratesapi.io/latest?base=USD'):
        self.url = url
