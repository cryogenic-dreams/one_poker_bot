class Player:
	LIFES = 10
	BET = 0

	def __init__ (self, name):
		self.hand = []
		#self.id = id
		self.name = name
		self.lifes = Player.LIFES
		self.bet = Player.BET
	
	def displayStatus(self):
		return 'Player ' + self.name + ': ' + self.isUPorDOWN(self.hand[0]) + ' | ' + self.isUPorDOWN(self.hand[1])
	
	def isUPorDOWN(card): #ideally, this will be in a different class named card, but... 2lazy
		if ('2' in card or '3' in card or '4' in card or '5' in card or '6' in card or '7' in card):
			return 'DOWN'
		else:
			return 'UP'

	def setBet(self, quantity):
		if (quantity <= self.lifes):
			self.lifes = self.lifes - quantity
			self.bet = self.bet + quantity
		else:
			return false