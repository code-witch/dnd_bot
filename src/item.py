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
	
	def setTitle(self, title):
		self.title = title

	def setDescription(self, desc):
		self.description = desc
	
	def setSell(self, sell):
		self.sell = sell

	def setBuy(self, buy):
		self.buy = buy

	def setAmount(self, amt):
		self.amount = amt
	
