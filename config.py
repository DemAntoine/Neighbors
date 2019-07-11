import logging
import time
import sys
from datetime import datetime
from pytz import timezone, utc


LOGGER_CONFIG = {
    'level': logging.INFO,
    'file': 'logfile.log',
    'formatter': logging.Formatter('{asctime} {message} {funcName}', datefmt='%y.%m.%d %H:%M:%S', style='{')
}


def customTime(*args):
    utc_dt = utc.localize(datetime.utcnow())
    my_tz = timezone("Europe/Kiev")
    converted = utc_dt.astimezone(my_tz)
    return converted.timetuple()


def log_msg(update):
    return f'id: {update.effective_user.id} name: {update.effective_user.full_name}-{update.effective_user.username}'


log = logging.getLogger()
# set custom timezone for logging
logging.Formatter.converter = customTime
fh = logging.FileHandler(LOGGER_CONFIG['file'], encoding='utf-8')
fh.setLevel(LOGGER_CONFIG['level'])
fh.setFormatter(LOGGER_CONFIG['formatter'])
log.addHandler(fh)
log.setLevel(LOGGER_CONFIG['level'])
