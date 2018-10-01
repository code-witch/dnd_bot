class Item:
	items = 0

	def __init__(self,title='default title', desc='default description', sell=0, buy=0, amt=1):
		self.title = title
		self.description = desc
		self.sell = sell
		self.buy = buy
		self.amount = amt
		self.id = items
		items += 1
	
	def set_title(self, title):
		self.title = title

	def set_desc(self, desc):
		self.description = desc
	
	def set_sell(self, sell):
		self.sell = sell

	def set_buy(self, buy):
		self.buy = buy

	def set_amount(self, amt):
		self.amount = amt
	
	def __str__(self):
		return self.name
