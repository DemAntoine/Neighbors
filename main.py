# -*- coding: utf-8 -*-
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ParseMode, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler, Filters
import logging
import sys
from datetime import datetime
from models import User, Show

KEY = sys.argv[1]
print('key ' + KEY[:8] + '... successfully used')

logging.basicConfig(
    filename="logfile.log", level=logging.INFO, datefmt='%y-%m-%d %H:%M:%S',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def get_user_id(update):
    try:
        user_id = update.message.chat_id
    except AttributeError:
        user_id = update.callback_query.message.chat_id
    return user_id


def get_username(update):
    try:
        username = update.message.chat.username
    except AttributeError:
        username = update.callback_query.message.chat.username
    return username


def get_first_name(update):
    try:
        first_name = update.message.chat.first_name
    except AttributeError:
        first_name = update.callback_query.message.chat.first_name
    return first_name


def get_last_name(update):
    try:
        last_name = update.message.chat.last_name
    except AttributeError:
        last_name = update.callback_query.message.chat.last_name
    return last_name


def start_command(bot, update):
    # check if user exist in DB (both tables). If not - create
    user, created = User.get_or_create(user_id=get_user_id(update))
    Show.get_or_create(user_id=get_user_id(update))
    # check if user changed own username. If so - update
    if user.username != get_username(update) or user.first_name != get_first_name(update):
        user.username = get_username(update)
        user.first_name = get_first_name(update)
        user.last_name = get_last_name(update)
        user.updated = datetime.now()
        user.save()
    
    # logging
    logging.info('user_id: %d username: %s command: %s' % (get_user_id(update), get_username(update), 'start_command'))
    
    edit_or_show_kbd(bot, update)
    

def edit_or_show_kbd(bot, update):
    """func show keyboard to chose: show neighbors or edit own info"""
    keyboard = [[InlineKeyboardButton('Дивитись сусідів 👫', callback_data='show')],
                [InlineKeyboardButton('Змінити свої дані ✏', callback_data='edit')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.sendMessage(chat_id=get_user_id(update), text='Що будемо робити ?',
                    reply_markup=reply_markup, parse_mode=ParseMode.HTML)
    logging.info('user_id: %d command: %s' % (get_user_id(update), 'edit_or_show_kbd'))


def houses_kbd(bot, update):
    """func show keyboard to chose house to show"""
    keyboard = [[InlineKeyboardButton('Будинок 1', callback_data='h1'),
                 InlineKeyboardButton('Будинок 2', callback_data='h2')],
                [InlineKeyboardButton('Будинок 3', callback_data='h3'),
                 InlineKeyboardButton('Будинок 4', callback_data='h4')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.message.reply_text('Який будинок показати ? 🏠 :', reply_markup=reply_markup)
    update.callback_query.answer()
    logging.info('user_id: %d command: %s' % (get_user_id(update), 'houses_kbd'))


def section_kbd(bot, update):
    """func show keyboard to chose section to show"""
    user_query = Show.get(user_id=get_user_id(update))
    user_query.house = int(update.callback_query.data[1])
    user_query.save()

    keyboard = [[InlineKeyboardButton('Секція 1', callback_data='s1'),
                 InlineKeyboardButton('Секція 2', callback_data='s2')],
                [InlineKeyboardButton('Секція 3', callback_data='s3'),
                 InlineKeyboardButton('Секція 4', callback_data='s4')],
                [InlineKeyboardButton('Секція 5', callback_data='s5'),
                 InlineKeyboardButton('Секція 6', callback_data='s6')],
                [InlineKeyboardButton('Показати всіх в цьому будинку 🏠', callback_data='show_this_house')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.message.reply_text('Яку секцію показати ? 🔢 :', reply_markup=reply_markup)
    update.callback_query.answer()
    logging.info('user_id: %d command: %s' % (get_user_id(update), 'section_kbd'))


def save_params(bot, update):
    user_query = Show.get(user_id=get_user_id(update))
    user_query.section = int(update.callback_query.data[1])
    user_query.save()
    update.callback_query.answer()
    show_section(bot, update)


def set_houses_kbd(bot, update):
    """func show keyboard to chose house to show"""
    keyboard = [[InlineKeyboardButton('Будинок 1', callback_data='_h1'),
                 InlineKeyboardButton('Будинок 2', callback_data='_h2')],
                [InlineKeyboardButton('Будинок 3', callback_data='_h3'),
                 InlineKeyboardButton('Будинок 4', callback_data='_h4')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.message.reply_text('В якому Ви будинку ? 🏠 :', reply_markup=reply_markup)
    update.callback_query.answer()
    logging.info('user_id: %d command: %s' % (get_user_id(update), 'set_houses_kbd'))


def set_section_kbd(bot, update):
    """func show keyboard to chose section to show"""
    user = User.get(user_id=get_user_id(update))
    user.house = int(update.callback_query.data[2])
    user.save()

    keyboard = [[InlineKeyboardButton('Секція 1', callback_data='_s1'),
                 InlineKeyboardButton('Секція 2', callback_data='_s2')],
                [InlineKeyboardButton('Секція 3', callback_data='_s3'),
                 InlineKeyboardButton('Секція 4', callback_data='_s4')],
                [InlineKeyboardButton('Секція 5', callback_data='_s5'),
                 InlineKeyboardButton('Секція 6', callback_data='_s6')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.message.reply_text('В якій Ви секції ? 🔢 :', reply_markup=reply_markup)
    update.callback_query.answer()
    logging.info('user_id: %d command: %s' % (get_user_id(update), 'set_section_kbd'))


def set_floor_kbd(bot, update):
    """func show keyboard to chose section to show"""
    user = User.get(user_id=get_user_id(update))
    user.section = int(update.callback_query.data[2])
    user.save()

    keyboard = []
    floor = 1
    for row in range(0, 5):
        floors = []
        for i in range(1, 6):
            floors.append(InlineKeyboardButton(str(floor), callback_data='_f' + str(floor)))
            floor += 1
        keyboard.append(floors)

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.message.reply_text('На якому Ви поверсі ? 🧗 :', reply_markup=reply_markup)
    update.callback_query.answer()
    logging.info('user_id: %d command: %s' % (get_user_id(update), 'set_floor_kbd'))


def set_apartment_kbd(bot, update):
    floor = [s for s in list(update.callback_query.data) if s.isdigit()]
    floor = int(''.join(floor))

    user = User.get(user_id=get_user_id(update))
    user.floor = floor
    user.save()

    keyboard = [[InlineKeyboardButton('Не хочу вказувати квартиру', callback_data='_apart_reject')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.message.reply_text('Напишіть в повідомленні номер квартири, або нажміть кнопку відмови:',
                                             reply_markup=reply_markup)
    update.callback_query.answer()
    logging.info('user_id: %d command: %s' % (get_user_id(update), 'set_apartment_kbd'))


def apartment_save(bot, update):
    
    text_success = '<b>Дякую, Ваші дані збережені</b>. Бажаєте подивитись сусідів?'
    text_failed = 'Вибачте, але номер квартири має містити <b>тільки цифри</b>. Спробуйте ще раз, або нажміть кнопку відмови'
    try:
        apartment = int(update.message.text)
        user = User.get(user_id=get_user_id(update))
        user.apartment = apartment
        user.save()
        bot.sendMessage(text=text_success, chat_id=get_user_id(update), parse_mode=ParseMode.HTML)
        logging.info('user_id: %d command: %s msg: %s' % (get_user_id(update), 'apart_save', update.message.text))
        start_command(bot, update)
    except ValueError:
        keyboard = [[InlineKeyboardButton('Не хочу вказувати квартиру', callback_data='_apart_reject')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(text=text_failed, reply_markup=reply_markup, parse_mode=ParseMode.HTML)
        logging.info('user_id: %d command: %s msg: %s' % (get_user_id(update), 'apart_save', update.message.text))


def save_user_data(bot, update):
    update.callback_query.answer()
    bot.sendMessage(chat_id=get_user_id(update), parse_mode=ParseMode.HTML, 
                    text='<b>Дякую, Ваші дані збережені</b>. Бажаєте подивитись сусідів?')
    start_command(bot, update)
    logging.info('user_id: %d command: %s' % (get_user_id(update), 'save_user_data'))
    

def show_this_house(bot, update):
    user_query = Show.get(user_id=get_user_id(update))
    neighbors = []

    for i in range(1, 7):
        neighbors.append('\n' + '📭 <b>Секція '.rjust(10, ' ') + str(i) + '</b>' + '\n')
        for user in User.select().where(User.house == user_query.house, User.section == i).order_by(User.floor):
            neighbors.append(str(user) + '\n')
    
    show_list = ('<b>Мешканці будинку №' + str(user_query.house) + '</b>:\n'
                 + '{}' * len(neighbors)).format(*neighbors)
    
    # for i in range(70):
    #     neighbors.append('<a href="tg://user?id=3680016">inline mention of a user</a>\n')
    #     show_list = ('<b>Мешканці будинку №' + str(user_query.house) + '</b>:\n'
    #              + '{}' * len(neighbors)).format(*neighbors)
    
    print(len(show_list))
    
    update.callback_query.answer()
    bot.sendMessage(chat_id=get_user_id(update), parse_mode=ParseMode.HTML,
                    disable_web_page_preview=True, text=show_list)
    
    logging.info('user_id: %d command: %s' % (get_user_id(update), 'show_this_house'))
    start_command(bot, update)


def show_section(bot, update):
    user_query = Show.get(user_id=get_user_id(update))
    query = User.select().where(
        User.house == user_query.house,
        User.section == user_query.section)
    neighbors = [str(user) + '\n' for user in query]

    show_list = ('<b>Мешканці секції №' + str(user_query.section) + '</b>:\n'
                 + '{}' * len(neighbors)).format(*neighbors)

    bot.sendMessage(chat_id=get_user_id(update), parse_mode=ParseMode.HTML,
                    disable_web_page_preview=True, text=show_list)
    
    logging.info('user_id: %d command: %s' % (get_user_id(update), 'show_section'))
    start_command(bot, update)


def main():
    updater = Updater(KEY)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start_command))
    dispatcher.add_handler(MessageHandler(Filters.text, apartment_save))
    dispatcher.add_handler(CallbackQueryHandler(callback=houses_kbd, pattern='^show$'))
    dispatcher.add_handler(CallbackQueryHandler(callback=show_this_house, pattern='^show_this_house$'))
    dispatcher.add_handler(CallbackQueryHandler(callback=section_kbd, pattern='^h'))
    dispatcher.add_handler(CallbackQueryHandler(callback=save_params, pattern='^s'))
    dispatcher.add_handler(CallbackQueryHandler(callback=set_houses_kbd, pattern='^edit'))
    dispatcher.add_handler(CallbackQueryHandler(callback=set_section_kbd, pattern='^_h'))
    dispatcher.add_handler(CallbackQueryHandler(callback=set_floor_kbd, pattern='^_s'))
    dispatcher.add_handler(CallbackQueryHandler(callback=set_apartment_kbd, pattern='^_f'))
    dispatcher.add_handler(CallbackQueryHandler(callback=save_user_data, pattern='^_apart_reject$'))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
