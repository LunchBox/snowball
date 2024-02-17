import pandas as pd
import pandas_ta as ta
import yfinance as yf

# TODO

df = yf.download("^SPX", period="60d", interval="5m")

print(ta.bbands(df.Open))