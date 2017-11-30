from random import shuffle
from Player import Player

class Game:

	clubs = ['2 of clubs', '3 of clubs', '4 of clubs', '5 of clubs', '6 of clubs', '7 of clubs', '8 of clubs', '9 of clubs', '10 of clubs', 'Jack of clubs', 'Queen of clubs', 'King of clubs', 'Ace of clubs']
	spades = ['2 of spades', '3 of spades', '4 of spades', '5 of spades', '6 of spades', '7 of spades', '8 of spades', '9 of spades', '10 of spades', 'Jack of spades', 'Queen of spades', 'King of spades', 'Ace of spades']
	hearts = ['2 of hearts', '3 of hearts', '4 of hearts', '5 of hearts', '6 of hearts', '7 of hearts', '8 of hearts', '9 of hearts', '10 of hearts', 'Jack of hearts', 'Queen of hearts', 'King of hearts', 'Ace of hearts']
	diamonds = ['2 of diamonds', '3 of diamonds', '4 of diamonds', '5 of diamonds', '6 of diamonds', '7 of diamonds', '8 of diamonds', '9 of diamonds', '10 of diamonds', 'Jack of diamonds', 'Queen of diamonds', 'King of diamonds', 'Ace of diamonds']
	DECK = clubs + spades + hearts + diamonds
	GAME_DECK = DECK * 3
	
	def __init__ (self, chat_id, player1, player2, matches, victories):
		self.chat_id = chat_id
		self.player1 = player1
		self.player2 = player2
		self.deck = shuffle(Game.GAME_DECK)
		self.matches = matches
		self.victories = victories
	
	def giveCards(self, firstP):
		if (firstP == 1):
			self.player1.hand = self.giveCard(self.player1)
			self.player2.hand = self.giveCard(self.player2)
		else:
			self.player2.hand = self.giveCard(self.player2)
			self.player1.hand = self.giveCard(self.player1)
		if len(self.player1.hand) == 2: 
			self.player1.displayStatus()
			self.player2.displayStatus()
	
	def giveCard(self, player):
		if len(self.deck) != 0:
			return player.hand.append(self.deck.pop())
		else:
			#end game here
			return false
		
	def winningCard(self, choice1, choice2):
		"""
		Returns 1 if first card wins or 2 if second card wins
		Returns 0 if there's a tie
		"""
		card1 = self.player1.hand[choice1]
		card2 = self.player2.hand[choice2]
	
		self.disposeCards(choice1, choice2)
	
		if('clubs' in card1):
			i1 = clubs.index(card1)
		elif('spades' in card1):
			i1 = spades.index(card1)
		elif('diamonds' in card1):
			i1 = diamonds.index(card1)
		elif('hearts' in card1):
			i1 = hearts.index(card1)
		
		if('clubs' in card2):
			i2 = clubs.index(card2)
		elif('spades' in card2):
			i2 = spades.index(card2)
		elif('diamonds' in card2):
			i2 = diamonds.index(card2)
		elif('hearts' in card2):
			i2 = hearts.index(card2)
		
		if (i1 < i2):#player 2 wins
			if (i1 == 0 and i2 == 12): #unless it's a 2vsAce
				return 1
			else:
				return 2
		elif (i1 == i2):
			return 0 #players tie
		elif (i1 > i2):#player 1 wins
			if (i2 == 0 and i1==12): #unless it's a 2vsAce
				return 2
			else:
				return 1
			
			
	def disposeCards(self, choice1, choice2): #save cards of the match and previous ones and then remove them from the players hand
		card1 = self.player1.hand[choice1]
		card2 = self.player2.hand[choice2]
		
		self.matches.append([card1, card2])
		self.player1.hand.remove(choice1)
		self.player2.hand.remove(choice2)
	
	def manageResult(self, choice1, choice2): #save results and redistribute lifes
		result = self.winningCard(choice1, choice2)
		victories.append(result)
		if(result == 1):
			#player 1 wins
			self.player1.lifes = self.player1.lifes + self.player1.bet + self.player2.bet
			self.initBets()
		elif (result == 2):
			#player 2 wins
			self.player2.lifes = self.player2.lifes + self.player1.bet + self.player2.bet
			self.initBets()
		else:
			#it's a tie
			self.player1.lifes = self.player1.lifes + self.player1.bet
			self.player2.lifes = self.player2.lifes + self.player2.bet
			self.initBets()
			
			
	def initBets(self):
		self.player1.bet = 0
		self.player2.bet = 0
