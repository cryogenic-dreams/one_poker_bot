# -*- coding: utf-8 -*-
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler, RegexHandler
from telegram import ReplyKeyboardMarkup, ParseMode, InlineKeyboardButton, InlineKeyboardMarkup, ForceReply
import logging
from random import randint
from Player import Player
from Game import Game
from strings import Strings
from gentlebot import MQBot
from telegram.ext import messagequeue as mq


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

chats = {}
PARTICIPATE, BET_CHECK, CARD, LIVES, C_R_F, Y_N = range(6)


def start(bot, update):
    update.message.reply_text(Strings.GREETINGS, parse_mode=ParseMode.MARKDOWN)
    update.message.reply_text(Strings.GREETINGS2, parse_mode=ParseMode.MARKDOWN)


def help(bot, update):
    update.message.reply_text(Strings.HELP)


def rules(bot, update):
    update.message.reply_text(Strings.RULES)


def disclaimer(bot, update):
    update.message.reply_text(Strings.DISCLAIMER)


def freeasinfreedom(bot, update):
    bot.send_message(update.message.chat_id, Strings.FREEDOM)


def status(bot, update):
    """Send the UPs and DOWNs of the players when the command /status is issued."""
    chat_id = update.message.chat_id
    if chats.get(chat_id) is None:
        bot.send_message(chat_id, Strings.NOT_STARTED, parse_mode=ParseMode.MARKDOWN)
    else:
        update.message.reply_text(chats[chat_id].player1.displayStatus(), parse_mode=ParseMode.MARKDOWN)
        update.message.reply_text(chats[chat_id].player2.displayStatus(), parse_mode=ParseMode.MARKDOWN)


def participate(bot, update):
    """
    take id and name of the user
    after second input, start the actual game
    """
    chat_id = update.message.chat_id
    user = update.message.from_user
    name = user.first_name
    if chats.get(chat_id) is None:
        update.message.reply_text(Strings.ENTRY % name,
                                  parse_mode=ParseMode.MARKDOWN)
        # create a new player
        p1 = Player(name, user, update.message.message_id)
        # create a new game
        game = Game(chat_id, p1, None)
        chats[chat_id] = game
        return PARTICIPATE
    else:
        if chats[chat_id].player2 is None:
            p2 = Player(name, user, update.message.message_id)
            chats[chat_id].player2 = p2
            update.message.reply_text(Strings.ENTRY % name,
                                      parse_mode=ParseMode.MARKDOWN)
            # once the players are set, lets give em cards
            bot.send_message(update.message.chat_id,
                             Strings.GAME_STARTS,
                             parse_mode=ParseMode.MARKDOWN)
            chats[chat_id].giveCards(1)  # give 2 cards for the 1st time
            chats[chat_id].giveCards(1)
            # display their current UPs and DOWNs
            show_cards(bot, chat_id)
            return CARD
        else:
            update.message.reply_text(Strings.ALREADY, parse_mode=ParseMode.MARKDOWN)


def show_cards(bot, chat_id):
    bot.send_message(chat_id,
                     chats[chat_id].player1.displayStatus(),
                     parse_mode=ParseMode.MARKDOWN,
                     isgroup=True)

    bot.send_message(chat_id,
                     chats[chat_id].player2.displayStatus(),
                     parse_mode=ParseMode.MARKDOWN,
                     isgroup=True)

    # here the player can see his hand
    custom_keyboard = [[chats[chat_id].player1.hand[0].decode('utf-8')],
                       [chats[chat_id].player1.hand[1].decode('utf-8')]]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard,
                                       selective=True)
    # turn selective ON so just this player receives the message

    bot.send_message(chat_id,
                     Strings.CARDS,
                     reply_markup=reply_markup,
                     reply_to_message_id=chats[chat_id].player1.reply_id,
                     parse_mode=ParseMode.MARKDOWN,
                     timeout=20.0,
                     isgroup=True)

    custom_keyboard = [[chats[chat_id].player2.hand[0].decode('utf-8')],
                       [chats[chat_id].player2.hand[1].decode('utf-8')]]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard,
                                       selective=True)
    bot.send_message(chat_id,
                     Strings.CARDS,
                     reply_markup=reply_markup,
                     reply_to_message_id=chats[chat_id].player2.reply_id,
                     parse_mode=ParseMode.MARKDOWN,
                     timeout=20.0,
                     isgroup=True)

    # here we create the actual selection menu of the cards so the choice remains secret

    bot.send_message(chat_id,
                     Strings.SELECT_CARD,
                     reply_markup=REPLY_MARKUP,
                     parse_mode=ParseMode.MARKDOWN,
                     isgroup=True)


def bet(bot, update):
    print 'user bets'
    user = update.message.from_user
    name = user.first_name
    chat_id = update.message.chat_id

    if chats[chat_id].player1.user == user:
        lives = chats[chat_id].player1.lives
        bet = chats[chat_id].player1.bet
    elif chats[chat_id].player2.user == user:
        lives = chats[chat_id].player2.lives
        bet = chats[chat_id].player2.bet
    else:
        lives = 0
        bet = 0
        update.message.reply_text(Strings.NOT_PLAYER,
                                  parse_mode=ParseMode.MARKDOWN)
    update.message.reply_text(Strings.P_LIVES % (name, lives),
                              parse_mode=ParseMode.MARKDOWN)
    update.message.reply_text(Strings.P_BET % (name, bet),
                              parse_mode=ParseMode.MARKDOWN)
    reply_markup = ForceReply(force_reply=True,
                              selective=True)
    update.message.reply_text(Strings.INPUT_BET,
                              reply_markup=reply_markup,
                              parse_mode=ParseMode.MARKDOWN)
    return LIVES


def check(bot, update):
    user = update.message.from_user
    name = user.first_name
    chat_id = update.message.chat_id

    if chats[chat_id].player1.user == user:
        chats[chat_id].player1.check = True
        update.message.reply_text(Strings.P_CHECKS % name,
                                  parse_mode=ParseMode.MARKDOWN)
        return BET_CHECK
    elif chats[chat_id].player2.user == user:
        chats[chat_id].player2.check = True
        update.message.reply_text(Strings.P_CHECKS % name,
                                  parse_mode=ParseMode.MARKDOWN)
        return BET_CHECK
    if chats[chat_id].player1.check and chats[chat_id].player2.check:
        bot.send_message(chat_id,
                         Strings.CHECK,
                         parse_mode=ParseMode.MARKDOWN,
                         isgroup=True)
        result = chats[chat_id].manageResult(chats[chat_id].player1.card_played,
                                             chats[chat_id].player2.card_played)
        bot.send_message(chat_id,
                         result,
                         parse_mode=ParseMode.MARKDOWN,
                         isgroup=True)

        if chats[chat_id].player1.lives == 0:
            if chats[chat_id].player1.red_lives == 0:
                bot.send_message(chat_id,
                                 Strings.END,
                                 parse_mode=ParseMode.MARKDOWN,
                                 isgroup=True)
                bot.send_message(chat_id,
                                 Strings.WIN % chats[chat_id].player2.name,
                                 parse_mode=ParseMode.MARKDOWN,
                                 isgroup=True)
                return ConversationHandler.END
            else:
                # wanna bet your own life?
                red_life_bet(bot, chat_id, chats[chat_id].player1)
                return Y_N
        elif chats[chat_id].player2.lives == 0:
            if chats[chat_id].player2.red_lives == 0:
                bot.send_message(chat_id,
                                 Strings.END,
                                 parse_mode=ParseMode.MARKDOWN,
                                 isgroup=True)
                bot.send_message(chat_id,
                                 Strings.WIN % chats[chat_id].player1.name,
                                 parse_mode=ParseMode.MARKDOWN,
                                 isgroup=True)
                return ConversationHandler.END
            else:
                # wanna bet your own life
                red_life_bet(bot, chat_id, chats[chat_id].player2)
                return Y_N
        else:
            show_cards(bot, chat_id)
            return CARD


def red_life_bet(bot, chat_id, player):
    custom_keyboard = [['YES'], ['NO']]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard,
                                       selective=True)  # turn selective ON so just this player receives the message
    bot.send_message(chat_id,
                     Strings.R_LIFE,
                     reply_markup=reply_markup,
                     reply_to_message_id=player.reply_id,
                     parse_mode=ParseMode.MARKDOWN,
                     isgroup=True)


def chose_red_life(bot, update):
    chat_id = update.message.chat_id
    choice = update.message.text
    if chats[chat_id].player1.lives == 0:
        if choice == 'YES':
            chats[chat_id].player1.lives = 1
            chats[chat_id].player1.red_lives = 0
            bot.send_message(chat_id,
                             Strings.R_GAME % chats[chat_id].player1.name,
                             parse_mode=ParseMode.MARKDOWN, isgroup=True)
            chats[chat_id].giveCards(2)
            show_cards(bot, chat_id)
            return CARD
        else:
            bot.send_message(chat_id,
                             Strings.END,
                             parse_mode=ParseMode.MARKDOWN, isgroup=True)
            bot.send_message(chat_id,
                             Strings.WIN % chats[chat_id].player2.name,
                             parse_mode=ParseMode.MARKDOWN, isgroup=True)
            return ConversationHandler.END
    elif chats[chat_id].player2.lives == 0:
        if choice == 'YES':
            chats[chat_id].player2.lives = 1
            chats[chat_id].player2.red_lives = 0
            bot.send_message(chat_id,
                             Strings.R_GAME % chats[chat_id].player2.name,
                             parse_mode=ParseMode.MARKDOWN, isgroup=True)
            chats[chat_id].giveCards(1)
            show_cards(bot, chat_id)
            return CARD
        else:
            bot.send_message(chat_id,
                             Strings.END,
                             parse_mode=ParseMode.MARKDOWN, isgroup=True)
            bot.send_message(chat_id,
                             Strings.WIN % chats[chat_id].player1.name,
                             parse_mode=ParseMode.MARKDOWN, isgroup=True)
            return ConversationHandler.END


def fold(bot, update):
    """Fold"""
    user = update.message.from_user
    name = user.first_name
    chat_id = update.message.chat_id
    bot.send_message(chat_id,
                     Strings.P_FOLDS % name,
                     parse_mode=ParseMode.MARKDOWN,
                     isgroup=True)
    if chats[chat_id].player1.user == user:
        winner = 2
    elif chats[chat_id].player2.user == user:
        winner = 1
    else:
        return C_R_F
    result = chats[chat_id].manageResult(chats[chat_id].player1.card_played,
                                         chats[chat_id].player2.card_played, winner)
    bot.send_message(chat_id,
                     result,
                     parse_mode=ParseMode.MARKDOWN,
                     isgroup=True)

    if chats[chat_id].player1.lives == 0:
        if chats[chat_id].player1.red_lives == 0:
            bot.send_message(chat_id,
                             Strings.END,
                             parse_mode=ParseMode.MARKDOWN,
                             isgroup=True)
            bot.send_message(chat_id,
                             Strings.WIN % chats[chat_id].player2.name,
                             parse_mode=ParseMode.MARKDOWN,
                             isgroup=True)
            return ConversationHandler.END
        else:
            # wanna bet your own life?
            red_life_bet(bot, chat_id, chats[chat_id].player1)
            return Y_N
    elif chats[chat_id].player2.lives == 0:
        if chats[chat_id].player2.red_lives == 0:
            bot.send_message(chat_id,
                             Strings.END,
                             parse_mode=ParseMode.MARKDOWN,
                             isgroup=True)
            bot.send_message(chat_id,
                             Strings.WIN % chats[chat_id].player1.name,
                             parse_mode=ParseMode.MARKDOWN,
                             isgroup=True)
            return ConversationHandler.END
        else:
            # wanna bet your own life
            red_life_bet(bot, chat_id, chats[chat_id].player2)
            return Y_N
    else:
        show_cards(bot, chat_id)
        return CARD


def quit(bot, update):
    """A player quits"""
    user = update.message.from_user
    name = user.first_name
    chat_id = update.message.chat_id
    bot.send_message(chat_id,
                     Strings.P_QUITS % name,
                     parse_mode=ParseMode.MARKDOWN,
                     isgroup=True)
    if chat_id in chats:
        del chats[chat_id]
        return ConversationHandler.END


def scores(bot, update):
    """Prints all the matches in a game"""
    chat_id = update.message.chat_id
    bot.send_message(chat_id,
                     chats[chat_id].displayScores(),
                     parse_mode=ParseMode.MARKDOWN,
                     isgroup=True)


def endgame(bot, update):
    """
    End the game, like quit, but there are neither winners nor losers
    """
    chat_id = update.message.chat_id
    bot.send_message(chat_id,
                     Strings.END,
                     parse_mode=ParseMode.MARKDOWN, isgroup=True)
    if chat_id in chats:
        del chats[chat_id]
        return ConversationHandler.END


def zawa(bot, update, job_queue, chat_data):
    """
    Every 1 to 10 minutes (randomly) bot posts a zawa (ざわ) message.
    It's a switcher, typing it for the 1st enables and the 2nd time disables it
    """
    chat_id = update.message.chat_id
    if 'job' not in chat_data:
        bot.send_message(chat_id,
                         Strings.ZAWA_ON,
                         parse_mode=ParseMode.MARKDOWN, isgroup=True)
        job = job_queue.run_repeating(callback_minute,
                                      randint(60, 600),
                                      context=chat_id)
        chat_data['job'] = job
    else:
        bot.send_message(chat_id,
                         Strings.ZAWA_OFF,
                         parse_mode=ParseMode.MARKDOWN, isgroup=True)
        job = chat_data['job']
        job.schedule_removal()
        del chat_data['job']


def lives(bot, update):
    chat_id = update.message.chat_id
    user = update.message.from_user
    lives_bet = int(update.message.text)
    name = user.first_name

    if chats[chat_id].player1.user == user:
        chats[chat_id].player1.setBet(lives_bet)
        update.message.reply_text(Strings.LIVES_BET % (name, lives_bet),
                                  parse_mode=ParseMode.MARKDOWN)

        custom_keyboard = [['CALL'], ['RAISE'], ['FOLD']]
        reply_markup = ReplyKeyboardMarkup(custom_keyboard,
                                           selective=False)
        # turn selective ON so just this player receives the message
        update.message.reply_text(Strings.CALL_RAISE_FOLD,
                                  reply_markup=reply_markup,
                                  parse_mode=ParseMode.MARKDOWN)
        return C_R_F

    elif chats[chat_id].player2.user == user:
        chats[chat_id].player2.setBet(lives_bet)
        update.message.reply_text(Strings.LIVES_BET % (name, lives_bet),
                                  parse_mode=ParseMode.MARKDOWN)

        custom_keyboard = [['CALL'], ['RAISE'], ['FOLD']]
        reply_markup = ReplyKeyboardMarkup(custom_keyboard,
                                           selective=False)
        # turn selective ON so just this player receives the message
        update.message.reply_text(Strings.CALL_RAISE_FOLD,
                                  reply_markup=reply_markup,
                                  parse_mode=ParseMode.MARKDOWN)
        return C_R_F
    else:
        update.message.reply_text(Strings.NOT_PLAYER,
                                  parse_mode=ParseMode.MARKDOWN)
        return LIVES


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def card(bot, update):
    query = update.callback_query
    user = query.from_user
    chat_id = query.message.chat_id
    selected_card = query.data
    if (chats[chat_id].player1.card_played == []) and (chats[chat_id].player2.card_played == []):
        bot.send_message(text=Strings.CARD_SELECTED.format(user.first_name),
                         chat_id=query.message.chat_id,
                         message_id=query.message.message_id,
                         parse_mode=ParseMode.MARKDOWN,
                         isgroup=True)

        if chats[chat_id].player1.user == user:
            chats[chat_id].player1.card_played = chats[chat_id].player1.hand[int(selected_card)]
            chats[chat_id].player1.hand.remove(chats[chat_id].player1.hand[int(selected_card)])

        elif chats[chat_id].player2.user == user:
            chats[chat_id].player2.card_played = chats[chat_id].player2.hand[int(selected_card)]
            chats[chat_id].player2.hand.remove(chats[chat_id].player2.hand[int(selected_card)])
        return CARD
    else:
        if chats[chat_id].player1.user == user and chats[chat_id].player1.card_played != []:
            bot.send_message(text=Strings.CARD_SELECTED2.format(user.first_name),
                             chat_id=query.message.chat_id,
                             message_id=query.message.message_id,
                             parse_mode=ParseMode.MARKDOWN, isgroup=True)
            return CARD
        elif chats[chat_id].player2.user == user and chats[chat_id].player2.card_played != []:
            bot.send_message(text=Strings.CARD_SELECTED2.format(user.first_name),
                             chat_id=query.message.chat_id,
                             message_id=query.message.message_id,
                             parse_mode=ParseMode.MARKDOWN, isgroup=True)
            return CARD
        else:
            if chats[chat_id].player1.user == user:
                chats[chat_id].player1.card_played = chats[chat_id].player1.hand[int(selected_card)]
                chats[chat_id].player1.hand.remove(chats[chat_id].player1.hand[int(selected_card)])

            elif chats[chat_id].player2.user == user:
                chats[chat_id].player2.card_played = chats[chat_id].player2.hand[int(selected_card)]
                chats[chat_id].player2.hand.remove(chats[chat_id].player2.hand[int(selected_card)])

            bot.edit_message_text(text=Strings.CARD_SELECTED.format(user.first_name),
                                  chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  parse_mode=ParseMode.MARKDOWN)
            bot.send_message(chat_id,
                             Strings.SELECTION_COMPLETED,
                             parse_mode=ParseMode.MARKDOWN, isgroup=True)
            custom_keyboard = [['CHECK'], ['BET']]
            reply_markup = ReplyKeyboardMarkup(custom_keyboard, selective=False)
            bot.send_message(chat_id,
                             Strings.QUESTION,
                             reply_markup=reply_markup,
                             parse_mode=ParseMode.MARKDOWN, isgroup=True)
            return BET_CHECK


def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu


def callback_minute(bot, job):
    bot.send_message(chat_id=job.context, text=Strings.CATCH[randint(0, len(Strings.CATCH) - 1)], isgroup=True)


def main():

    q = mq.MessageQueue()
    queuebot = MQBot(mqueue=q)
    updater = Updater(bot=queuebot)
    dp = updater.dispatcher

    # big ass list of commands
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("rules", rules))
    dp.add_handler(CommandHandler("status", status))
    dp.add_handler(CommandHandler("disclaimer", disclaimer))
    dp.add_handler(CommandHandler("freeasinfreedom", freeasinfreedom))
    dp.add_handler(CommandHandler("endgame", endgame))
    dp.add_handler(CommandHandler("scores", scores))
    dp.add_handler(CommandHandler("zawa", zawa, pass_job_queue=True, pass_chat_data=True))
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("participate", participate)],

        states={
            PARTICIPATE: [CommandHandler("participate", participate)],
            CARD: [CallbackQueryHandler(card)],
            BET_CHECK: [RegexHandler('^(BET)$', bet),
                        RegexHandler('^(CHECK)$', check)],
            LIVES: [RegexHandler('^[0-9]+$', lives)],
            C_R_F: [RegexHandler('^(CALL)$', check),
                    RegexHandler('^(RAISE)$', bet),
                    RegexHandler('^(FOLD)$', fold)],
            Y_N: [RegexHandler('^(YES|NO)$', chose_red_life)]
        },

        fallbacks=[CommandHandler("quit", quit)],
        per_user=False,
        per_chat=True
    )
    dp.add_handler(conv_handler)

    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()


button_list = [
        InlineKeyboardButton(Strings.MENU1, callback_data=0),
        InlineKeyboardButton(Strings.MENU2, callback_data=1),
    ]
REPLY_MARKUP = InlineKeyboardMarkup(build_menu(button_list, n_cols=1))

if __name__ == '__main__':
    main()
