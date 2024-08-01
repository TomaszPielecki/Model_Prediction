# # -*- coding: utf-8 -*-
# import pandas as pd
# import requests
#
#
# # Pobranie danych z Api 100 kryptowalut malejąco-desc
# def coin_gecko():
#     url = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc'
#     response = requests.get(url)
#     if response.status_code == 200:
#         info = response.json()
#         # Listy
#         a = info[0]['name'], info[0]['current_price'], info[0]['high_24h'], info[0]['low_24h'],
#         b = info[1]['name'], info[1]['current_price'], info[1]['high_24h'], info[1]['low_24h'],
#         c = info[2]['name'], info[2]['current_price'], info[2]['high_24h'], info[2]['low_24h'],
#         d = info[3]['name'], info[3]['current_price'], info[3]['high_24h'], info[3]['low_24h'],
#         e = info[4]['name'], info[4]['current_price'], info[4]['high_24h'], info[4]['low_24h'],
#         f = info[5]['name'], info[5]['current_price'], info[5]['high_24h'], info[5]['low_24h'],
#         g = info[6]['name'], info[6]['current_price'], info[6]['high_24h'], info[6]['low_24h'],
#         h = info[7]['name'], info[7]['current_price'], info[7]['high_24h'], info[7]['low_24h'],
#         i = info[8]['name'], info[8]['current_price'], info[8]['high_24h'], info[8]['low_24h'],
#         j = info[9]['name'], info[9]['current_price'], info[9]['high_24h'], info[9]['low_24h'],
#         k = info[10]['name'], info[10]['current_price'], info[10]['high_24h'], info[10]['low_24h'],
#         m = info[11]['name'], info[11]['current_price'], info[11]['high_24h'], info[11]['low_24h'],
#         # Zamiana Listy w tuple, zwiększenie wydajności wyciągania danych
#         tup = (a, b, c, d, e, f, g, h, i, j, k, m)
#         data = tup
#         # Wykres z Server's coingecko w walucie PLN z ostatnich 24 godzin, Top 12 Walut
#         df = pd.DataFrame(data, columns=['Name', 'Price_Now', 'Max_Price_24h', 'Low_Price_24h'])
#         print(df)
#
#
# coin_gecko()

# -*- coding: utf-8 -*-
import pandas as pd
import requests


# Pobranie danych z Api 100 kryptowalut malejąco-desc
def coin_gecko():
    url = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc'
    response = requests.get(url)
    if response.status_code == 200:
        info = response.json()

        # Tworzenie listy z danymi dla każdego krypto
        data = [
            (crypto['name'], crypto['current_price'], crypto['high_24h'], crypto['low_24h'])
            for crypto in info[:20]
        ]

        # Tworzenie DataFrame z listy
        df = pd.DataFrame(data, columns=['Name', 'Price_Now', 'Max_Price_24h', 'Low_Price_24h'])
        print(df)
    else:
        print(f"Failed to fetch data: {response.status_code}")


coin_gecko()
