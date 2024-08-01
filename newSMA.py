# -*- coding: utf-8 -*-
import datetime as dt

import matplotlib.pyplot as plt
import yfinance as yf

plt.style.use('default')
ma_1 = 12
ma_2 = 50


def get_user_input():
    crypto = input("Enter cryptocurrency symbol e.g. BTC, ETH, LTC: ").upper()
    against = input("Enter currency symbol e.g. USD, EUR: ").upper()
    return crypto, against


def download_data(crypto, against):
    start = dt.datetime.now() - dt.timedelta(days=365)
    end = dt.datetime.now()
    data = yf.download(tickers=f'{crypto}-{against}', start=start, end=end)
    return data


def calculate_signals(data):
    data[f'SMA_{ma_1}'] = data['Close'].rolling(window=ma_1).mean()
    data[f'SMA_{ma_2}'] = data['Close'].rolling(window=ma_2).mean()

    buy_signal = []
    sell_signal = []
    trigger = 0

    for x in range(len(data)):
        if data[f'SMA_{ma_1}'].iloc[x] > data[f'SMA_{ma_2}'].iloc[x] and trigger != 1:
            buy_signal.append(data['Close'].iloc[x])
            sell_signal.append(float('nan'))
            trigger = 1
        elif data[f'SMA_{ma_1}'].iloc[x] < data[f'SMA_{ma_2}'].iloc[x] and trigger != -1:
            buy_signal.append(float('nan'))
            sell_signal.append(data['Close'].iloc[x])
            trigger = -1
        else:
            buy_signal.append(float('nan'))
            sell_signal.append(float('nan'))

    data['Buy Signal'] = buy_signal
    data['Sell Signal'] = sell_signal

    return data


def plot_data(data, crypto):
    plt.figure(figsize=(14, 7))
    plt.plot(data['Close'], label=f"Actual Price {crypto}", alpha=0.5)
    plt.plot(data[f'SMA_{ma_1}'], label=f'SMA_{ma_1}', color='orange', linestyle='--')
    plt.plot(data[f'SMA_{ma_2}'], label=f'SMA_{ma_2}', color='pink', linestyle='--')
    plt.scatter(data.index, data['Buy Signal'], label="Buy Signal", marker="^", color="#00ff00", lw=3)
    plt.scatter(data.index, data['Sell Signal'], label="Sell Signal", marker="v", color="#ff0000", lw=3)

    plt.legend(loc='upper left')
    plt.show()


def main():
    crypto, against = get_user_input()
    data = download_data(crypto, against)
    data = calculate_signals(data)
    plot_data(data, crypto)


if __name__ == "__main__":
    main()
