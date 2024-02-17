#!/usr/bin/env python
# coding: utf-8

# In[22]:


from IPython.display import display

from mlxtend.frequent_patterns import apriori
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import association_rules

import pandas as pd
import yfinance as yf

import time 


# In[23]:


data = [
	['Milk', 'Onion', 'Nutmeg', 'Kidney Beans', 'Eggs', 'Yogurt'],
	['Dill', 'Onion', 'Nutmeg', 'Kidney Beans', 'Eggs', 'Yogurt'],
	['Milk', 'Apple', 'Kidney Beans', 'Eggs'],
	['Milk', 'Unicorn', 'Corn', 'Kidney Beans', 'Yogurt'],
	['Corn', 'Onion', 'Onion', 'Kidney Beans', 'Ice cream', 'Eggs']
]


# In[24]:


enc = TransactionEncoder()
arr = enc.fit(data).transform(data)

display(arr)


# In[25]:


display(enc.columns_)


# In[26]:


df = pd.DataFrame(arr, columns = enc.columns_)
display(df)


# In[27]:


res = apriori(df, min_support=0.3, use_colnames=True, max_len=4)

f_res = res[res['itemsets'].map(len) > 1].sort_values('support', ascending=False)

display(f_res)


# In[28]:


tickers = ['^SPX', 'NVDA', 'MSFT', 'AAPL', 'META']

df = yf.download(
    tickers, 
    start="2023-01-01", 
    end="2023-12-31", 
    interval="1d", 
    group_by='Ticker'
)

display(df)


# In[29]:


closes = []
for t in tickers:
    close = df[t].Close
    
    # apply label
    close = close.diff().apply(lambda x: "%s UP" % t if x > 0 else "%s DOWN" % t)
    
    close.name = t
    closes.append(close)

df = pd.concat(closes, axis=1)

display(df)


# In[30]:


spx = df[['^SPX']][1:].reset_index(drop=True)

rest = df.loc[:, df.columns != '^SPX'][:-1].reset_index(drop=True)

df = pd.concat([spx, rest], axis=1)
display(df)


# In[31]:


data = df.values

enc = TransactionEncoder()
arr = enc.fit(data).transform(data)

df = pd.DataFrame(arr, columns = enc.columns_)

start_time = time.time()

res = apriori(df, min_support=0.3, use_colnames=True, max_len=4)

print("--- run time: %s seconds ---" % (time.time() - start_time))


# In[32]:


def contain_spx(list): 
	return any(item.startswith("^SPX") for item in list)


# In[33]:


f_res = res[res['itemsets'].map(len) > 1]

f_res = f_res[f_res['itemsets'].apply(contain_spx)].sort_values('support', ascending=False)

display(f_res)


# In[34]:


rules = association_rules(res, metric="confidence", min_threshold=0.5)
rules = rules[rules['consequents'].apply(contain_spx)]
display(rules)

