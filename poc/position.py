class Position:
	
	def __init__(self, initial_state):
		self.state = initial_state
		self.trade = "READY"
		self.action = initial_state
		self.market = initial_state
		self.strategy = "GRID TRADE"

	def market_buy(self):
		self.state = "IN"
		self.action = "LONG TRADE"
		self.trade = "READY" 

	def market_short(self):
		self.state = "IN"
		self.action = "SHORT TRADE"
		self.trade = "READY"

	def market_delay(self):
		self.state = "IN"
		self.action = "DELAY TRADE"
		self.trade = "NOT READY"

	def market_sell(self):
		self.state = "OUT"
		self.action = "HOLD"
		self.trade = "READY"

	def win(self):
		self.state = "OUT"
		self.trade = "READY"

	def loss(self):
		self.state = "OUT"
		self.trade = "NOT READY"
		# self.action = "SHORT TRADE"

	def ready(self):
		self.trade = "READY"

	def not_ready(self):
		self.trade = "NOT READY"

	def delay(self):
		self.action = "DELAY TRADE"
		self.trade = "NOT READY"

	def market_change_bull(self):
		self.market = "BULL"

	def market_change_bear(self):
		self.market = "BEAR"

	def bull_run(self):
		self.action = "WAIT FOR REVERSE"

	def force_bull(self):
		self.action = "BULL FORCE"

	def long_term_strat(self):
		self.strategy = "LONG TERM"

	def short_term_strat(self):
		self.strategy = "SHORT TERM"

	def grid_strat(self):
		self.strategy = "GRID TRADE"