# -*- encoding: utf 8 -*-
from random import shuffle
from strings import Strings


class Game:
    # I heard you like emojis, so I put unicode in the code so you can enjoy them while playing. ur welcome

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

    def __init__(self,
                 chat_id,
                 player1,
                 player2=None,
                 matches=None,
                 victories=None,
                 bets=None,
                 max_bet=0):

        if bets is None:
            bets = []
        if victories is None:
            victories = []
        if matches is None:
            matches = []
        self.chat_id = chat_id
        self.player1 = player1
        self.player2 = player2
        self.deck = Game.GAME_DECK
        shuffle(self.deck)
        self.matches = matches
        self.bets = bets
        self.victories = victories
        self.max_bet = max_bet

    def giveCards(self, first_player):
        if first_player == 1:
            self.player1.hand.append(self.giveCard())
            self.player2.hand.append(self.giveCard())
        else:
            self.player2.hand.append(self.giveCard())
            self.player1.hand.append(self.giveCard())

    def giveCard(self):
        if len(self.deck) != 0:
            return self.deck.pop()
        else:
            # never came to this end, so reshuffle and chill
            self.deck = Game.GAME_DECK
            shuffle(self.deck)
            return self.deck.pop()

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

    def manageResult(self, card1, card2, fold=None):  # save results and redistribute lives
        if fold is None:
            result = self.winningCard(card1, card2)
        else:
            result = fold  # technically this should be called winner, not fold
            self.matches.append([card1, card2])
        self.victories.append(result)
        self.manageLives(result)
        self.initPlayers()
        self.manageCards(result)

        return self.displayScore(len(self.victories)-1)

    def initPlayers(self):
        self.player1.check = False
        self.player2.check = False
        self.player1.bet = 0
        self.player1.setBet(1)
        self.player2.bet = 0
        self.player2.setBet(1)
        self.player1.card_played = []
        self.player2.card_played = []

    def displayScores(self):
        i = len(self.victories) - 1
        string = ""
        while i > -1:
            string = self.displayScore(i) + string
            i -= 1
        return string

    def displayScore(self, number):
        return Strings.SCORES % (
            number + 1, self.player1.name, self.bets[number][0],
            self.matches[number][0].decode('utf-8'),
            self.player2.name, self.bets[number][1],
            self.matches[number][1].decode('utf-8'),
            self.whoWon(self.victories[number]))

    def whoWon(self, number):
        """
        Players are just numbers, after all...
        """
        if number == 1:
            return self.player1.name + " won.\n"
        elif number == 2:
            return self.player2.name + " won.\n"
        else:
            return "Players tied.\n"

    def manageLives(self, result):
        self.bets.append([self.player1.bet, self.player2.bet])
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

    def manageCards(self, result):
        if result == 1:
            self.giveCards(1)
        elif result == 2:
            self.giveCards(2)
        else:
            self.giveCards(1)
            
    def update_max_bet(self):
        self.max_bet = min(self.player1.lives, self.player2.lives)
