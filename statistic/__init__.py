from config import log, log_msg
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


class Stat:
    def __init__(self, bot, update):
        log.info(log_msg(update))
        update.callback_query.answer()
        keyboard = [[InlineKeyboardButton('Назад', callback_data='statistics'),
                     InlineKeyboardButton('Меню', callback_data='_menu')]]
        self.reply_markup = InlineKeyboardMarkup(keyboard)
