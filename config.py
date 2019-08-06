import logging
from datetime import datetime
from pytz import timezone, utc
import os


def customTime(*args):
    utc_dt = utc.localize(datetime.utcnow())
    my_tz = timezone("Europe/Kiev")
    converted = utc_dt.astimezone(my_tz)
    return converted.timetuple()


def log_msg(update):
    return f'id: {update.effective_user.id} name: {update.effective_user.full_name} usrnm: {update.effective_user.username}'


logging.Formatter.converter = customTime

log = logging.getLogger('logger_1')
fh = logging.FileHandler('logfile.log', encoding='utf-8')
fh.setLevel(logging.INFO)
fh.setFormatter(logging.Formatter('{asctime} {message} {funcName}', datefmt='%y.%m.%d %H:%M:%S', style='{'))
log.addHandler(fh)
log.setLevel(logging.INFO)

log_chat = logging.getLogger('logger_2')
fh2 = logging.FileHandler(os.path.join('log_chat.log'), encoding='utf-8')
fh2.setLevel(logging.INFO)
fh2.setFormatter(logging.Formatter('{asctime} {message}', datefmt='%y.%m.%d %H:%M:%S', style='{'))
log_chat.addHandler(fh2)
log_chat.setLevel(logging.INFO)
