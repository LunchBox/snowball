#!/usr/bin/env python
# coding: utf-8

# # backtesting with ATR adjustment

# > The **average true range (ATR)** is a market volatility indicator used in technical analysis. It is typically derived from the 14-day simple moving average of a series of true range indicators. The ATR was initially developed for use in commodities markets but has since been applied to all types of securities.

# In[1]:


from backtesting import Backtest, Strategy
import yfinance as yf
import pandas_ta as ta


# In[2]:


data = yf.download("^SPX", period="60d", interval="5m")


# In[3]:


class FallUp(Strategy):
    def init(self):
        self.down_days = 0
        self.hold_days = 0

    def next(self):
        # close price of previous day
        pv = self.data.Close[-2]

        # close price of current day
        cv = self.data.Close[-1]

        # consecutively falling 3 times and reversal, buy-in
        if self.down_days >= 5 and cv > pv and self.data['atr'] > 4:
            self.buy()
            self.hold_days = 0
            self.down_days_after_position = 0

        # record falling times
        if cv < pv:
            self.down_days += 1
        else:
            self.down_days = 0

        if self.position:
            self.hold_days += 1

            # record falling times after position
            if cv < pv:
                self.down_days_after_position += 1

            if self.down_days > 1:
                self.position.close()

            # with position, falling once within 4 times, close the position
            if self.hold_days <= 4 and self.down_days_after_position > 0:
                self.position.close()


# pandas_ta 中有現成的 atr 可以用

# In[4]:


data['atr'] = ta.atr(data.High, data.Low, data.Close, length=28, fillna=0)

data['atr']


# In[5]:


bt = Backtest(
    data, 

    # Strategy
    FallUp, 

    # Commission
    commission=.002, 

    # 預設使用翌日的 Open 作為買賣價格，這裡改成使用當日的 close 作為買賣價格
    trade_on_close=True,

    # 每次只下 1 張單
    exclusive_orders=True 
)

stats = bt.run()


# In[6]:


stats


# In[7]:


stats._trades


# In[8]:


bt.plot()


# In[ ]:




