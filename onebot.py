# -*- coding: utf-8 -*-
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, ConversationHandler, RegexHandler
from telegram import ChatMember, KeyboardButton, ReplyKeyboardMarkup, ParseMode, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove, ForceReply
import logging
from random import shuffle, randint
from Player import Player
from Game import Game


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
TOKEN = "___YOURBOTSTOKEN___" #write here your bot's token
GREETINGS = '``` Welcome to One Poker. If you wish to participate, enter the command``` /participate'
GREETINGS2 = 'Type /rules for an explanation of the game mechanics and /help to know the commands of this bot. Type /disclaimer to know further.'
RULES = 'One Poker is a game in which two people play following these rules:\n1. Both of you will receive 10 lives, you can bet a minimum of 1 life in each round and a maximum of the lives you have at that moment.\n2.The game uses three decks of poker without the joker card, when . \n 3. Each player will receive 2 cards and will have in his hand always 2 cards. \n 4. The value of the cards is determined by its number, being DOWN cards: 2, 3, 4, 5, 6, 7 and UP cards: 8, 9, 10, J, Q, K, A. \n 5. The winning card is always the highest with the exception of the 2 that wins the Ace. \n 6. Once players receive their cards, both of them will be informed if they have UP or DOWN cards in their hand. \n 7. The game ends when one of the players loses all the lives.\n '
HELP = 'Here is a list of all the commands Mother Sophie has:\n /disclaimer\n /endgame\n /freeasinfreedom - Link to the code in github.\n /fold\n /help - This command.\n /participate - Starts a new game.\n /quit - Players cannot quit One Poker irl but here you can.\n /raise\n /rules\n /scores - Display how the game goes so far, including cards, victories\n /start\n /state\n /zawa\n'
DISCLAIMER = 'I do not own any of names or refences made of the manga neither the original gameplay idea of One Poker.'
FREEDOM = 'If you want a copy of the code, you can have it in my github: https://github.com/cryogenic-dreams/one_poker_bot/'
GAME_STARTS = '``` The game will start now.\nEach player will receive two cards.```'
CARDS = '``` These are your cards.```'
SELECT_CARD = '``` Please select your card.```'
SELECTION_COMPLETED = '``` Card selection has been completed.\nNow proceeding to betting phase.```'
QUESTION = '``` Check or bet?```'
CHECK = '``` Both players check.```'
CALL_RAISE_FOLD = '``` Call, raise or fold?```'
BET_COMPL = '``` Betting complete.```'
BET2 = '```The betting phase has been completed.```'
CARD_REV = '``` Now revealing the cards.```'
WIN = '```The winner is %s ```'
chats={}
LIVES,FOLD,C_R_F = range(3)
ZAWAZAWA = 'ざわ... ざわ...'
NATURAL = 'It\'s only natural.'
MEAN = 'What does it mean to gamble? What does it...'
PRESSURE = 'THE PRESSURE... it\'s crushing!'
BUT = 'But...'
STILL = 'Still!'
KUYASHII = 'KUYASHII'
CATCH = [ZAWAZAWA, NATURAL, MEAN, KUYASHII, STILL, BUT, PRESSURE, ZAWAZAWA, ZAWAZAWA]#extra zawas, just because

def start(bot, update):
    update.message.reply_text(GREETINGS, parse_mode = ParseMode.MARKDOWN)
    update.message.reply_text(GREETINGS2)
    
def help(bot, update):
    update.message.reply_text(HELP)

def rules(bot, update):
    update.message.reply_text(RULES)

def disclaimer(bot, update):
    update.message.reply_text(DISCLAIMER)
    
def freeasinfreedom(bot, update):
    bot.send_message(update.message.chat_id, FREEDOM)

def status(bot, update):
    """Send the UPs and DOWNs of the players when the command /status is issued."""
    chat_id = update.message.chat_id
    update.message.reply_text(chats[chat_id].player1.displayStatus(), parse_mode = ParseMode.MARKDOWN)
    update.message.reply_text(chats[chat_id].player2.displayStatus(), parse_mode = ParseMode.MARKDOWN)

def participate(bot, update):
    """take id and name of the user"""
    """after second input, start the actual game"""
    chat_id = update.message.chat_id
    user = update.message.from_user
    name = user.first_name
    if (chats.get(chat_id) is None):
        update.message.reply_text('``` Entry completed.\n' + name + ': 10 Lives.```', parse_mode = ParseMode.MARKDOWN)
	#create a new player
	p1 = Player(name, user, [], False)
	#create a new game
	game = Game(chat_id, p1, None, [], [], [])
    	chats[chat_id] = game
	chats[chat_id].giveCards(1)
	custom_keyboard = [[chats[chat_id].player1.hand[0].decode('utf-8')], [chats[chat_id].player1.hand[1].decode('utf-8')]]
	reply_markup = ReplyKeyboardMarkup(custom_keyboard, selective = True)
	update.message.reply_text(CARDS, reply_markup=reply_markup, parse_mode = ParseMode.MARKDOWN)

    else:
	if(chats[chat_id].player2 is None):
		p2 = Player(name, user, [], False)
		chats[chat_id].player2 = p2
		update.message.reply_text('``` Entry completed.\n' + name + ': 10 Lives.```', parse_mode = ParseMode.MARKDOWN)
		#once the players are set, lets give em cards
		bot.send_message(update.message.chat_id, GAME_STARTS, parse_mode = ParseMode.MARKDOWN)
		chats[chat_id].giveCards(2) #give 2 cards for the 1st time

		#display their current UPs and DOWNs
		bot.send_message(chat_id, chats[chat_id].player1.displayStatus(), parse_mode = ParseMode.MARKDOWN)
    		bot.send_message(chat_id, chats[chat_id].player2.displayStatus(), parse_mode = ParseMode.MARKDOWN)

		#here the player can see his hand
		custom_keyboard = [[chats[chat_id].player2.hand[0].decode('utf-8')], [chats[chat_id].player2.hand[1].decode('utf-8')]]
		reply_markup = ReplyKeyboardMarkup(custom_keyboard, selective = True) #turn selective ON so just this player receives the message
		update.message.reply_text(CARDS, reply_markup=reply_markup, parse_mode = ParseMode.MARKDOWN)

		#here we create the actual selection menu of the cards so the choice remains secret
		button_list = [
    			InlineKeyboardButton("Select 1st card", callback_data=0),
    			InlineKeyboardButton("Select 2nd card", callback_data=1),
		]
		reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=1))
		bot.send_message(chat_id, SELECT_CARD, reply_markup=reply_markup, parse_mode = ParseMode.MARKDOWN)
	else:
		update.message.reply_text('``` There are already two people playing.```', parse_mode = ParseMode.MARKDOWN)
    		
    print chats
	
def bet(bot, update):
    """Raise a bet"""
    user = update.message.from_user
    name = user.first_name
    chat_id = update.message.chat_id

    if(chats[chat_id].player1.user == user):
	lives = chats[chat_id].player1.lives
	bet = chats[chat_id].player1.bet
    elif(chats[chat_id].player2.user == user):
	lives = chats[chat_id].player2.lives
	bet = chats[chat_id].player2.bet
    else:
	lives = 0
	bet = 0
	update.message.reply_text('``` You are not a player.```', parse_mode = ParseMode.MARKDOWN)
    update.message.reply_text('``` You have: %i lives.```'%(lives), parse_mode = ParseMode.MARKDOWN)
    update.message.reply_text('``` You have bet: %i lives.```' %(bet), parse_mode = ParseMode.MARKDOWN)
    reply_markup=ForceReply(force_reply = True, selective = True)
    update.message.reply_text('``` Input lives to bet.```', reply_markup=reply_markup, parse_mode = ParseMode.MARKDOWN)
    return LIVES
	
def check(bot, update):
    user = update.message.from_user
    name = user.first_name
    update.message.reply_text(name+' checks.', parse_mode = ParseMode.MARKDOWN)
    if(chats[chat_id].player1.user == user):
	chats[chat_id].player1.check = True
    elif(chats[chat_id].player2.user == user):
	chats[chat_id].player2.check = True
    if(chats[chat_id].player1.check == True) and (chats[chat_id].player2.check == True):
	chats[chat_id].manageResult(choice1, choice2)
	

def fold(bot, update):
    """Fold"""
    user = update.message.from_user
    name = user.first_name
    chat_id = update.message.chat_id
    bot.send_message(chat_id, '``` ' + name + ' folds.```', parse_mode = ParseMode.MARKDOWN)
    return ConversationHandler.END


def quit(bot, update):
    """A player quits"""
    user = update.message.from_user
    name = user.first_name
    chat_id = update.message.chat_id
    bot.send_message(chat_id, '``` ' + name + ' quits. Game ends.```', parse_mode = ParseMode.MARKDOWN)
    if(chats.has_key(chat_id)):
	del chats[chat_id]
	

def scores(bot, update):
    """Prints all the matches in a game"""
    chat_id = update.message.chat_id
    bot.send_message(chat_id, chats[chat_id].displayScores(), parse_mode = ParseMode.MARKDOWN)

def endgame(bot, update):
    """End the game, like quit, but there are not winners nor losers"""
    chat_id = update.message.chat_id
    bot.send_message(chat_id, '``` Game ends.```', parse_mode = ParseMode.MARKDOWN)
    if(chats.has_key(chat_id)):
    	del chats[chat_id]
	
def zawa(bot, update, job_queue, chat_data):
    """Every 1 to 10 minutes (randomly) bot posts a zawa (ざわ) message. It's a switcher, typing it for the 1st enables and the 2nd time disables it"""
    chat_id = update.message.chat_id
    if('job' not in chat_data):
	bot.send_message(chat_id, '``` Zawa mode switched ON```', parse_mode = ParseMode.MARKDOWN)
	job = job_queue.run_repeating(callback_minute, 120, context=chat_id)
 	chat_data['job'] = job
    else:
	bot.send_message(chat_id, '``` Zawa mode switched OFF```', parse_mode = ParseMode.MARKDOWN)
	job = chat_data['job']
    	job.schedule_removal()
    	del chat_data['job']

def call(bot, update):
    """Lets keep the tutorial's examples from now"""
    check(bot, update)

def raiseB(bot, update):
    """Lets keep the tutorial's examples from now"""
    bet(bot, update)


def lives(bot, update):
    chat_id = update.message.chat_id
    user = update.message.from_user

    if(chats[chat_id].player1.user == user):
        chats[chat_id].player1.setBet(int(update.message.text))
    	update.message.reply_text('``` ' + update.message.from_user.first_name+' bets '+update.message.text + ' lives.```', parse_mode = ParseMode.MARKDOWN)
	custom_keyboard = [['CALL'], ['RAISE'], ['FOLD']]
	reply_markup = ReplyKeyboardMarkup(custom_keyboard, selective = False) #turn selective ON so just this player receives the message
	update.message.reply_text(CALL_RAISE_FOLD, reply_markup=reply_markup, parse_mode = ParseMode.MARKDOWN)
    elif(chats[chat_id].player2.user == user):
	chats[chat_id].player2.setBet(int(update.message.text))
	update.message.reply_text('``` ' + update.message.from_user.first_name+' bets '+update.message.text + ' lives.```', parse_mode = ParseMode.MARKDOWN)
	
	custom_keyboard = [['CALL'], ['RAISE'], ['FOLD']]
	reply_markup = ReplyKeyboardMarkup(custom_keyboard, selective = False) #turn selective ON so just this player receives the message
	update.message.reply_text(CALL_RAISE_FOLD, reply_markup=reply_markup, parse_mode = ParseMode.MARKDOWN)
    else:
	update.message.reply_text('``` You are not a player.```', parse_mode = ParseMode.MARKDOWN)
    return C_R_F

def echo(bot, update):
    """Log Errors caused by Updates."""
    print update.message.text

def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)

def card(bot, update):
    query = update.callback_query
    user = query.from_user
    chat_id = query.message.chat_id
    selected_card = query.data
    if(chats[chat_id].player1.card_played == []) or (chats[chat_id].player1.card_played == []):
    	bot.send_message(text="``` {} has selected a card.```".format(user.first_name), chat_id=query.message.chat_id, message_id=query.message.message_id, parse_mode = ParseMode.MARKDOWN)
	if (chats[chat_id].player1.user == user):
		chats[chat_id].player1.card_played = chats[chat_id].player1.hand[int(selected_card)]
		chats[chat_id].player1.hand.remove(chats[chat_id].player1.hand[int(selected_card)])
		print chats[chat_id].player1.card_played
	elif (chats[chat_id].player2.user == user):
		chats[chat_id].player2.card_played = chats[chat_id].player2.hand[int(selected_card)]
		chats[chat_id].player2.hand.remove(chats[chat_id].player1.hand[int(selected_card)])
    else:	
	if (chats[chat_id].player1.user == user and chats[chat_id].player1.card_played != []):
		bot.send_message(text="``` {} has already selected a card.```".format(user.first_name), chat_id=query.message.chat_id, message_id=query.message.message_id, parse_mode = ParseMode.MARKDOWN)
	elif (chats[chat_id].player2.user == user and chats[chat_id].player2.card_played != []):
		bot.send_message(text="``` {} has already selected a card.```".format(user.first_name), chat_id=query.message.chat_id, message_id=query.message.message_id, parse_mode = ParseMode.MARKDOWN)
	else:
 		bot.edit_message_text(text="``` {} has selected a card.```".format(user.first_name), chat_id=query.message.chat_id, message_id=query.message.message_id, parse_mode = ParseMode.MARKDOWN)
		custom_keyboard = [['CHECK'], ['BET']]
		reply_markup = ReplyKeyboardMarkup(custom_keyboard, selective = False)
		bot.send_message(chat_id, CARDS, reply_markup=reply_markup, parse_mode = ParseMode.MARKDOWN)
		

def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu

def callback_minute(bot, job):
    bot.send_message(chat_id = job.context, text=CATCH[randint(0,len(CATCH)-1)])

def main():

    updater = Updater(TOKEN)
    dp = updater.dispatcher
    j = updater.job_queue

    # big ass list of commands
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("rules", rules))
    dp.add_handler(CommandHandler("status", status))
    dp.add_handler(CommandHandler("participate", participate))
    dp.add_handler(CallbackQueryHandler(card))
    dp.add_handler(CommandHandler("disclaimer", disclaimer))
    dp.add_handler(CommandHandler("freeasinfreedom", freeasinfreedom))
    dp.add_handler(CommandHandler("check", check))
    dp.add_handler(CommandHandler("quit", quit))
    dp.add_handler(CommandHandler("endgame", endgame))
    dp.add_handler(CommandHandler("scores", scores))
    dp.add_handler(CommandHandler("zawa", zawa, pass_job_queue=True, pass_chat_data=True))
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('bet', bet)],

        states={
            LIVES: [MessageHandler(Filters.text, lives)],
  	    C_R_F: [RegexHandler('^(CALL)$', call), 
		RegexHandler('^(RAISE)$', raiseB),
		RegexHandler('^(FOLD)$', fold),]
	  
        },

        fallbacks=[CommandHandler('quit', quit)]
    )

    dp.add_handler(conv_handler)


    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
