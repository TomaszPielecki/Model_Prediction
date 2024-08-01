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
    data[f'EMA_{ma_1}'] = data['Adj Close'].rolling(window=ma_1).mean()
    data[f'EMA_{ma_2}'] = data['Adj Close'].rolling(window=ma_2).mean()

    buy_signal = []
    sell_signal = []
    trigger = 0

    for x in range(len(data)):
        if data[f'EMA_{ma_1}'].iloc[x] > data[f'EMA_{ma_2}'].iloc[x] and trigger != 1:
            buy_signal.append(data['Adj Close'].iloc[x])
            sell_signal.append(float('nan'))
            trigger = 1
        elif data[f'EMA_{ma_1}'].iloc[x] < data[f'EMA_{ma_2}'].iloc[x] and trigger != -1:
            buy_signal.append(float('nan'))
            sell_signal.append(data['Adj Close'].iloc[x])
            trigger = -1
        else:
            buy_signal.append(float('nan'))
            sell_signal.append(float('nan'))

    data['Buy Signal'] = buy_signal
    data['Sell Signal'] = sell_signal

    return data


def identify_support_resistance(data, window=50):
    data['Support'] = data['Adj Close'].rolling(window=window, center=True).min()
    data['Resistance'] = data['Adj Close'].rolling(window=window, center=True).max()
    return data


def plot_data(data, crypto):
    plt.figure(figsize=(14, 7))
    plt.plot(data['Adj Close'], label=f"Actual Price {crypto}", alpha=0.5)
    plt.plot(data[f'EMA_{ma_1}'], label=f'EMA_{ma_1}', color='orange', linestyle='--')
    plt.plot(data[f'EMA_{ma_2}'], label=f'EMA_{ma_2}', color='pink', linestyle='--')
    plt.plot(data['Support'], label='Support', color='blue', linestyle='--')
    plt.plot(data['Resistance'], label='Resistance', color='red', linestyle='--')
    plt.scatter(data.index, data['Buy Signal'], label="Buy Signal", marker="^", color="#00ff00", lw=3)
    plt.scatter(data.index, data['Sell Signal'], label="Sell Signal", marker="v", color="#ff0000", lw=3)

    plt.legend(loc='upper left')
    plt.title(f"{crypto} Price with EMA, Support and Resistance")
    plt.show()


def plot_elliott_wave(data, points):
    plt.figure(figsize=(14, 7))
    plt.plot(data['Adj Close'], label='Price', alpha=0.5)
    wave_points = data['Adj Close'].iloc[points]
    plt.plot(wave_points, label='Elliott Wave', marker='o', linestyle='-', color='purple')

    for i, txt in enumerate(['Wave 1', 'Wave 2', 'Wave 3', 'Wave 4', 'Wave 5']):
        plt.annotate(txt, (wave_points.index[i], wave_points.iloc[i]), textcoords="offset points", xytext=(0, 10),
                     ha='center')

    plt.legend(loc='upper left')
    plt.title("Elliott Wave")
    plt.show()


def main():
    crypto, against = get_user_input()
    data = download_data(crypto, against)
    data = calculate_signals(data)
    data = identify_support_resistance(data)

    plot_data(data, crypto)

    # Przykładowe punkty dla fal Elliotta (należy je dostosować na podstawie analizy technicznej)
    elliott_points = [20, 50, 80, 110, 140]
    plot_elliott_wave(data, elliott_points)


if __name__ == "__main__":
    main()
