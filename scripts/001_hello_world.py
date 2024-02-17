#!/usr/bin/env python
# coding: utf-8

# In[1]:


# importing the modules
from IPython.display import display
import pandas as pd
 
# creating a DataFrame
dict = {'Name' : ['Martha', 'Tim', 'Rob', 'Georgia'],
        'Maths' : [87, 91, 97, 95],
        'Science' : [83, 99, 84, 76]}
df = pd.DataFrame(dict)
 
# displaying the DataFrame
display(df)


# In[2]:


import yfinance as yf

ticker = '^SPX'

period = "5d"
interval = "5m"

df = yf.download(ticker, period=period, interval=interval)

display(df)


# In[5]:


import pandas_ta as ta

atr = ta.atr(df.High, df.Low, df.Close, window=14, fillna=0)

display(atr)


# In[4]:


import matplotlib.pyplot as plt

plt.plot(atr.reset_index(drop=True))

