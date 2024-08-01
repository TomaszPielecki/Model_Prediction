import datetime as dt
import os
import matplotlib
import yfinance
import neuralprophet
import pandas

import matplotlib.pyplot as plt
import yfinance as yf
from neuralprophet import NeuralProphet

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

# Simple cache for downloaded data
cache = {}


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


def download_data(crypto, against, start_date, end_date):
    key = f"{crypto}-{against}-{start_date}-{end_date}"
    if key in cache:
        return cache[key]
    data = yf.download(f'{crypto}-{against}', start=start_date, end=end_date, interval='1d')
    cache[key] = data
    return data


def prepare_data(data):
    stocks = data[['Close']].reset_index()
    stocks.columns = ['ds', 'y']
    return stocks


def fit_model(stocks):
    model = NeuralProphet()
    model.fit(stocks, freq='D')
    return model


def make_predictions(model, stocks):
    future = model.make_future_dataframe(stocks, periods=300)
    forecast = model.predict(future)
    actual_prediction = model.predict(stocks)
    return forecast, actual_prediction


def plot_results(crypto, against, stocks, forecast, actual_prediction):
    plt.figure(figsize=(12, 6))
    plt.plot(actual_prediction['ds'], actual_prediction['yhat1'], label="Prediction (Actual)", c='r')
    plt.plot(forecast['ds'], forecast['yhat1'], label='Future Prediction', c='b')
    plt.plot(stocks['ds'], stocks['y'], label='Actual', c='g')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%b\n%Y'))
    plt.legend()
    plt.title(f'{crypto}-{against} Forecast')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.show()


def main():
    try:
        crypto, against = get_user_input()
        while crypto:
            start_date = dt.datetime.now() - dt.timedelta(days=365 * 4)
            end_date = dt.datetime.now()
            data = download_data(crypto, against, start_date, end_date)
            if data.empty:
                raise ValueError(
                    f"No data available for cryptocurrency {crypto} in currency {against} during this time period.")
            stocks = prepare_data(data)
            model = fit_model(stocks)
            forecast, actual_prediction = make_predictions(model, stocks)
            plot_results(crypto, against, stocks, forecast, actual_prediction)
            crypto, against = get_user_input()
    except ValueError as ve:
        print(f"Error: {ve}. Please try again.")


if __name__ == "__main__":
    main()
