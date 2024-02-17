from efficient_apriori import apriori

import pandas as pd
import yfinance as yf

import time 

data = [
	['Milk', 'Onion', 'Nutmeg', 'Kidney Beans', 'Eggs', 'Yogurt'],
	['Dill', 'Onion', 'Nutmeg', 'Kidney Beans', 'Eggs', 'Yogurt'],
	['Milk', 'Apple', 'Kidney Beans', 'Eggs'],
	['Milk', 'Unicorn', 'Corn', 'Kidney Beans', 'Yogurt'],
	['Corn', 'Onion', 'Onion', 'Kidney Beans', 'Ice cream', 'Eggs']
]

itemsets, rules = apriori(data, min_support=0.5,  min_confidence=1)
print(rules) 




tickers = ['^SPX', 'NVDA', 'MSFT', 'AAPL', 'META']

# all spx 500
# spx_tickers = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]
# spx_tickers.to_csv('spx_tickers.csv', index=False)

# ticker_len = 70
# tickers = ["^SPX"] + pd.read_csv('spx_tickers.csv').iloc[:ticker_len, 0].tolist()

df = yf.download(
 tickers, 
 period="60d",
 interval="5m",
 group_by='Ticker'
)
print(df)


closes = []
for t in tickers:
	close = df[t].Close

	# apply label
	close = close.diff().apply(lambda x: "%s UP" % t if x > 0 else "%s DOWN" % t)

	close.name = t
	closes.append(close)

df = pd.concat(closes, axis=1)

print(df)


spx = df[['^SPX']][1:].reset_index(drop=True)

rest = df.loc[:, df.columns != '^SPX'][:-1].reset_index(drop=True)

df = pd.concat([spx, rest], axis=1)
print(df)

start_time = time.time()
itemsets, rules = apriori(df.values, min_support=0.2,  min_confidence=0.5)
print("--- run time: %s seconds ---" % (time.time() - start_time))

# 50 tickers around 14s
# 70 tickers around 60s


# print(itemsets)
# print(rules) 

rules_rhs = filter(lambda rule: len(rule.lhs) == 1 and rule.rhs[0].startswith('^SPX'), rules)
for rule in sorted(rules_rhs, key=lambda rule: rule.confidence, reverse=True):
  print(rule)