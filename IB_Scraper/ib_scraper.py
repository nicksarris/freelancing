__author__ = 'Nick Sarris (ngs5st)'

import requests
import pandas as pd
from bs4 import BeautifulSoup

def scraper(url):

    scraper = requests.session()
    response = scraper.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    data = list(soup.find_all('td')[44:])

    ib_symbols = []
    for i in range(0, len(data), 4):
        symbol = str(data[i])
        symbol = symbol.replace('<td>','')
        symbol = symbol.replace('</td>','')
        list.append(ib_symbols, symbol)

    descriptions = []
    for i in range(1, len(data), 4):
        desc = str(data[i]).split('>')[2]
        desc = desc.replace('</a','')
        list.append(descriptions, desc)

    symbols = []
    for i in range(2, len(data), 4):
        symbol = str(data[i])
        symbol = symbol.replace('<td>','')
        symbol = symbol.replace('</td>','')
        list.append(symbols, symbol)

    currencies = []
    for i in range(3, len(data), 4):
        currency = str(data[i])
        currency = currency.replace('<td>','')
        currency = currency.replace('</td>','')
        list.append(currencies, currency)

    return ib_symbols, descriptions, symbols, currencies

def main():

    url = 'https://www.interactivebrokers.com/en/index.php?f=2222&exch=globex&showcategories=FUTGRP'
    ib_symbols, descriptions, symbols, currencies = scraper(url)

    final_data = []
    for a,b,c,d in zip(ib_symbols, descriptions, symbols, currencies):
        list.append(final_data, [a,b,c,d])

    columns = ['IB_Symbol','Description','Symbol','Currency']
    ibroker_df = pd.DataFrame(final_data, columns=columns)
    ibroker_df.to_csv('final_data.csv', index=False)

if __name__ == '__main__':
    main()