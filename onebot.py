# -*- encoding: utf 8 -*-
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ChatMember
import logging
from random import shuffle
from Player import Player
from Game import Game


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
TOKEN = "___SUPERSECRETTOKEN__" #write here your bot's token
GREETINGS = 'Welcome to One Poker. If you wish to participate, enter the command /participate'
GREETINGS2 = 'Type /rules for an explanation of the game mechanics and /help to know the commands of this bot. Type /disclaimer to know further.'
RULES = 'One Poker is a game in which two people play following these rules:\n1. Both of you will receive 10 lives, you can bet a minimum of 1 life in each round and a maximum of the lives you have at that moment.\n2.The game uses three decks of poker without the joker card, when . \n 3. Each player will receive 2 cards and will have in his hand always 2 cards. \n 4. The value of the cards is determined by its number, being DOWN cards: 2, 3, 4, 5, 6, 7 and UP cards: 8, 9, 10, J, Q, K, A. \n 5. The winning card is always the highest with the exception of the 2 that wins the Ace. \n 6. Once players receive their cards, both of them will be informed if they have UP or DOWN cards in their hand. \n 7. The game ends when one of the players loses all the lives.\n '
HELP = 'Here is a list of all the commands Mother Sophie has:\n /disclaimer\n /endgame\n /freeasinfreedom - Link to the code in github.\n /fold\n /help - This command.\n /participate - Starts a new game.\n /quit - Players cannot quit One Poker irl but here you can.\n /raise\n /rules\n /scores - Display how the game goes so far, including cards, victories\n /start\n /state\n /zawa\n'
DISCLAIMER = 'I don not own any of names or refences made of the manga neither the original gameplay idea of One Poker.'
FREEDOM = 'If you want a copy of the code, you can have it in my github: https://github.com/cryogenic-dreams/one_poker_bot/'
GAME_STARTS = 'The game will start now.\nEach player will receive two cards.'
SELECT_CARD = 'Please select your card.'
SELECTION_COMPLETED = 'Card selection has been completed.\nNow proceeding to betting phase.'
QUESTION = 'Check or bet?'
CHECK = 'Both players check.'
BET_COMPL = 'Betting complete.'
BET2 = 'The betting phase has been completed.'
CARD_REV = 'Now revealing the cards.'
WIN = 'The winner is '
chats={}


def start(bot, update):
    """Send greetings messages when the command /start is issued."""
    update.message.reply_text(GREETINGS)
    update.message.reply_text(GREETINGS2)
    
def help(bot, update):
    """Send a list of the commands when the command /help is issued."""
    update.message.reply_text(HELP)

def rules(bot, update):
    """Send a message when the command /rules is issued."""
    update.message.reply_text(RULES)

def disclaimer(bot, update):
    """Send a message when the command /rules is issued."""
    update.message.reply_text(DISCLAIMER)
    
def freeasinfreedom(bot, update):
    """Send a message when the command /rules is issued."""
    bot.send_message(update.message.chat_id, FREEDOM)

def status(bot, update, hand1, hand2):
    """Send the UPs and DOWNs of the players when the command /status is issued."""
    chat_id = update.message.chat_id
    update.message.reply_text(chats[chat_id].player1.displayStatus())
    update.message.reply_text(chats[chat_id].player2.displayStatus())

def participate(bot, update):
    """take id and name of the user"""
    """after second input, start the actual game"""
    chat_id = update.message.chat_id
    name = update.message.from_user.first_name
    if (not(chats.has_key(chat_id))):
        update.message.reply_text('Entry completed.\n' + name + ': 10 Lives.')
		p1 = Player(name)
		game = Game(chat_id, p1, None, [], [])
    	chats[chat_id] = game
    else:
		if(chats[chat_id].player2 is None):
			p2 = Player(name)
			chats[chat_id].player2 = p2
			update.message.reply_text('Entry completed.\n' + name + ': 10 Lives.')
			#once the players are set, lets give em cards
			bot.send_message(update.message.chat_id, GAME_STARTS)
			chats[chat_id].giveCards(1)
			chats[chat_id].giveCards(1) #give 2 cards for the 1st time
		else:
			update.message.reply_text('There is a maximum of 2 players in this game.')
	bot.send_message(update.message.chat_id, SELECT_CARD)		
    print chats
	
def raiseBet(bot, update):
    """Raise a bet"""
	
def fold(bot, update):
    """Fold"""

def quit(bot, update):
    """Player that sends the message quits the game"""
	
def scores(bot, update):
    """Prints all the matches in a game"""

def endgame(bot, update):
    """End the game, like quit, but there are not winners nor losers"""
	
def zawa(bot, update):
    """Every 1 to 10 minutes (randomly) bot posts a zawa (ざわ) message. It's a switcher, typing it for the 1st enables and the 2nd time disables it"""
	
def echo(bot, update):
    """Lets keep the tutorial's examples from now"""
    update.message.reply_text(update.message.text)

def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():

    updater = Updater(TOKEN)
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("rules", rules))
    dp.add_handler(CommandHandler("status", status))
    dp.add_handler(CommandHandler("participate", participate))
    dp.add_handler(CommandHandler("disclaimer", disclaimer))
    dp.add_handler(CommandHandler("freeasinfreedom", freeasinfreedom))
    dp.add_handler(CommandHandler("fold", fold))
    dp.add_handler(CommandHandler("raise", raiseBet))
    dp.add_handler(CommandHandler("quit", quit))
    dp.add_handler(CommandHandler("endgame", endgame))
    dp.add_handler(CommandHandler("scores", scores))
    dp.add_handler(CommandHandler("zawa", zawa))

    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
