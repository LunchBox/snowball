#!/usr/bin/env python
# coding: utf-8

# In[10]:


from backtesting import Backtest, Strategy
import yfinance as yf


# In[11]:


# https://stackoverflow.com/questions/40256338/calculating-average-true-range-atr-on-ohlc-data-with-python
def wwma(values, n):
    """
        J. Welles Wilder's EMA 
    """
    return values.ewm(alpha=1/n, adjust=False).mean()

def atr(df, n=14):
    data = df.copy()
    high = data.High
    low = data.Low
    close = data.Close
    data['tr0'] = abs(high - low)
    data['tr1'] = abs(high - close.shift())
    data['tr2'] = abs(low - close.shift())
    tr = data[['tr0', 'tr1', 'tr2']].max(axis=1)
    atr = wwma(tr, n)
    return atr


# In[12]:


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


# In[13]:


data = yf.download("^SPX", period="60d", interval="5m")
data['atr'] = atr(data)

bt = Backtest(
    data, 

    # Strategy
    FallUp, 

    # Commission
    commission=.002, 

    # market orders will be filled with respect to the current bar's closing price instead of the next bar's open.
    trade_on_close=True,

    # new order auto-closes the previous trade/position, making at most a single trade (long or short) in effect at each time
    exclusive_orders=True 
)

stats = bt.run()


# In[14]:


display(stats)


# In[15]:


display(stats._trades)


# In[16]:


bt.plot()

