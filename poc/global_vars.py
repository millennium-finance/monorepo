import numpy as np

class Global_Rising_Roof():
	def __init__(self,initial_state):
		self.position = "OUT"
		self.buy_price = np.nan
		self.roof = np.nan
		self.roof_2 = np.nan
		self.passed_first_roof = "FALSE"
		self.floor = np.nan
		self.floor_2 = np.nan
		self.passed_first_floor = "FALSE"

	def not_ready(self):
		self.trade = "NOT READY"

	def ready(self):
		self.trade = "READY"
		

class Global_Grid():
	def __init__(self,initial_state,initial_state_trade):
		self.made_first_trade = "FALSE"
		self.all_trades_out = "FALSE"
		self.all_trades_closed = "TRUE"
		self.trade = initial_state_trade
		self.trade_value = 1
		self.double_even_trade = "FALSE"
		self.wait_to_sell = "FALSE"
		self.trade_style = initial_state
		self.balance = "FULL"

	def opened_trade(self):
		self.opened_or_closed = "OPENED"
		self.opened_or_closed_value = 0

	def closed_trade(self):
		self.opened_or_closed = "CLOSED"
		self.opened_or_closed_value = 1

	def not_ready(self):
		self.trade = "NOT READY"

	def ready(self):
		self.trade = "READY"

	def double_even(self):
		self.double_even_trade = "TRUE" 

	def start_over(self):
		self.made_first_trade = "FALSE"
		self.all_trades_closed = "TRUE"
		self.wait_to_sell = "FALSE"
		self.all_trades_out = "TRUE"	

	def trade_bull(self):
		self.trade_style = "BULL GRID"
		self.made_first_trade = "FALSE"
		self.all_trades_closed = "TRUE"
		self.trade = "READY"

	def trade_bear(self):
		self.trade_style = "BEAR GRID"
		self.made_first_trade = "FALSE"
		self.all_trades_closed = "TRUE"
		self.trade = "READY"

	def switch_trends(self):
		if self.trade_style == "BULL GRID":
			self.trade_style = "BEAR GRID"
		else:
			self.trade_style = "BULL GRID"

	def out_of_money(self):
		self.balance = "EMPTY"