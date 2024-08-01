# -*- coding: utf-8 -*-
import datetime as dt

import matplotlib.pyplot as plt
import yfinance as yf


def get_user_input():
    while True:
        try:
            crypto = input("Enter cryptocurrency symbol e.g. BTC, ETH, LTC: ").upper()
            if any(char.isdigit() for char in crypto):
                raise ValueError("Entered cryptocurrency name is invalid.")
            against = input("Enter currency symbol e.g. USD, EUR: ").upper()
            if any(char.isdigit() for char in against):
                raise ValueError("Entered currency name is invalid.")
            return crypto, against
        except ValueError as ve:
            print(f"Error: {ve}. Please try again.")


def download_data(crypto, against, start, end):
    return yf.download(tickers=f'{crypto}-{against}', start=start, end=end)


def calculate_macd(data, short_window, long_window, signal_window):
    data['EMA_12'] = data['Close'].ewm(span=short_window, adjust=False).mean()
    data['EMA_26'] = data['Close'].ewm(span=long_window, adjust=False).mean()
    data['MACD'] = data['EMA_12'] - data['EMA_26']
    data['Signal'] = data['MACD'].ewm(span=signal_window, adjust=False).mean()
    return data


def generate_signals(data):
    buy_signal = []
    sell_signal = []
    macd_cross_signal = []

    for i in range(len(data)):
        if data['MACD'].iloc[i] > data['Signal'].iloc[i]:
            buy_signal.append(data['Close'].iloc[i])
            sell_signal.append(float('nan'))
        elif data['MACD'].iloc[i] < data['Signal'].iloc[i]:
            buy_signal.append(float('nan'))
            sell_signal.append(data['Close'].iloc[i])
        else:
            buy_signal.append(float('nan'))
            sell_signal.append(float('nan'))

        # Add detailed MACD cross signal
        if i % 10 == 0:
            macd_cross_signal.append(data['MACD'].iloc[i])
        else:
            macd_cross_signal.append(float('nan'))

    data['Buy Signal'] = buy_signal
    data['Sell Signal'] = sell_signal
    data['MACD Cross Signal'] = macd_cross_signal
    return data


def plot_data(data, crypto):
    plt.figure(figsize=(14, 7))
    plt.plot(data['Close'], label=f"Actual Price {crypto}", alpha=0.5, color='blue')
    plt.plot(data['MACD'], label='MACD (12/26)', color='orange')
    plt.plot(data['Signal'], label='Signal (9)', color='green')
    plt.scatter(data.index, data['Buy Signal'], label="Buy Signal", marker="^", color="green", lw=3)
    plt.scatter(data.index, data['Sell Signal'], label="Sell Signal", marker="v", color="red", lw=3)
    plt.scatter(data.index, data['MACD Cross Signal'], label="MACD Cross Signal", marker="o", color="purple", lw=1)

    plt.legend(loc='upper left')
    plt.show()


def main():
    crypto, against = get_user_input()
    start = dt.datetime.now() - dt.timedelta(days=365)
    end = dt.datetime.now()
    data = download_data(crypto, against, start, end)

    data = calculate_macd(data, short_window=12, long_window=26, signal_window=9)
    data = generate_signals(data)

    plot_data(data, crypto)


if __name__ == "__main__":
    main()
