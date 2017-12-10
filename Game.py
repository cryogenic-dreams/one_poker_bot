# -*- encoding: utf 8 -*-
from random import shuffle
from Player import Player


class Game:
    # I heard you like emojis, so I put emojis in the code so you can enjoy them while playing. ur welcome
    clubs = ['2 of ♣️', '3 of ♣️', '4 of ♣️', '5 of ♣️', '6 of ♣️', '7 of ♣️', '8 of ♣️', '9 of ♣️', '10 of ♣️',
             'Jack of ♣️', 'Queen of ♣️', 'King of ♣️', 'Ace of ♣️']
    spades = ['2 of ♠️', '3 of ♠️', '4 of ♠️', '5 of ♠️', '6 of ♠️', '7 of ♠️', '8 of ♠️', '9 of ♠️', '10 of ♠️',
              'Jack of ♠️', 'Queen of ♠️', 'King of ♠️', 'Ace of ♠️']
    hearts = ['2 of ♥️', '3 of ♥️', '4 of ♥️', '5 of ♥️', '6 of ♥️', '7 of ♥️', '8 of ♥️', '9 of ♥️', '10 of ♥️',
              'Jack of ♥️', 'Queen of ♥️', 'King of ♥️', 'Ace of ♥️']
    diamonds = ['2 of ♦️', '3 of ♦️', '4 of ♦️', '5 of ♦️', '6 of ♦️', '7 of ♦️', '8 of ♦️', '9 of ♦️', '10 of ♦️',
                'Jack of ♦️', 'Queen of ♦️', 'King of ♦️', 'Ace of ♦️']
    DECK = clubs + spades + hearts + diamonds
    GAME_DECK = DECK * 3

    def __init__(self, chat_id, player1, player2, matches, victories, deck):
        self.chat_id = chat_id
        self.player1 = player1
        self.player2 = player2
        self.deck = Game.GAME_DECK
        shuffle(self.deck)
        self.matches = matches
        self.victories = victories

    def giveCards(self, firstP):
        if firstP == 1:
            self.player1.hand.append(self.giveCard())
            self.player2.hand.append(self.giveCard())
        else:
            self.player2.hand.append(self.giveCard())
            self.player1.hand.append(self.giveCard())

    def giveCard(self):
        if len(self.deck) != 0:
            return self.deck.pop()
        else:
            # end game here
            return false

    def winningCard(self, card1, card2):
        """
	Returns 1 if first card wins or 2 if second card wins
	Returns 0 if there's a tie
	"""
        self.matches.append([card1, card2])

        if '♣️' in card1:
            i1 = Game.clubs.index(card1)
        elif '♠️' in card1:
            i1 = Game.spades.index(card1)
        elif '♦️' in card1:
            i1 = Game.diamonds.index(card1)
        elif '♥️' in card1:
            i1 = Game.hearts.index(card1)

        if '♣️' in card2:
            i2 = Game.clubs.index(card2)
        elif '♠️' in card2:
            i2 = Game.spades.index(card2)
        elif '♦️' in card2:
            i2 = Game.diamonds.index(card2)
        elif '♥️' in card2:
            i2 = Game.hearts.index(card2)

        if i1 < i2:  # player 2 wins
            if i1 == 0 and i2 == 12:  # unless it's a 2vsAce
                return 1
            else:
                return 2
        elif i1 == i2:
            return 0  # players tie
        elif i1 > i2:  # player 1 wins
            if i2 == 0 and i1 == 12:  # unless it's a 2vsAce
                return 2
            else:
                return 1

    def manageResult(self, card1, card2):  # save results and redistribute lives
        result = self.winningCard(card1, card2)
        self.victories.append(result)
        if result == 1:
            # player 1 wins
            self.player1.lives = self.player1.lives + self.player1.bet + self.player2.bet
        elif result == 2:
            # player 2 wins
            self.player2.lives = self.player2.lives + self.player1.bet + self.player2.bet
        else:
            # it's a tie
            self.player1.lives = self.player1.lives + self.player1.bet
            self.player2.lives = self.player2.lives + self.player2.bet

        self.initPlayers()
        if result == 1:
            self.giveCards(1)
        elif result == 2:
            self.giveCards(2)
        else:
            self.giveCards(1)

        return self.whoWon(result)

    def initPlayers(self):
        self.player1.check = False
        self.player2.check = False
        self.player1.bet = 0
        self.player2.bet = 0
        self.player1.card_played = []
        self.player2.card_played = []

    def displayScores(self):
        i = 0
        string = ''
        while i < len(self.victories):
            string = '``` Round %i: %s - %s | %s - %s [RESULT: %s] ```' % (i + 1, self.player1.name, self.matches[i][0], self.player2.name, self.matches[i][1], self.whoWon(self.victories[i])) + string
            i += 1
        return string

    def whoWon(self, number):
        """
	Players are just numbers, after all...
	"""
        if number == 1:
            return self.player1.name + ' won.\n'
        elif number == 2:
            return self.player2.name + ' won.\n'
        else:
            return 'Players tied.\n'
