# -*- coding: utf-8 -*-
import datetime as dt

import matplotlib.pyplot as plt
import yfinance as yf


# Pobierz dane
def download_data(ticker):
    start = dt.datetime.now() - dt.timedelta(days=365)
    end = dt.datetime.now()
    data = yf.download(ticker, start=start, end=end)
    return data


# Oblicz Wstęgi Bollingera
def bollinger_bands(data, window=20, no_of_std=2):
    data['SMA'] = data['Adj Close'].rolling(window).mean()
    data['Bollinger_Up'] = data['SMA'] + (data['Adj Close'].rolling(window).std() * no_of_std)
    data['Bollinger_Down'] = data['SMA'] - (data['Adj Close'].rolling(window).std() * no_of_std)
    return data


# Oblicz poziomy Fibonacciego
def fibonacci_levels(data):
    max_price = data['Adj Close'].max()
    min_price = data['Adj Close'].min()
    diff = max_price - min_price
    levels = {
        'Fib_0': max_price,
        'Fib_0.236': max_price - 0.236 * diff,
        'Fib_0.382': max_price - 0.382 * diff,
        'Fib_0.5': max_price - 0.5 * diff,
        'Fib_0.618': max_price - 0.618 * diff,
        'Fib_0.764': max_price - 0.764 * diff,
        'Fib_1': min_price
    }
    return levels


# Rysuj dane
def plot_data(data, ticker, levels):
    plt.figure(figsize=(14, 7))
    plt.plot(data['Adj Close'], label=f"Price {ticker}", alpha=0.5)
    plt.plot(data['Bollinger_Up'], label='Bollinger Up', linestyle='--', color='red')
    plt.plot(data['Bollinger_Down'], label='Bollinger Down', linestyle='--', color='green')
    plt.plot(data['SMA'], label='SMA', linestyle='-', color='blue')

    for level in levels:
        plt.axhline(y=levels[level], color='gray', linestyle='--')
        plt.text(data.index[-1], levels[level], level, va='center')

    plt.legend(loc='best')
    plt.title(f'{ticker} - Bollinger Bands and Fibonacci Levels')
    plt.show()


# Main function
def main():
    ticker = input("Enter cryptocurrency symbol (e.g., BTC-USD, ETH-USD): ").upper()
    data = download_data(ticker)
    data = bollinger_bands(data)
    fib_levels = fibonacci_levels(data)
    plot_data(data, ticker, fib_levels)


if __name__ == "__main__":
    main()
