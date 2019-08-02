# -*- coding: utf-8 -*-
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, InputMediaPhoto, ChatAction
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler, Filters, run_async
from telegram.error import (TelegramError, Unauthorized, BadRequest, TimedOut, NetworkError)
import sys
import os
import time
import re
import shutil
import matplotlib.pyplot as plt
from datetime import datetime
from models import Show, Jubilee, Parking, UserName, Own
from constants import help_msg, about_msg, building_msg, houses_arr, greeting_msg
from classes import filt_integers, filt_call_err, block_filter
from config import log, log_chat, log_msg
from functools import wraps
from statistic.stat_classes import CommonStat, Charts, ChatStat

KEY = sys.argv[1]
ADMIN_ID = sys.argv[2]
print('key ...' + KEY[-6:] + ' successfully used')


def restricted(func):
    """Restrict access to func"""

    @wraps(func)
    def command_func(*args, **kwargs):
        bot, update = args
        if not Own.get_or_none(Own.house, Own.section, user=update.effective_user.id):
            if update.callback_query:
                update.callback_query.answer()
            return
        return func(bot, update, **kwargs)

    return command_func


def send_typing_action(func):
    """Sends typing action while processing func command."""

    @wraps(func)
    def command_func(*args, **kwargs):
        bot, update = args
        bot.send_chat_action(chat_id=update.effective_message.chat_id, action=ChatAction.UPLOAD_DOCUMENT)
        return func(bot, update, **kwargs)

    return command_func


def start_command(bot, update):
    """handle /start command"""
    log.info(log_msg(update))
    if update.callback_query:
        update.callback_query.answer()
    is_changed(update)
    menu_kbd(bot, update)


def help_command(bot, update):
    """handle /help command"""
    log.info(log_msg(update))
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton('Меню', callback_data='_menu')]])
    bot.sendMessage(chat_id=update.effective_user.id, text=help_msg, parse_mode=ParseMode.HTML,
                    reply_markup=reply_markup)


def about_command(bot, update):
    """handle /about command"""
    log.info(log_msg(update))
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton('Меню', callback_data='_menu')]])
    bot.sendMessage(chat_id=update.effective_user.id, text=about_msg,
                    parse_mode=ParseMode.HTML, disable_web_page_preview=True, reply_markup=reply_markup)


def menu_kbd(bot, update):
    """show keyboard to chose: show neighbors or edit own info"""
    log.info(log_msg(update))
    text = '<b>Меню:</b>\n<i>Додайте свої дані, щоб мати доступ до перегляду сусідів, та інших функцій</i>'
    keyboard = [[InlineKeyboardButton('Додати свої дані 📝', callback_data='edit')],
                [InlineKeyboardButton('Хід будівництва 🏗️', callback_data='building')],
                [InlineKeyboardButton('Статистика 📊️', callback_data='statistics')], ]

    if Own.get_or_none(Own.house, Own.section, user=update.effective_user.id):
        text = text.split('\n')[0]
        keyboard[0] = [InlineKeyboardButton('Змінити свої дані ✏', callback_data='edit')]
        keyboard += [[InlineKeyboardButton('Дивитись сусідів 👫', callback_data='show')],
                     [InlineKeyboardButton('Мій будинок 🏠', callback_data='house_neighbors'),
                      InlineKeyboardButton('Моя секція 🔢', callback_data='section_neighbors')],
                     [InlineKeyboardButton('Паркомісця 🅿️', callback_data='parking')],
                     [InlineKeyboardButton('Сповіщення 🔔', callback_data='notifications')], ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.sendMessage(chat_id=update.effective_user.id, text=text, reply_markup=reply_markup,
                    parse_mode=ParseMode.HTML)


def is_changed(update):
    log.info(log_msg(update))
    # check if user exist in DB. If not - create
    username = update.effective_user.username
    user_id = update.effective_user.id
    full_name = update.effective_user.full_name

    user, created = UserName.get_or_create(user_id=user_id)
    Show.get_or_create(user_id=user_id)

    if not created:
        # check if user changed own name attributes. If so - update
        if user.username != username or user.full_name != full_name:
            user.username = username
            user.full_name = full_name
            user.updated = datetime.now().strftime('%y.%m.%d %H:%M:%S.%f')[:-4]
            user.save()
    else:
        user.username = username
        user.full_name = full_name
        user.save()


def chosen_owns(update):
    user_id = update.effective_user.id
    try:
        user = Own.select().where(Own.user == user_id)[Show.get(user_id=user_id).owns or 0]
    except IndexError:
        user, created = Own.get_or_create(user=user_id)
    return user


@run_async
def new_neighbor_report(bot, update, created_user):
    """Send message for users who enabled notifications"""
    log.info(log_msg(update))

    # query for users who set notifications as _notify_house
    query_params = Show.select(Show.user_id).where(Show.notification_mode == '_notify_house')
    query_users = Own.select(Own.user).where(Own.house == created_user.house)
    query = query_params & query_users
    # prevent telegram blocking spam
    for i, user in enumerate(query):
        if i % 29 == 0:
            time.sleep(1)
        try:
            bot.sendMessage(chat_id=user.user_id, parse_mode=ParseMode.HTML,
                            text=f'Новий сусід\n{created_user.joined_str}')
        except BadRequest as err:
            bot.sendMessage(chat_id=ADMIN_ID, text=f'failed to send notification for user {user.user_id} {err}',
                            parse_mode=ParseMode.HTML)

    # query for users who set notifications as _notify_section
    query_params = Show.select(Show.user_id).where(Show.notification_mode == '_notify_section')
    query_users = query_users.where(Own.section == created_user.section)
    query = query_params & query_users
    for i, user in enumerate(query):
        if i % 29 == 0:
            time.sleep(1)
        try:
            bot.sendMessage(chat_id=user.user_id, parse_mode=ParseMode.HTML,
                            text=f'Новий сусід\n{created_user.joined_str}')
        except BadRequest as err:
            bot.sendMessage(chat_id=ADMIN_ID, text=f'failed to send notification for user {user.user_id} {err}',
                            parse_mode=ParseMode.HTML)


@run_async
def user_created_report(bot, update, created_user, text):
    """when created new, or updated user - send report-message for admins"""
    log.info(log_msg(update))
    bot.sendMessage(chat_id=ADMIN_ID, parse_mode=ParseMode.HTML,
                    text=f'{text} {created_user.joined_str}\n{created_user.user_id}')
    try:
        bot.sendMessage(chat_id=422485737, parse_mode=ParseMode.HTML,
                        text=f'{text} {created_user.joined_str}\n{created_user.user_id}')
    except BadRequest:
        pass
    jubilee(bot, update, created_user)


def check_owns(bot, update):
    """check how many records for user in db"""
    log.info(log_msg(update))
    if not len(Own.select().where(Own.user == update.effective_user.id)) > 1:
        if update.callback_query.data == 'house_neighbors':
            show_house(bot, update)
            return
        elif update.callback_query.data == 'section_neighbors':
            show_section(bot, update)
            return
        else:
            if not Own.get_or_none(Own.user == update.effective_user.id, Own.house):
                text = 'В якому Ви будинку ? 🏠 :'
                set_houses_kbd(bot, update, text)
            else:
                text = f'Змінюємо Ваші дані:\n{Own.get(user=update.effective_user.id).setting_str}\nВ якому Ви будинку ? 🏠 :'
                set_houses_kbd(bot, update, text)
    # if more than 1 records for user, call func for select
    else:
        select_owns(bot, update)


def select_owns(bot, update):
    """if user have more than 1 records in db, select which one to show/edit"""
    log.info(log_msg(update))
    update.callback_query.answer()

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
    user_owns = Own.select().where(Own.user == update.effective_user.id)
    for i, j in enumerate(user_owns):
        keyboard.append([InlineKeyboardButton(f'{j.edit_btn_str}', callback_data=f'set_owns{i}{view_edit}')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.message.reply_text(text=text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)


def owns_selected(bot, update):
    """save params to db"""
    log.info(log_msg(update))
    update.callback_query.answer()

    view_edit = update.callback_query.data[-13:]
    owns = [s for s in list(update.callback_query.data) if s.isdigit()]
    owns = int(''.join(owns))

    user = Show.get(user_id=update.effective_user.id)
    user.owns = owns
    user.save()

    if view_edit == 'view_my_house':
        show_house(bot, update)
    elif view_edit == 'view_my_secti':
        show_section(bot, update)
    else:
        user = Own.select().where(Own.user == update.effective_user.id)[owns]
        text = f'Змінюємо Ваші дані:\n{user.setting_str}\nВ якому Ви будинку ? 🏠 :'
        set_houses_kbd(bot, update, text)


def houses_kbd(bot, update):
    """show keyboard to chose house to show"""
    log.info(log_msg(update))
    update.callback_query.answer()

    keyboard = [[InlineKeyboardButton('Будинок 1', callback_data='p_h1'),
                 InlineKeyboardButton('Будинок 2', callback_data='p_h2')],
                [InlineKeyboardButton('Будинок 3', callback_data='p_h3'),
                 InlineKeyboardButton('Будинок 4', callback_data='p_h4')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.editMessageText('Який будинок показати ? 🏠 :', reply_markup=reply_markup,
                        message_id=update.effective_message.message_id, chat_id=update.effective_user.id)


def section_kbd(bot, update):
    """callbackQuery from houses_kbd(). show keyboard to chose section to show"""
    log.info(log_msg(update))
    update.callback_query.answer()
    user_query = Show.get(user_id=update.effective_user.id)
    user_query.house = int(update.callback_query.data[3])
    user_query.save()

    keyboard = [[InlineKeyboardButton('Секція 1', callback_data='p_s1'),
                 InlineKeyboardButton('Секція 2', callback_data='p_s2')],
                [InlineKeyboardButton('Секція 3', callback_data='p_s3'),
                 InlineKeyboardButton('Секція 4', callback_data='p_s4')],
                [InlineKeyboardButton('Секція 5', callback_data='p_s5'),
                 InlineKeyboardButton('Секція 6', callback_data='p_s6')],
                [InlineKeyboardButton('Показати всіх в цьому будинку 🏠', callback_data='show_this_house')]]

    # if selected house 3 or 4, so no 6s section there. delete it from keyboard
    if user_query.house in [3, 4]:
        del keyboard[-2][1]

    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.editMessageText('Яку секцію показати ? 🔢 :', reply_markup=reply_markup,
                        message_id=update.effective_message.message_id, chat_id=update.effective_user.id)


def save_params(bot, update):
    """callbackQuery from section_kbd(). save params to db table"""
    log.info(log_msg(update))
    update.callback_query.answer()
    user_query = Show.get(user_id=update.effective_user.id)
    user_query.section = int(update.callback_query.data[3])
    user_query.save()
    some_section = True
    show_section(bot, update, some_section=some_section)


def set_houses_kbd(bot, update, text=''):
    """show keyboard to chose its own house"""
    log.info(log_msg(update))
    update.callback_query.answer()
    # to do: Seems like can remove redundant if/else.
    if not Own.get_or_none(Own.user == update.effective_user.id, Own.house):
        text = text
    elif len(Own.select().where(Own.user == update.effective_user.id)) > 1:
        text = text
    else:
        text = text
    keyboard = [[InlineKeyboardButton('Будинок 1', callback_data='_h1'),
                 InlineKeyboardButton('Будинок 2', callback_data='_h2')],
                [InlineKeyboardButton('Будинок 3', callback_data='_h3'),
                 InlineKeyboardButton('Будинок 4', callback_data='_h4')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.editMessageText(text=text, reply_markup=reply_markup, parse_mode=ParseMode.HTML,
                        message_id=update.effective_message.message_id, chat_id=update.effective_user.id)


def set_section_kbd(bot, update):
    """callbackQuery from set_houses_kbd(). show keyboard to chose its own section"""
    log.info(log_msg(update))
    update.callback_query.answer()
    user = chosen_owns(update)
    user.house = int(update.callback_query.data[2])
    user.save()

    keyboard = [[InlineKeyboardButton('Секція 1', callback_data='_s1'),
                 InlineKeyboardButton('Секція 2', callback_data='_s2')],
                [InlineKeyboardButton('Секція 3', callback_data='_s3'),
                 InlineKeyboardButton('Секція 4', callback_data='_s4')],
                [InlineKeyboardButton('Секція 5', callback_data='_s5'),
                 InlineKeyboardButton('Секція 6', callback_data='_s6')], ]
    # if selected house 3 or 4 so no 6 section there. delete it from keyboard
    if user.house in [3, 4]:
        del keyboard[-1][1]

    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.editMessageText('В якій Ви секції ? 🔢 :', reply_markup=reply_markup, parse_mode=ParseMode.HTML,
                        message_id=update.effective_message.message_id, chat_id=update.effective_user.id)


def set_floor_kbd(bot, update):
    """callbackQuery from set_section_kbd(). show keyboard to chose its own floor"""
    log.info(log_msg(update))
    update.callback_query.answer()
    user = chosen_owns(update)
    user.section = int(update.callback_query.data[2])
    user.save()

    floors = houses_arr[f'house_{user.house}'][f'section_{user.section}']
    keyboard = []
    count_ = len(floors)
    while count_ > 0:
        floor = []
        for i in range(3):
            if count_ == 0:
                break
            floor.append(InlineKeyboardButton(f'{floors[-count_]}', callback_data=f'_f{floors[-count_]}'))
            count_ -= 1
        keyboard.append(floor)

    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.editMessageText('На якому Ви поверсі ? 🧗 :', reply_markup=reply_markup, parse_mode=ParseMode.HTML,
                        message_id=update.effective_message.message_id, chat_id=update.effective_user.id)


def set_apartment_kbd(bot, update):
    """func show message with ask to tell its own appartment"""
    log.info(log_msg(update))
    update.callback_query.answer()
    floor = [s for s in list(update.callback_query.data) if s.isdigit()]
    floor = int(''.join(floor))

    user = chosen_owns(update)
    user.floor = floor
    user.save()

    user_mode = Show.get(user_id=update.effective_user.id)
    user_mode.msg_apart_mode = True
    user_mode.save()

    text = 'В якій ви квартирі? 🚪 \nНапишіть в повідомленні номер квартири, або нажміть кнопку відмови:'
    keyboard = [[InlineKeyboardButton('Не хочу вказувати квартиру', callback_data='_apart_reject')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.message.reply_text(text=text, reply_markup=reply_markup)


@restricted
def parking_kbd(bot, update):
    """callbackQuery handler. pattern: ^parking$"""
    log.info(log_msg(update))
    update.callback_query.answer()

    keyboard = [[InlineKeyboardButton('Схема jpg 🔍️️', callback_data='park_schema_jpg_btn')],
                [InlineKeyboardButton('Схема pdf 📎️️', callback_data='park_schema_pdf_btn')],
                [InlineKeyboardButton('Моє паркомісце 🚗', callback_data='set_parking_btn')],
                [InlineKeyboardButton('Усі власники 👥', callback_data='_parking_owners_btn')],
                [InlineKeyboardButton('Меню', callback_data='_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.callback_query.message.text:
        bot.editMessageText(message_id=update.effective_message.message_id, text='Меню <code>Паркомісця</code>',
                            chat_id=update.effective_user.id, reply_markup=reply_markup, parse_mode=ParseMode.HTML)
    else:
        bot.sendMessage(chat_id=update.effective_user.id, reply_markup=reply_markup, parse_mode=ParseMode.HTML,
                        text='Меню <code>Паркомісця</code>')


def parking_house_kbd(bot, update):
    """callbackQuery handler. pattern: ^set_parking_btn$"""
    log.info(log_msg(update))
    update.callback_query.answer()
    text = '<b>Паркінг якого будинку? :</b>'

    keyboard = [[InlineKeyboardButton('Будинок 1', callback_data='_parkhouse-1'),
                 InlineKeyboardButton('Будинок 2', callback_data='_parkhouse-2')],
                [InlineKeyboardButton('Будинок 3', callback_data='_parkhouse-3'),
                 InlineKeyboardButton('Будинок 4', callback_data='_parkhouse-4')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    bot.editMessageText(text=text, reply_markup=reply_markup, parse_mode=ParseMode.HTML,
                        message_id=update.effective_message.message_id, chat_id=update.effective_user.id)


@send_typing_action
def parking_schema(bot, update):
    """callbackQuery handler. pattern: ^park_schema_jpg_btn$|^park_schema_pdf_btn$"""
    log.info(log_msg(update))
    update.callback_query.answer()

    keyboard = [[InlineKeyboardButton('Назад', callback_data='parking'),
                InlineKeyboardButton('Меню', callback_data='_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.callback_query.data == 'park_schema_jpg_btn':
        media = [InputMediaPhoto(open(os.path.join('img', 'parking_h_1.jpg'), 'rb')),
                 InputMediaPhoto(open(os.path.join('img', 'parking_h_2.jpg'), 'rb')), ]
        bot.sendMediaGroup(chat_id=update.effective_user.id, media=media)
        bot.sendMessage(chat_id=update.effective_user.id, parse_mode=ParseMode.HTML,
                        reply_markup=reply_markup, text='<b>Схеми паркінгу будинків 1 та 2:</b>')
    elif update.callback_query.data == 'park_schema_pdf_btn':
        bot.sendDocument(chat_id=update.effective_user.id, document=open(os.path.join('img', 'parking_h_1.pdf'), 'rb'),
                         caption='Схема Паркінгу будинку 1')
        bot.sendDocument(chat_id=update.effective_user.id, document=open(os.path.join('img', 'parking_h_2.pdf'), 'rb'),
                         reply_markup=reply_markup, caption='Схема Паркінгу будинку 2')


# to do: refactor or create package parking
def set_parking(bot, update):
    """callbackQuery handler. pattern: ^_next_btn$|^_previous_btn$|^_parkhouse-"""
    log.info(log_msg(update))
    update.callback_query.answer()
    user_id = update.effective_user.id
    user, created = Parking.get_or_create(user_id=user_id)

    if '_parkhouse-' in update.callback_query.data:
        parking_house = int(update.callback_query.data.split('-')[1])
        user.house = parking_house
        user.save()

    previous_btn = InlineKeyboardButton('⏪ Попередні', callback_data='_previous_btn')
    next_btn = InlineKeyboardButton('Наступні ⏩', callback_data='_next_btn')
    menu_btn = InlineKeyboardButton('Меню', callback_data='_menu')
    back_btn = InlineKeyboardButton('Назад', callback_data='parking')

    query = Parking.select().where(Parking.house == user.house)
    query = [i.parking for i in query]

    keyboard = []
    if '_parkhouse-' in update.callback_query.data or '_previous_btn' in update.callback_query.data:
        for i in range(0, 50, 5):
            row = []
            for j in range(1, 6):
                icon = f'🔑' if j + i in query else f''
                row.append(InlineKeyboardButton(str(j + i) + icon, callback_data=f'_park_place-{j + i}'))
            keyboard.append(row)
        keyboard.append([menu_btn, back_btn, next_btn])
    else:
        for i in range(50, 105, 5):
            row = []
            for j in range(1, 6):
                icon = f'🔑' if j + i in query else f''
                row.append(InlineKeyboardButton(str(j + i) + icon, callback_data=f'_park_place-{j + i}'))
            keyboard.append(row)
        keyboard.append([menu_btn, back_btn, previous_btn])

    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.editMessageText(message_id=update.effective_message.message_id, text='Вкажіть Ваше паркомісце\n',
                        chat_id=user_id, reply_markup=reply_markup, parse_mode=ParseMode.HTML)


def save_parking(bot, update):
    """callbackQuery handler. pattern: ^_park_place-"""
    log.info(log_msg(update))
    update.callback_query.answer()
    user_id = update.effective_user.id
    park_place = int(update.callback_query.data.split('-')[1])

    keyboard = [[InlineKeyboardButton('Назад', callback_data='parking')],
                [InlineKeyboardButton('Меню', callback_data='_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    user = Parking.get(user_id=user_id)
    user.parking = park_place
    user.save()
    bot.editMessageText(message_id=update.effective_message.message_id, text='<b>Дякую Ваші дані збережено!</b>',
                        chat_id=user_id, reply_markup=reply_markup, parse_mode=ParseMode.HTML)


@restricted
def show_parking(bot, update):
    """callbackQuery handler. pattern: ^_parking_owners_btn$"""
    log.info(log_msg(update))
    update.callback_query.answer()

    keyboard = [[InlineKeyboardButton('Назад', callback_data='parking')],
                [InlineKeyboardButton('Меню', callback_data='_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    parkings = Parking.select(Parking.house).where(Parking.parking).distinct().order_by(Parking.house)
    query = Parking.select().where(Parking.parking).order_by(Parking.parking)

    neighbors = []
    for i in parkings:
        neighbors.append(f'\n{"<b>Паркінг будинку №".rjust(30, " ")} {i.house}</b>\n')
        for user in query.where(Parking.house == i.house):
            neighbors.append(f'{user.user} <b>{user.parking}</b>\n')

    show_list = ('<b>Власники паркомісць</b>:\n'
                 + '{}' * len(neighbors)).format(*neighbors)

    bot.editMessageText(text=show_list, parse_mode=ParseMode.HTML, reply_markup=reply_markup,
                        chat_id=update.effective_user.id, message_id=update.effective_message.message_id)


def msg_handler(bot, update):
    """handle all text msg except other filters do"""
    msg = update.message.text
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton('Меню', callback_data='_menu')]])
    bot.sendPhoto(chat_id=update.effective_user.id, photo=open(os.path.join('img', 'maybe.jpg'), 'rb'),
                  reply_markup=reply_markup,
                  caption=f'Я ще не розумію людської мови, але вчусь, і скоро буду розуміть деякі слова і фрази\n'
                  f'Краще скористайтесь меню')
    log.info(log_msg(update) + f' text: {msg}')


def group_chat_logging(bot, update):
    """handle text msgs in group chat. MessageHandler((Filters.text & Filters.group)"""
    msg = update.message.text
    log_chat.info(log_msg(update) + f' msg: {msg}')

    src = os.path.join('logfiles', 'log_chat.log')
    if os.stat(src).st_size > 10 ** 6:
        dst = os.path.join('logfiles', datetime.now().strftime('%y.%m.%d ') + 'log_chat.log')
        shutil.copyfile(src, dst)
        with open(src, 'w'):
            pass


def jubilee(bot, update, created_user):
    """Check if new added user is 'hero of the day' i.e some round number in db"""
    log.info(log_msg(update))
    celebration_count = [i for i in range(0, 2000, 50)]
    query = Own.select().where(Own.house, Own.section)

    check_list = [query.where(Own.house == i).count() for i in range(1, 5)]
    total = query.count()
    text = f'сусідів 🎇 🎈 🎉 🎆 🍹\nВітаємо\n{created_user.joined_str}'

    for count, house in enumerate(check_list, start=1):
        if house in celebration_count:
            x, created = Jubilee.get_or_create(house=count, count=house)
            if created:
                text = f'В будинку № {count} Вже зареєстровано {house} ' + text
                try:
                    bot.sendMessage(chat_id=-1001076439601, text=text, parse_mode=ParseMode.HTML)  # test chat
                except BadRequest:
                    bot.sendMessage(chat_id=-1001307649156, text=text, parse_mode=ParseMode.HTML)
                return

    if total in celebration_count:
        text = f'Вже зареэстровано {total} сусідів 🎇 🎈 🎉 🎆 🍹\nВітаємо\n{created_user.joined_str}'
        x, created = Jubilee.get_or_create(house=0, count=total)
        if created:
            try:
                bot.sendMessage(chat_id=-1001076439601, text=text, parse_mode=ParseMode.HTML)  # test chat
            except BadRequest:
                bot.sendMessage(chat_id=-1001307649156, text=text, parse_mode=ParseMode.HTML)


def save_user_data(bot, update):
    """callbackQuery handler. pattern: ^_apart_reject$|^_section_reject$ AND integer text handler"""
    log.info(log_msg(update))
    if update.callback_query:
        update.callback_query.answer()

    user = chosen_owns(update)
    user_mode = Show.get(user_id=update.effective_user.id)

    if user_mode.msg_apart_mode and update.message:
        apartment = int(update.message.text)
        user.apartment = apartment
    else:
        if update.callback_query.data == '_apart_reject':
            user.apartment = None

    user.updated = datetime.now().strftime('%y.%m.%d %H:%M:%S.%f')[:-4]
    user.save()
    user_mode.msg_apart_mode = False
    user_mode.save()

    text = f'В базе {"ОБНОВЛЕН" if user.updated else "СОЗДАН"} пользователь:\n'
    user_created_report(bot, update, created_user=user, text=text)
    new_neighbor_report(bot, update, created_user=user)

    text_success = '<b>Дякую, Ваші дані збережені</b>. Бажаєте подивитись сусідів?'
    bot.sendMessage(text=text_success, chat_id=update.effective_user.id, parse_mode=ParseMode.HTML)
    menu_kbd(bot, update)

    prepared_data = prepare_data()
    make_pie(prepared_data)
    make_bars(prepared_data)


@restricted
def show_house(bot, update):
    """ """
    log.info(log_msg(update))
    update.callback_query.answer()
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton('Меню', callback_data='_menu')]])

    if update.callback_query.data == 'show_this_house':
        # if user want see selected house
        user_query = Show.get(user_id=update.effective_user.id)
    else:
        # if user want see own house and have one
        user_query = chosen_owns(update)

    neighbors = []
    sections = Own.select(Own.section).where(Own.house == user_query.house, Own.section).distinct().order_by(
        Own.section)
    query = Own.select().where(Own.house == user_query.house, Own.section).order_by(Own.floor)

    for i in sections:
        neighbors.append(f'\n{"📭 <b>Секція".rjust(30, " ")} {i.section}</b>\n')
        for user in query.where(Own.section == i.section):
            neighbors.append(f'{user.user}   {user}\n')

    show_list = (f'<b>Мешканці будинку № {user_query.house}</b>:\n'
                 + '{}' * len(neighbors)).format(*neighbors)

    if len(show_list) < 6200:
        bot.sendMessage(chat_id=update.effective_user.id, parse_mode=ParseMode.HTML, text=show_list,
                        reply_markup=reply_markup)
    else:
        part_1, part_2, part_3 = show_list.partition('📭 <b>Секція 4'.rjust(30, ' ') + '</b>' + '\n')
        bot.sendMessage(chat_id=update.effective_user.id, parse_mode=ParseMode.HTML, text=part_1[:-2])
        # to do: remove "." from 2nd msg. Without that dot, rjust not works
        bot.sendMessage(chat_id=update.effective_user.id, parse_mode=ParseMode.HTML, text='.' + part_2 + part_3,
                        reply_markup=reply_markup)


@restricted
def show_section(bot, update, *args, some_section=False):
    """Here need some documentation"""
    log.info(log_msg(update))
    update.callback_query.answer()
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton('Меню', callback_data='_menu')]])

    if not some_section:
        user_query = chosen_owns(update)
    else:
        user_query = Show.get(user_id=update.effective_user.id)

    query = Own.select().where(Own.house == user_query.house, Own.section == user_query.section).order_by(Own.floor)
    neighbors = [f'{user.user}   {user}\n' for user in query]
    show_list = (f'<b>Мешканці секції № {user_query.section} Будинку № {user_query.house}</b>:\n'
                 + '{}' * len(neighbors)).format(*neighbors)

    bot.sendMessage(chat_id=update.effective_user.id, parse_mode=ParseMode.HTML,
                    disable_web_page_preview=True, text=show_list, reply_markup=reply_markup)


def catch_err(bot, update, error):
    """handle all telegram errors end send report. There is no 'update' so can't logging much info"""
    user_id = update.effective_user.id if update else 'no update'
    try:
        raise error
    except Unauthorized:
        bot.sendMessage(chat_id=ADMIN_ID, text=f'ERROR:\n {error}\n type {type(error)} id: {user_id}')
    except BadRequest:
        bot.sendMessage(chat_id=ADMIN_ID, text=f'ERROR:\n {error}\n type {type(error)} id: {user_id}')
    except (TimedOut, NetworkError, TelegramError):
        bot.sendMessage(chat_id=ADMIN_ID, text=f'ERROR:\n {error}\n type {type(error)} id: {user_id}')


# to do: apply to more then 1 custom filter
@run_async
def del_msg(bot, update):
    """message text handler for specific words in group chats MessageHandler((Filters.group & block_filter).
    See filters in classes module
    """
    chat_id = update.message.chat_id
    message_id = update.message.message_id
    pattern = block_filter(update.message)
    warn_msg = f'Повідомлення які містять <code>{pattern}</code> видаляються автоматично'

    bot.deleteMessage(chat_id=chat_id, message_id=message_id)
    deleted_msg = bot.sendMessage(chat_id=chat_id, parse_mode=ParseMode.HTML, text=warn_msg)
    time.sleep(5)
    bot.deleteMessage(chat_id=chat_id, message_id=deleted_msg.message_id)
    log.info(log_msg(update) + f' {pattern}')


@run_async
def greeting(bot, update):
    """handle new chat members, and sent greeting message. Delete after delay. Running async"""
    log.info(log_msg(update))
    new_member_name = update.message.new_chat_members[0].full_name
    text = greeting_msg.format(new_member_name)
    update.message.reply_text(text=text, parse_mode=ParseMode.HTML, disable_web_page_preview=True)


def prepare_data():
    """Create show_list (string) for statistic message, and pie_values (list) for chart"""
    log.info('this func has no update')

    query = Own.select().where(Own.house, Own.section)
    houses = query.select(Own.house).distinct().order_by(Own.house)
    total_users = UserName.select().count()

    # did users indicate their info
    intro_yes = Own.select(Own.user).where(Own.house, Own.section).distinct().count()
    intro_not = total_users - intro_yes
    introduced = {'Yes': intro_yes, 'No': intro_not}

    # last 3 joined users
    last_3_users = list(reversed(query.order_by(Own.id)[-3:]))

    neighbors = []
    pie_values = []
    bars_values = {}
    for house_ in houses:
        count = query.where(Own.house == house_.house).count()
        pie_values.append(count)
        neighbors.append(f'\n{"🏠 <b>Будинок".rjust(30, " ")} {house_.house}</b> <code>({count})</code>\n')
        sections = query.select(Own.section).where(Own.house == house_.house).distinct().order_by(Own.section)
        section_dict = {}
        for section_ in sections:
            count = query.where(Own.house == house_.house, Own.section == section_.section).count()
            neighbors.append(f'Секція{section_.section} <code>({count})</code>\n')
            section_dict[section_.section] = count
        bars_values[house_.house] = section_dict

    show_list = (f'<b>Всього користувачів: {total_users}</b>\n'
                 f'<i>Дані вказані {intro_yes}</i>\n'
                 f'<i>Дані не вказані {intro_not}</i>\n'
                 + '{}' * len(neighbors)).format(*neighbors) + '\n<b>Нові користувачі</b>'

    for i in last_3_users:
        show_list += f'\n{i.joined_str}'

    return {'show_list': show_list, 'pie_values': pie_values, 'bars_values': bars_values, 'introduced': introduced}


def statistics_kbd(bot, update):
    """callbackQuery handler. pattern:^statistics$"""
    log.info(log_msg(update))
    update.callback_query.answer()
    keyboard = [[InlineKeyboardButton('Загальна інфо', callback_data='statistics_common')],
                [InlineKeyboardButton('Графіка 📊', callback_data='charts')],
                [InlineKeyboardButton('Чат 💬', callback_data='statistics_chat')],
                [InlineKeyboardButton('Меню', callback_data='_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.editMessageText('<b>Меню</b> <code>Статистика</code>', reply_markup=reply_markup, parse_mode=ParseMode.HTML,
                        message_id=update.effective_message.message_id, chat_id=update.effective_user.id)


def statistics_common(bot, update):
    """callbackQuery handler. pattern:^statistics_common$"""
    CommonStat(bot, update).answer(bot, update, prepare_data()['show_list'])


@send_typing_action
def charts(bot, update):
    """callbackQuery handler. pattern:^charts$. Show chart"""
    Charts(bot, update).answer(bot, update)


def statistics_chat(bot, update):
    """Statistics for messaging in group chat. Show top 10 by msgs and by chars"""
    ChatStat(bot, update).answer(bot, update)


@run_async
def make_pie(prepared_data):
    """create pie total by houses"""
    log.info('this func has no update')

    # func for setting values format on pie
    def make_autopct(values):
        def my_autopct(pct):
            total = sum(values)
            val = int(round(pct * total / 100.0))
            return val

        return my_autopct

    # pie by houses
    sizes = prepared_data['pie_values']
    labels = [f'Буд. {i + 1}' for i in range(len(sizes))]
    fig1, ax1 = plt.subplots(figsize=None)
    ax1.pie(
        sizes, labels=labels, autopct=make_autopct(sizes), radius=1.3, pctdistance=0.8, shadow=True, labeldistance=1.1
    )
    img_path = os.path.join('img', 'charts', '1_pie.png')
    fig1.savefig(img_path)
    fig1.clf()
    plt.close()

    # pie by introduced
    sizes = list(prepared_data['introduced'].values())
    labels = list(prepared_data['introduced'].keys())
    fig2, ax2 = plt.subplots(figsize=None)
    ax2.pie(
        sizes, labels=labels, autopct=make_autopct(sizes), radius=1.3, pctdistance=0.8, shadow=True, labeldistance=1.1
    )
    ax2.set_title(label='Користувачі вказали свої дані', pad=15)
    img_path = os.path.join('img', 'charts', '2_pie.png')
    fig2.savefig(img_path)
    fig2.clf()
    plt.close()


@run_async
def make_bars(prepared_data):
    """create bars for houses sections count"""
    log.info('this func has no update')

    # to do: enable time.sleep(0.5) if async will make unexpected charts
    # time.sleep(0.5)
    values_ = prepared_data['bars_values']

    def autolabel(rects, height_factor):
        for i, rect in enumerate(rects):
            height = rect.get_height()
            label = '%d' % int(height)
            ax3.text(rect.get_x() + rect.get_width() / 2., height_factor * height,
                     '{}'.format(label),
                     ha='center', va='bottom')

    for house in values_:
        sections = [f'Сек{i[-1]}' for i in houses_arr[f'house_{house}']]
        values = [values_[house].get(int(i[-1]), 0) for i in sections]

        fig3, ax3 = plt.subplots()
        ax3.bar(sections, values)
        ax3.set_title(f'Будинок {house}')
        autolabel(ax3.patches, height_factor=0.85)

        img_path = os.path.join('img', 'charts', f'bar{house}.png')
        fig3.savefig(img_path, dpi=200)
        fig3.clf()
        plt.close()


def notifications_kbd(bot, update):
    """callbackQuery handler. pattern:^notifications$. Show notifications keyboard settings"""
    log.info(log_msg(update))
    update.callback_query.answer()
    user = Show.get(user_id=update.effective_user.id)

    keyboard = [[InlineKeyboardButton('В моєму будинку 🏠', callback_data='_notify_house')],
                [InlineKeyboardButton('В моїй секції 🔢', callback_data='_notify_section')],
                [InlineKeyboardButton('Вимкнути сповіщення 🔕', callback_data='_notify_OFF')],
                [InlineKeyboardButton('Меню', callback_data='_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    _dict = {None: 'Вимкнено', '_notify_OFF': 'Вимкнено',
             '_notify_section': 'В моїй секції 🔢', '_notify_house': 'В моєму будинку 🏠'}

    text = f'Зараз сповіщення встановленні в режим\n' \
        f'<b>{_dict[user.notification_mode]}</b>\nОтримувати сповіщення коли з\'явиться новий сусід:'

    bot.editMessageText(chat_id=update.effective_user.id, parse_mode=ParseMode.HTML,
                        text=text, reply_markup=reply_markup, message_id=update.effective_message.message_id)


def notifications_save(bot, update):
    """callbackQuery handler. pattern: from notifications_kbd func. Save notifications settings to db"""
    log.info(log_msg(update))
    update.callback_query.answer()
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton('Меню', callback_data='_menu')]])

    user = Show.get(user_id=update.effective_user.id)
    user.notification_mode = update.callback_query.data
    user.save()
    bot.editMessageText('<b>Ок!</b> Налаштування збережено', reply_markup=reply_markup, parse_mode=ParseMode.HTML,
                        message_id=update.effective_message.message_id, chat_id=update.effective_chat.id, )


def del_command(bot, update):
    """For deleting commands sent in group chat. MessageHandler(Filters.command & Filters.group).
    If so - delete message from group chat. """
    command = re.sub(r'@.*', '', update.message.text)
    log.info(log_msg(update) + f' DEL {command}')
    chat_id = update.message.chat_id
    message_id = update.message.message_id
    bot.deleteMessage(chat_id=chat_id, message_id=message_id)
    commands = {'/start': start_command,
                '/help': help_command,
                '/about': about_command}
    try:
        commands[command](bot, update)
    except KeyError:
        pass


def building(bot, update):
    """CallbackQueryHandler. pattern ^building$"""
    log.info(log_msg(update))
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton('Меню', callback_data='_menu')]])
    bot.sendMessage(chat_id=update.effective_user.id, text=building_msg,
                    parse_mode=ParseMode.HTML, disable_web_page_preview=True, reply_markup=reply_markup)
    update.callback_query.answer()


def main():
    updater = Updater(KEY)

    dp = updater.dispatcher
    # group filters
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, greeting))
    dp.add_handler(MessageHandler((Filters.command & Filters.group), del_command))
    dp.add_handler(MessageHandler((Filters.group & block_filter), del_msg))
    dp.add_handler(MessageHandler((Filters.text & Filters.group), group_chat_logging))
    # commands
    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("about", about_command))

    dp.add_handler(MessageHandler(filt_integers, save_user_data))
    dp.add_handler(MessageHandler(Filters.text, msg_handler))
    dp.add_handler(CallbackQueryHandler(start_command, pattern='^_menu$'))
    dp.add_handler(CallbackQueryHandler(building, pattern='^building$'))
    # statistics
    dp.add_handler(CallbackQueryHandler(statistics_kbd, pattern='^statistics$'))
    dp.add_handler(CallbackQueryHandler(statistics_common, pattern='^statistics_common$'))
    dp.add_handler(CallbackQueryHandler(statistics_chat, pattern='^statistics_chat$'))
    dp.add_handler(CallbackQueryHandler(charts, pattern='^charts$'))

    dp.add_handler(CallbackQueryHandler(notifications_kbd, pattern='^notifications$'))
    dp.add_handler(CallbackQueryHandler(notifications_save, pattern='^_notify_section$|^_notify_house$|^_notify_OFF$'))
    dp.add_handler(CallbackQueryHandler(houses_kbd, pattern='^show$'))
    dp.add_handler(CallbackQueryHandler(show_house, pattern='^show_this_house$'))
    dp.add_handler(CallbackQueryHandler(section_kbd, pattern='^p_h'))
    dp.add_handler(CallbackQueryHandler(save_params, pattern='^p_s'))
    dp.add_handler(CallbackQueryHandler(check_owns, pattern='^edit$|^house_neighbors$|section_neighbors'))
    dp.add_handler(CallbackQueryHandler(owns_selected, pattern='^set_owns'))
    dp.add_handler(CallbackQueryHandler(set_section_kbd, pattern='^_h'))
    dp.add_handler(CallbackQueryHandler(save_user_data, pattern='^_apart_reject$'))
    # parking
    dp.add_handler(CallbackQueryHandler(parking_kbd, pattern='^parking$'))
    dp.add_handler(CallbackQueryHandler(parking_house_kbd, pattern='^set_parking_btn$'))
    dp.add_handler(CallbackQueryHandler(parking_schema, pattern='^park_schema_jpg_btn$|^park_schema_pdf_btn$'))
    dp.add_handler(CallbackQueryHandler(set_parking, pattern='^_next_btn$|^_previous_btn$|^_parkhouse-'))
    dp.add_handler(CallbackQueryHandler(save_parking, pattern='^_park_place-'))
    dp.add_handler(CallbackQueryHandler(show_parking, pattern='^_parking_owners_btn$'))

    dp.add_handler(CallbackQueryHandler(set_floor_kbd, pattern='^_s'))
    dp.add_handler(CallbackQueryHandler(set_apartment_kbd, pattern='^_f'))

    dp.add_error_handler(catch_err)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
