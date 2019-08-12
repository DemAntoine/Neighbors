from telegram import ParseMode, InputMediaPhoto
from statistic import Stat
import os
import re
from constants import WarAndPeace
from models import Own, Chat


class CommonStat(Stat):
    def __init__(self, bot, update):
        super().__init__(bot, update)

    def answer(self, bot, update, show_list):
        if not Own.get_or_none(Own.house, Own.section, user=update.effective_user.id):
            for i in range(1, 6):
                show_list = show_list.replace(show_list.split('\n')[-i], '')
            show_list = show_list[:-5]

        bot.editMessageText(chat_id=update.effective_user.id, parse_mode=ParseMode.HTML, text=show_list,
                            message_id=update.effective_message.message_id, reply_markup=self.reply_markup)


class Charts(Stat):
    def __init__(self, bot, update):
        super().__init__(bot, update)

    def answer(self, bot, update):
        charts_dir = os.path.join('img', 'charts')
        charts_list = sorted([f for f in os.listdir(charts_dir) if not f.startswith('.')])
        media = [InputMediaPhoto(open(os.path.join('img', 'charts', i), 'rb')) for i in charts_list]

        bot.sendMediaGroup(chat_id=update.effective_user.id, media=media)
        bot.sendMessage(chat_id=update.effective_user.id, parse_mode=ParseMode.HTML,
                        reply_markup=self.reply_markup, text='Повернутись в меню:')


class ChatStat(Stat):
    def __init__(self, bot, update):
        super().__init__(bot, update)

    def answer(self, bot, update):
        data = {}
        query = Chat.select().order_by(-Chat.id)
        for msg in query:
            try:
                data[msg.user_id][0] += msg.msg_len
                data[msg.user_id][1] += 1
            except KeyError:
                data[msg.user_id] = [msg.msg_len, 1, msg.full_name]
        
        by_chars = sorted(data.items(), key=lambda x: x[1][0], reverse=True)
        by_msgs = sorted(data.items(), key=lambda x: x[1][1], reverse=True)
        by_chars_avg = sorted(filter(lambda x: x[1][1] > 5, data.items()), key=lambda x: (x[1][0] / x[1][1]))

        template = '<a href="tg://user?id={}">{}</a> {}'

        top_chars = [template.format(user[0], user[1][2], user[1][0]) + '\n' for user in by_chars[:10]]
        top_msgs = [template.format(user[0], user[1][2], user[1][1]) + '\n' for user in by_msgs[:10]]
        top_chars_avg_min = [template.format(user[0], user[1][2], round(user[1][0] / user[1][1])) + '\n' for user in by_chars_avg[:10]]
        top_chars_avg_max = [template.format(user[0], user[1][2], round(user[1][0] / user[1][1])) + '\n' for user in by_chars_avg[-10:]]
        top_chars_avg_max.reverse()
        total_chars = sum([i[0] for i in data.values()])

        show_list = ('<i>Вже написано {:.2%} роману Війна і Мир</i>'.format(total_chars/WarAndPeace) + '\n\n' +
                     '<b>Лідери по кількості знаків</b>\n' + '{}'
                     * len(top_chars)).format(*top_chars) + '\n' + \
                    ('<b>Лідери по кількості повідомлень</b>\n' + '{}'
                     * len(top_msgs)).format(*top_msgs) + '\n' + \
                    ('<b>Найдовші повідомлення</b> <i>Сер. довжина</i>\n' + '{}'
                     * len(top_chars_avg_max)).format(*top_chars_avg_max) + '\n' + \
                    ('<b>Найкоротші повідомлення</b> <i>Сер. довжина</i>\n' + '{}'
                     * len(top_chars_avg_min)).format(*top_chars_avg_min)

        bot.editMessageText(chat_id=update.effective_user.id, message_id=update.effective_message.message_id,
                            parse_mode=ParseMode.HTML, text=show_list, reply_markup=self.reply_markup)
