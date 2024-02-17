#!/usr/bin/env python
# coding: utf-8

# In[17]:


from IPython.display import display

from backtesting import Backtest, Strategy
import yfinance as yf


# In[18]:


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
		if self.down_days >= 3 and cv > pv:
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

			# in any window, falling over 2 times, close the position
			# backtesting can do long / short trading, self.sell() means shorting, 
			# close position should use self.position.close()
			if self.down_days_after_position > 1:
				self.position.close()
			
			# with position, falling once within 4 times, close the position
			if self.hold_days <= 4 and self.down_days_after_position > 0:
				self.position.close()


# In[19]:


bt = Backtest(
	# data
	yf.download("^SPX", period="60d", interval="5m"), 

	# Strategy
	FallUp, 

	# Commission
	commission=.002, 

	# market orders will be filled with respect to the current bar's closing price instead of the next bar's open.
	trade_on_close=True,

	# new order auto-closes the previous trade/position, making at most a single trade (long or short) in effect at each time
	exclusive_orders=True 
)


# In[20]:


stats = bt.run()


# In[21]:


display(stats)


# In[22]:


display(stats._trades)


# In[23]:


bt.plot()

