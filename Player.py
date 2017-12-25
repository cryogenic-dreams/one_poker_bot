# -*- encoding: utf 8 -*-


class Player:
    LIVES = "You: Bet🕴x%i - Lives🕴x%i   \nRival: Bet🕴x%i - Lives🕴x%i"
    UP = "⬆️"
    DOWN = "️⬇️"

    def __init__(self,
                 name,
                 user,
                 reply_id,
                 lives=9,
                 bet=1,
                 card=None,
                 check=False,
                 red_lives=1,
                 hand=None):

        if card is None:
            card = []
        if hand is None:
            hand = []
        self.user = user
        self.name = name
        self.lives = lives
        self.bet = bet
        self.card_played = card
        self.check = check
        self.reply_id = reply_id
        self.red_lives = red_lives
        self.hand = hand

    def displayStatus(self, rival):
        return "You: %s %s\nRival: %s %s" % (self.isUPorDOWN(self.hand[0]), self.isUPorDOWN(self.hand[1]),
                                            rival.isUPorDOWN(self.hand[0]), rival.isUPorDOWN(self.hand[1]))

    def isUPorDOWN(self, card):  # ideally, this will be in a different class named card, but... 2lazy
        if '2' in card or '3' in card or '4' in card or '5' in card or '6' in card or '7' in card:
            return Player.DOWN
        else:
            return Player.UP

    def setBet(self, quantity):
        if quantity <= self.lives:
            self.lives = self.lives - quantity
            self.bet = self.bet + quantity

    def display_lives(self, rival):
        return Player.LIVES % (self.bet, self.lives, rival.bet, rival.lives)
