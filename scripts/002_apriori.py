from mlxtend.frequent_patterns import apriori
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import association_rules

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

enc = TransactionEncoder()
arr = enc.fit(data).transform(data)

print(arr)
print(enc.columns_)

df = pd.DataFrame(arr, columns = enc.columns_)
print(df)

res = apriori(df, min_support=0.3, use_colnames=True, max_len=4)

res = res[res['itemsets'].map(len) > 1]

res = res.sort_values('support', ascending=False)

print(res)



tickers = ['^SPX', 'NVDA', 'MSFT', 'AAPL', 'META']
df = yf.download(
 tickers, 
 start="2023-01-01", 
 end="2023-12-31", 
 interval="1d", 
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


data = df.values

enc = TransactionEncoder()
arr = enc.fit(data).transform(data)

print(arr)
print(enc.columns_)

df = pd.DataFrame(arr, columns = enc.columns_)
print(df)

start_time = time.time()
res = apriori(df, min_support=0.3, use_colnames=True, max_len=4)
print("--- run time: %s seconds ---" % (time.time() - start_time))

def contain_spx(list): 
	return any(item.startswith("^SPX") for item in list)

filtered_res = res[res['itemsets'].map(len) > 1]

filtered_res = filtered_res[filtered_res['itemsets'].apply(contain_spx)]

filtered_res = filtered_res.sort_values('support', ascending=False)

print(filtered_res)

rules = association_rules(res, metric="confidence", min_threshold=0.5)
rules = rules[rules['consequents'].apply(contain_spx)]
print(rules)