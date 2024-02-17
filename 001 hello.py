import yfinance as yf

ticker = '^SPX'

period = "5d"
interval = "5m"

df = yf.download(ticker, period=period, interval=interval)

print(df)
