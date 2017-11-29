from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ChatMember
import logging
from random import shuffle


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
TOKEN = "___SUPERSECRETTOKEN__" #write here your bot's token
GREETINGS = 'Welcome to One Poker. If you wish to play, enter the command /participate'
GREETINGS2 = 'Type /rules for an explanation of the game mechanics and /help to know the commands of this bot. Type /disclaimer to know further.'
RULES = 'One Poker is a game in which two people play following these rules:\n 1. Both of you will receive 10 lifes, you can bet a minimum of 1 life in each round and a maximum of the lifes you have at that moment.\n 2.The game uses three decks of poker without the joker card, when it runs out of cards, the game ends in tie. \n 3.Each player will receive 2 cards at the begining and will have in his hand always 2 cards. \n 4.The value of the cards is determined by its number, being DOWN cards: 2, 3, 4, 5, 6, 7 and UP cards: 8, 9, 10, J, Q, K, A. \n 5.The winning card is always the highest with the exception of the 2 that wins the Ace. \n 6.Once players receive their cards, both of them will be informed if they have UP or DOWN cards in their hand. \n 7.The game ends when one of the players loses all his lifes.\n '
HELP = 'Here is a list of all the commands Mother Sophie has:\n /disclaimer\n /endgame\n /freeasinfreedom - Link to the code in github.\n /fold\n /help - This command.\n /participate - Starts a new game.\n /quit - Players cannot quit One Poker irl but here you can.\n /raise\n /rules\n /score - Display how the game goes so far, including cards, victories\n /start\n /state\n /zawa\n'
DISCLAIMER = ' '
FREEDOM = 'If you want a copy of the code, you can have it in my github: https://github.com/cryogenic-dreams/one_poker_bot/'

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
    update.message.reply_text(FREEDOM)

def status(bot, update, hand1, hand2):
    """Send the UPs and DOWNs of the players when the command /status is issued."""
    update.message.reply_text()
    update.message.reply_text()

def participate(bot, update):
    """take id and name of the user"""
    """after second input, start the actual game"""
    update.message.reply_text('Hello player1')

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

    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
