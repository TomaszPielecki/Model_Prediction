# -*- coding: utf-8 -*-

import datetime as dt

import pandas as pd
import yfinance as yf

start = dt.datetime.now() - dt.timedelta(days=5)
end = dt.datetime.now()
# Dane z Yahoo Finance
data = yf.download(tickers="eth-USD", start=start, end=end)
df = pd.DataFrame(data, columns=['High', 'Low', 'Open', 'Volume', 'Close'])
print(df)
