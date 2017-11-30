# -*- encoding: utf 8 -*-
from random import shuffle
from Player import Player

class Game:

	clubs = ['2 of ♣️', '3 of ♣️', '4 of ♣️', '5 of ♣️', '6 of ♣️', '7 of ♣️', '8 of ♣️', '9 of ♣️', '10 of ♣️', 'Jack of ♣️', 'Queen of ♣️', 'King of ♣️', 'Ace of ♣️']
	spades = ['2 of ♠️', '3 of ♠️', '4 of ♠️', '5 of ♠️', '6 of ♠️', '7 of ♠️', '8 of ♠️', '9 of ♠️', '10 of ♠️', 'Jack of ♠️', 'Queen of ♠️', 'King of ♠️', 'Ace of ♠️']
	hearts = ['2 of ♥️', '3 of ♥️', '4 of ♥️', '5 of ♥️', '6 of ♥️', '7 of ♥️', '8 of ♥️', '9 of ♥️', '10 of ♥️', 'Jack of ♥️', 'Queen of ♥️', 'King of ♥️', 'Ace of ♥️']
	diamonds = ['2 of ♦️', '3 of ♦️', '4 of ♦️', '5 of ♦️', '6 of ♦️', '7 of ♦️', '8 of ♦️', '9 of ♦️', '10 of ♦️', 'Jack of ♦️', 'Queen of ♦️', 'King of ♦️', 'Ace of ♦️']
	DECK = clubs + spades + hearts + diamonds
	GAME_DECK = DECK * 3
	
	def __init__ (self, chat_id, player1, player2, matches, victories, deck):
		self.chat_id = chat_id
		self.player1 = player1
		self.player2 = player2
		self.deck = Game.GAME_DECK
		shuffle(self.deck)
		self.matches = matches
		self.victories = victories
	
	def giveCards(self, firstP):
		if (firstP == 1):
			self.player1.hand.append(self.giveCard(self.player1))
			self.player2.hand.append(self.giveCard(self.player2))
		else:
			self.player2.hand.append(self.giveCard(self.player2))
			self.player1.hand.append(self.giveCard(self.player1))

	
	def giveCard(self, player):
		if len(self.deck) != 0:
			return self.deck.pop()
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
	
		if('♣️' in card1):
			i1 = clubs.index(card1)
		elif('♠️' in card1):
			i1 = spades.index(card1)
		elif('♦️' in card1):
			i1 = diamonds.index(card1)
		elif('♥️' in card1):
			i1 = hearts.index(card1)
		
		if('♣️' in card2):
			i2 = clubs.index(card2)
		elif('♠️' in card2):
			i2 = spades.index(card2)
		elif('♦️' in card2):
			i2 = diamonds.index(card2)
		elif('♥️' in card2):
			i2 = hearts.index(card2)
		
		if (i1 < i2):#player 2 wins
			if (i1 == 0 and i2 == 12): #unless it's a 2vsAce
				return 1
			else:
				return 2
		elif (i1 == i2):
			return 0 #players tie
		elif (i1 > i2):#player 1 wins
			if (i2 == 0 and i1 == 12): #unless it's a 2vsAce
				return 2
			else:
				return 1
			
			
	def disposeCards(self, choice1, choice2): #save cards of the match and previous ones and then remove them from the players hand
		card1 = self.player1.hand[choice1]
		card2 = self.player2.hand[choice2]
		
		self.matches.append([card1, card2])
		self.player1.hand.remove(choice1)
		self.player2.hand.remove(choice2)
	
	def manageResult(self, choice1, choice2): #save results and redistribute lives
		result = self.winningCard(choice1, choice2)
		victories.append(result)
		if(result == 1):
			#player 1 wins
			self.player1.lives = self.player1.lives + self.player1.bet + self.player2.bet
		elif (result == 2):
			#player 2 wins
			self.player2.lives = self.player2.lives + self.player1.bet + self.player2.bet
		else:
			#it's a tie
			self.player1.lives = self.player1.lives + self.player1.bet
			self.player2.lives = self.player2.lives + self.player2.bet
			
		self.initBets()
		return result
			
	def initBets(self):
		self.player1.bet = 0
		self.player2.bet = 0
