# -*- coding: utf-8 -*-
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ParseMode, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler, Filters
import sys
import os
import logging
from datetime import datetime
from models import User, Show
from constants import help_msg, about_msg

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


def chosen_owns(update):
    try:
        user = User.select().where(User.user_id == get_user_id(update))[Show.get(user_id=get_user_id(update)).owns or 0]
    except IndexError:
        user = User.select().where(User.user_id == get_user_id(update))[0]
    return user


def is_changed(update):
    # check if user exist in DB (both tables). If not - create
    user, created = User.get_or_create(user_id=get_user_id(update))
    Show.get_or_create(user_id=get_user_id(update))
    # check if user changed own username. If so - update
    if user.username != get_username(update) or user.first_name != get_first_name(update) or user.last_name != get_last_name(update):
        for user in User.select().where(User.user_id == get_user_id(update)):
            user.username = get_username(update)
            user.first_name = get_first_name(update)
            user.last_name = get_last_name(update)
            user.updated = datetime.now()
            user.save()


def start_command(bot, update):
    is_changed(update)
    # logging
    logging.info('user_id: %d username: %s command: %s' % (get_user_id(update), get_username(update), 'start_command'))

    edit_or_show_kbd(bot, update)


def help_command(bot, update):
    is_changed(update)

    bot.sendMessage(chat_id=get_user_id(update), text=help_msg, parse_mode=ParseMode.HTML)
    # logging
    logging.info('user_id: %d username: %s command: %s' % (get_user_id(update), get_username(update), 'help_command'))


def about_command(bot, update):
    is_changed(update)

    bot.sendMessage(chat_id=get_user_id(update), text=about_msg,
                    parse_mode=ParseMode.HTML, disable_web_page_preview=True)
    # logging
    logging.info('user_id: %d username: %s command: %s' % (get_user_id(update), get_username(update), 'about_command'))


def user_created_report(bot):
    created_user = User.select().where(User.house > 0).order_by(User.created)[-1]
    bot.sendMessage(chat_id=3680016, parse_mode=ParseMode.HTML,
                    text=f'В базе создан новый пользователь:\n'
                    f'{created_user.user_created()}'
                    )
    bot.sendMessage(chat_id=422485737, parse_mode=ParseMode.HTML,
                    text=f'В базе создан новый пользователь:\n'
                    f'{created_user.user_created()}'
                    )


def edit_or_show_kbd(bot, update):
    """func show keyboard to chose: show neighbors or edit own info"""
    if User.get(user_id=get_user_id(update)).house and User.get(user_id=get_user_id(update)).section:
        keyboard = [[InlineKeyboardButton('Дивитись сусідів 👫', callback_data='show')],
                    [InlineKeyboardButton('Змінити свої дані ✏', callback_data='edit')],
                    [InlineKeyboardButton('Мій будинок 🏠', callback_data='house_neighbors'),
                     InlineKeyboardButton('Моя секція 🔢', callback_data='section_neighbors')]]
    else:
        keyboard = [[InlineKeyboardButton('Дивитись сусідів 👫', callback_data='show')],
                    [InlineKeyboardButton('Змінити свої дані ✏', callback_data='edit')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.sendMessage(chat_id=get_user_id(update), text='Меню:',
                    reply_markup=reply_markup, parse_mode=ParseMode.HTML)
    logging.info('user_id: %d command: %s' % (get_user_id(update), 'edit_or_show_kbd'))


def check_owns(bot, update):
    if update.callback_query.data == 'house_neighbors':
        if not len(User.select().where(User.user_id == get_user_id(update))) > 1:
            show_house(bot, update)
            return
    elif update.callback_query.data == 'section_neighbors':
        if not len(User.select().where(User.user_id == get_user_id(update))) > 1:
            show_section(bot, update)
            return

    if not User.get(user_id=get_user_id(update)).house:
        text = 'В якому Ви будинку ? 🏠 :'
        set_houses_kbd(bot, update, text)
    elif not len(User.select().where(User.user_id == get_user_id(update))) > 1:
        text = 'Змінюємо Ваші дані:\n' + User.get(
            user_id=get_user_id(update)).setting_str() + '\nВ якому Ви будинку ? 🏠 :'
        set_houses_kbd(bot, update, text)
    else:
        select_owns(bot, update)


def select_owns(bot, update):
    if update.callback_query.data == 'house_neighbors':
        text = 'Сусіди по якому будинку ? :'
        view_edit = 'view_my_house'
    elif update.callback_query.data == 'section_neighbors':
        text = 'Секція якої з Ваших квартир ? :'
        view_edit = 'view_my_secti'
    else:
        text = 'Яку адресу змінити? :'
        view_edit = 'edit'
    keyboard = []
    user_owns = User.select().where(User.user_id == get_user_id(update))
    for i, j in enumerate(user_owns):
        keyboard.append([InlineKeyboardButton(str(j.edit_btn_str()), callback_data='set_owns' + str(i) + view_edit)])
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.message.reply_text(text=text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)
    update.callback_query.answer()


def owns_selected(bot, update):
    view_edit = update.callback_query.data[-13:]
    owns = [s for s in list(update.callback_query.data) if s.isdigit()]
    owns = int(''.join(owns))
    user = Show.get(user_id=get_user_id(update))
    user.owns = owns
    user.save()
    update.callback_query.answer()

    if view_edit == 'view_my_house':
        show_house(bot, update)
    elif view_edit == 'view_my_secti':
        show_section(bot, update)
    else:
        user = User.select().where(User.user_id == get_user_id(update))[owns]
        text = 'Змінюємо Ваші дані:\n' + user.setting_str() + '\nВ якому Ви будинку ? 🏠 :'
        set_houses_kbd(bot, update, text)


def houses_kbd(bot, update):
    """func show keyboard to chose house to show"""
    keyboard = [[InlineKeyboardButton('Будинок 1', callback_data='p_h1'),
                 InlineKeyboardButton('Будинок 2', callback_data='p_h2')],
                [InlineKeyboardButton('Будинок 3', callback_data='p_h3'),
                 InlineKeyboardButton('Будинок 4', callback_data='p_h4')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.message.reply_text('Який будинок показати ? 🏠 :', reply_markup=reply_markup)
    update.callback_query.answer()
    logging.info('user_id: %d command: %s' % (get_user_id(update), 'houses_kbd'))


def section_kbd(bot, update):
    """func show keyboard to chose section to show"""
    user_query = Show.get(user_id=get_user_id(update))
    user_query.house = int(update.callback_query.data[3])
    user_query.save()

    keyboard = [[InlineKeyboardButton('Секція 1', callback_data='p_s1'),
                 InlineKeyboardButton('Секція 2', callback_data='p_s2')],
                [InlineKeyboardButton('Секція 3', callback_data='p_s3'),
                 InlineKeyboardButton('Секція 4', callback_data='p_s4')],
                [InlineKeyboardButton('Секція 5', callback_data='p_s5'),
                 InlineKeyboardButton('Секція 6', callback_data='p_s6')],
                [InlineKeyboardButton('Показати всіх в цьому будинку 🏠', callback_data='show_this_house')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.message.reply_text('Яку секцію показати ? 🔢 :', reply_markup=reply_markup)
    update.callback_query.answer()
    logging.info('user_id: %d command: %s' % (get_user_id(update), 'section_kbd'))


def save_params(bot, update):
    user_query = Show.get(user_id=get_user_id(update))
    user_query.section = int(update.callback_query.data[3])
    user_query.save()
    update.callback_query.answer()
    some_section = True
    show_section(bot, update, some_section)


def set_houses_kbd(bot, update, text=''):
    """func show keyboard to chose its own house"""
    if not User.get(user_id=get_user_id(update)).house:
        text = text
    elif len(User.select().where(User.user_id == get_user_id(update))) > 1:
        text = text
    else:
        text = text
    keyboard = [[InlineKeyboardButton('Будинок 1', callback_data='_h1'),
                 InlineKeyboardButton('Будинок 2', callback_data='_h2')],
                [InlineKeyboardButton('Будинок 3', callback_data='_h3'),
                 InlineKeyboardButton('Будинок 4', callback_data='_h4')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.message.reply_text(text=text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)

    update.callback_query.answer()
    logging.info('user_id: %d command: %s' % (get_user_id(update), 'set_houses_kbd'))


def set_section_kbd(bot, update):
    """func show keyboard to chose its own section"""
    user = chosen_owns(update)
    user.house = int(update.callback_query.data[2])
    user.updated = datetime.now()
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
    """func show keyboard to chose its own floor"""
    # user = User.get(user_id=get_user_id(update))
    user = chosen_owns(update)
    user.section = int(update.callback_query.data[2])
    user.updated = datetime.now()
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
    """func show message with ask to tell its own appartment"""
    floor = [s for s in list(update.callback_query.data) if s.isdigit()]
    floor = int(''.join(floor))

    user = chosen_owns(update)
    user.floor = floor
    user.updated = datetime.now()
    user.save()

    user_mode = Show.get(user_id=get_user_id(update))
    user_mode.msg_apart_mode = True
    user_mode.save()

    keyboard = [[InlineKeyboardButton('Не хочу вказувати квартиру', callback_data='_apart_reject')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.message.reply_text('Напишіть в повідомленні номер квартири, або нажміть кнопку відмови:',
                                             reply_markup=reply_markup)
    update.callback_query.answer()
    logging.info('user_id: %d command: %s' % (get_user_id(update), 'set_apartment_kbd'))


def apartment_save(bot, update):
    user_mode = Show.get(user_id=get_user_id(update))
    if user_mode.msg_apart_mode:
        text_success = '<b>Дякую, Ваші дані збережені</b>. Бажаєте подивитись сусідів?'
        text_failed = f'Вибачте, але номер квартири має містити <b>тільки цифри</b>.' \
            f'Спробуйте ще раз, або нажміть кнопку відмови'
        try:
            apartment = int(update.message.text)
            user = chosen_owns(update)
            user.apartment = apartment
            user.updated = datetime.now()
            user.save()
            bot.sendMessage(text=text_success, chat_id=get_user_id(update), parse_mode=ParseMode.HTML)
            logging.info('user_id: %d command: %s msg: %s' % (get_user_id(update), 'apart_save', update.message.text))
            user_mode.msg_apart_mode = False
            user_mode.save()

            user_created_report(bot)

            start_command(bot, update)
        except ValueError:
            keyboard = [[InlineKeyboardButton('Не хочу вказувати квартиру', callback_data='_apart_reject')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            update.message.reply_text(text=text_failed, reply_markup=reply_markup, parse_mode=ParseMode.HTML)
            logging.info('user_id: %d command: %s msg: %s' % (get_user_id(update), 'apart_save', update.message.text))
    else:
        bot.sendPhoto(chat_id=get_user_id(update), photo=open(os.path.join('img', 'maybe.jpg'), 'rb'),
                      caption=f'Я ще не розумію людської мови, але вже вчусь, і скоро буду розуміть деякі слова і фрази'
                      f'Краще скористайтесь однією з кнопок')
        logging.info('user_id: %d command: %s msg: %s' % (get_user_id(update), 'apart_save', update.message.text))
        start_command(bot, update)


def save_user_data(bot, update):
    update.callback_query.answer()
    bot.sendMessage(chat_id=get_user_id(update), parse_mode=ParseMode.HTML,
                    text='<b>Дякую, Ваші дані збережені</b>. Бажаєте подивитись сусідів?')

    user_mode = Show.get(user_id=get_user_id(update))
    user_mode.msg_apart_mode = False
    user_mode.save()

    user = chosen_owns(update)
    user.apartment = None
    user.updated = datetime.now()
    user.save()

    user_created_report(bot)

    start_command(bot, update)
    logging.info('user_id: %d command: %s' % (get_user_id(update), 'save_user_data'))


def show_house(bot, update):
    if update.callback_query.data == 'show_this_house':
        # if user want see selected house
        user_query = Show.get(user_id=get_user_id(update))
    else:
        # if user want see own house and have one
        user_query = chosen_owns(update)

    neighbors = []

    for i in range(1, 7):
        neighbors.append('\n' + '📭 <b>Секція '.rjust(30, ' ') + str(i) + '</b>' + '\n')
        for user in User.select().where(User.house == user_query.house, User.section == i).order_by(User.floor):
            neighbors.append(str(user) + '\n')

    show_list = ('<b>Мешканці будинку №' + str(user_query.house) + '</b>:\n'
                 + '{}' * len(neighbors)).format(*neighbors)

    # if len(show_list) < 2500:
    bot.sendMessage(chat_id=get_user_id(update), parse_mode=ParseMode.HTML, text=show_list)
    # else:
    #     part_1, part_2, part_3 = show_list.partition('<pre>       📭 Секція 4</pre>\n')
    #     bot.sendMessage(chat_id=get_user_id(update), parse_mode=ParseMode.HTML, text=part_1[:-2])
    #     bot.sendMessage(chat_id=get_user_id(update), parse_mode=ParseMode.HTML, text=part_2 + part_3)

    update.callback_query.answer()
    logging.info('user_id: %d command: %s' % (get_user_id(update), 'show_this_house'))
    start_command(bot, update)


def show_section(bot, update, some_section=False):
    if not some_section:
        user_query = chosen_owns(update)
    else:
        user_query = Show.get(user_id=get_user_id(update))

    query = User.select().where(
        User.house == user_query.house,
        User.section == user_query.section).order_by(User.floor)
    neighbors = [str(user) + '\n' for user in query]

    show_list = ('<b>Мешканці секції № ' + str(user_query.section) + ' Будинку № ' + str(user_query.house) + '</b>:\n'
                 + '{}' * len(neighbors)).format(*neighbors)

    bot.sendMessage(chat_id=get_user_id(update), parse_mode=ParseMode.HTML,
                    disable_web_page_preview=True, text=show_list)
    update.callback_query.answer()

    logging.info('user_id: %d command: %s' % (get_user_id(update), 'show_section'))
    start_command(bot, update)


def main():
    updater = Updater(KEY)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start_command))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("about", about_command))
    dispatcher.add_handler(MessageHandler(Filters.text, apartment_save))
    dispatcher.add_handler(CallbackQueryHandler(callback=houses_kbd, pattern='^show$'))
    dispatcher.add_handler(CallbackQueryHandler(callback=show_house, pattern='^show_this_house$'))
    # dispatcher.add_handler(CallbackQueryHandler(callback=show_section, pattern='^section_neighbors$'))
    dispatcher.add_handler(CallbackQueryHandler(callback=section_kbd, pattern='^p_h'))
    dispatcher.add_handler(CallbackQueryHandler(callback=save_params, pattern='^p_s'))
    # dispatcher.add_handler(CallbackQueryHandler(callback=set_houses_kbd, pattern='^edit$'))
    dispatcher.add_handler(CallbackQueryHandler(callback=check_owns, pattern='^edit$|^house_neighbors$|section_neighbors'))
    dispatcher.add_handler(CallbackQueryHandler(callback=owns_selected, pattern='^set_owns'))
    dispatcher.add_handler(CallbackQueryHandler(callback=set_section_kbd, pattern='^_h'))
    dispatcher.add_handler(CallbackQueryHandler(callback=set_floor_kbd, pattern='^_s'))
    dispatcher.add_handler(CallbackQueryHandler(callback=set_apartment_kbd, pattern='^_f'))
    dispatcher.add_handler(CallbackQueryHandler(callback=save_user_data, pattern='^_apart_reject$'))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
