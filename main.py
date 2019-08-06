# -*- coding: utf-8 -*-
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from config import log, log_chat, log_msg


KEY = '949481837:AAG3EbJzVdxIGkoznDPlmcjfj_GV1P2pZCk'

print('key ...' + KEY[-6:] + ' successfully used')


def func_1(bot, update):

    log.info(log_msg(update))

    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton('Меню', callback_data='_menu')]])
    bot.sendMessage(chat_id=update.effective_user.id, text='func 1 btn', parse_mode=ParseMode.HTML,
                    reply_markup=reply_markup)

    raise ValueError


def func_2(bot, update):

    log_chat.info(log_msg(update))

    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton('Меню', callback_data='_menu')]])
    bot.sendMessage(chat_id=update.effective_user.id, text='func 2 btn', parse_mode=ParseMode.HTML,
                    reply_markup=reply_markup)

    raise ValueError


def menu_kbd(bot, update):

    log.info(log_msg(update))
    text = '<b>Меню:</b>'
    keyboard = [[InlineKeyboardButton('func_1', callback_data='func_1')],
                [InlineKeyboardButton('func_2', callback_data='func_2')], ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.sendMessage(chat_id=update.effective_user.id, text=text, reply_markup=reply_markup,
                    parse_mode=ParseMode.HTML)


def main():
    updater = Updater(KEY)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", menu_kbd))
    dp.add_handler(CallbackQueryHandler(func_1, pattern='^func_1$'))
    dp.add_handler(CallbackQueryHandler(func_2, pattern='^func_2$'))
    dp.add_handler(CallbackQueryHandler(menu_kbd, pattern='^_menu$'))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
