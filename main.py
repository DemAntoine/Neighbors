# -*- coding: utf-8 -*-
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ParseMode, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler, Filters
import logging
import sys
from datetime import datetime
from models import User

KEY = sys.argv[1]
print('key ' + KEY[:8] + '... successfully used')

logging.basicConfig(
    filename="logfile.log", level=logging.INFO, datefmt='%y-%m-%d %H:%M:%S',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def get_user_id(update):
    try:
        user_id = update.message.from_user.id
    except AttributeError:
        user_id = update.callback_query.message.chat_id
    return user_id


def get_username(update):
    try:
        username = update.message.from_user.username
    except AttributeError:
        username = update.callback_query.message.from_user.username
    return username


def start_command(bot, update):
    # check if user exist in DB. If not - create
    user, created = User.get_or_create(user_id=get_user_id(update))
    # check if user changed own username. If so - update
    if user.username != get_username(update):
        user.username = get_username(update)
        user.updated = datetime.now()
    user.save()
    # send start_message
    # bot.sendMessage(chat_id=get_user_id(update), text='start_message', parse_mode=ParseMode.HTML)
    edit_or_show_kbd(bot, update)
    # logging
    logging.info('user_id: %d username: %s command: %s' % (get_user_id(update), get_username(update), 'start_command'))


def edit_or_show_kbd(bot, update):
    """func show keyboard to chose: show neighbors or edit own info"""
    keyboard = [[InlineKeyboardButton('Дивитись сусідів      👫', callback_data='show')],
                [InlineKeyboardButton('Змінити дані         ✏', callback_data='edit')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Виберіть:', reply_markup=reply_markup)
    # need to call this method to prevent multiple answer
    update.callback_query.answer()

    logging.info('user_id: %d command: %s' % (get_user_id(update), 'edit_or_show_kbd'))


def houses_kbd(bot, update):
    """func show keyboard to chose house to show"""
    keyboard = [[InlineKeyboardButton('Будинок 1', callback_data='h1'),
                 InlineKeyboardButton('Будинок 2', callback_data='h2')],
                [InlineKeyboardButton('Будинок 3', callback_data='h3'),
                 InlineKeyboardButton('Будинок 4', callback_data='h4')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.message.reply_text('Виберіть будинок:', reply_markup=reply_markup)

    update.callback_query.answer()

    logging.info('user_id: %d command: %s' % (get_user_id(update), 'houses_kbd'))


def section_kbd(bot, update):
    """func show keyboard to chose section to show"""
    keyboard = [[InlineKeyboardButton('Секція 1', callback_data='s1'),
                 InlineKeyboardButton('Секція 2', callback_data='s2')],
                [InlineKeyboardButton('Секція 3', callback_data='s3'),
                 InlineKeyboardButton('Секція 4', callback_data='s4')],
                [InlineKeyboardButton('Секція 5', callback_data='s5'),
                 InlineKeyboardButton('Секція 6', callback_data='s6')],
                [InlineKeyboardButton('Показати всіх в цьому будинку', callback_data='show_house')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.message.reply_text('Виберіть секцію:', reply_markup=reply_markup)

    update.callback_query.answer()

    logging.info('user_id: %d command: %s' % (get_user_id(update), 'section_kbd'))


def floor_kbd(bot, update):
    """func show keyboard to chose section to show"""
    keyboard = []
    floor = []
    for row in range(1, 6):
        for i in range(0, 5):
            floor.append([InlineKeyboardButton(str(row + i), callback_data='f'+str(row + 1))])

        keyboard.append(floor)
    keyboard.append([InlineKeyboardButton('Показати всіх в цій секції', callback_data='show_section')])
    # keyboard = [[InlineKeyboardButton('1', callback_data='s1'),
    #              InlineKeyboardButton('2', callback_data='s2'),
    #             InlineKeyboardButton('3', callback_data='s3'),
    #              InlineKeyboardButton('4', callback_data='s4'),
    #             InlineKeyboardButton('5', callback_data='s5')],
    #              [InlineKeyboardButton('6', callback_data='s6'),
    #               InlineKeyboardButton('2', callback_data='s2'),
    #               InlineKeyboardButton('3', callback_data='s3'),
    #               InlineKeyboardButton('3', callback_data='s3'),
    #               InlineKeyboardButton('4', callback_data='s4')],
    #             [InlineKeyboardButton('6', callback_data='s6'),
    #              InlineKeyboardButton('2', callback_data='s2'),
    #              InlineKeyboardButton('3', callback_data='s3'),
    #              InlineKeyboardButton('3', callback_data='s3'),
    #              InlineKeyboardButton('4', callback_data='s4')],
    #             [InlineKeyboardButton('6', callback_data='s6'),
    #              InlineKeyboardButton('2', callback_data='s2'),
    #              InlineKeyboardButton('3', callback_data='s3'),
    #              InlineKeyboardButton('3', callback_data='s3'),
    #              InlineKeyboardButton('4', callback_data='s4')],
    #             [InlineKeyboardButton('6', callback_data='s6'),
    #              InlineKeyboardButton('2', callback_data='s2'),
    #              InlineKeyboardButton('3', callback_data='s3'),
    #              InlineKeyboardButton('3', callback_data='s3'),
    #              InlineKeyboardButton('4', callback_data='s4')],
    #             [InlineKeyboardButton('Показати всіх в цій секції', callback_data='show_section')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.message.reply_text('Виберіть секцію:', reply_markup=reply_markup)

    update.callback_query.answer()

    logging.info('user_id: %d command: %s' % (get_user_id(update), 'floor_kbd'))


def main():
    updater = Updater(KEY)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start_command))
    dispatcher.add_handler(CallbackQueryHandler(callback=houses_kbd, pattern='show'))
    dispatcher.add_handler(CallbackQueryHandler(callback=section_kbd, pattern='^h'))
    dispatcher.add_handler(CallbackQueryHandler(callback=floor_kbd, pattern='^s'))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
