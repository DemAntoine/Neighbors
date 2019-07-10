from telegram.ext import BaseFilter
import re


class MyFilters(BaseFilter):
    """Custom text filters"""

    def call_err(self, message):
        return 'error' in message.text

    def integers(self, message):
        if message.text:
            pattern = r'^[0-9]+$'
            found = re.findall(pattern, message.text)
            return found if found else False

    def flood(self, message):
        pattern = r'\bфлуд\w{,4}\b|\bбубнил\w{,4}\b'
        if message.text:
            found = re.findall(pattern, message.text, flags=re.IGNORECASE)
            return found if found else False

    def fuck(self, message):
        pattern = r'\bхуй\w{,4}\b|\bп.зда\w{,4}\b'
        if message.text:
            found = re.findall(pattern, message.text, flags=re.IGNORECASE)
            return found if found else False


filt_integers = MyFilters().integers
filt_call_err = MyFilters().call_err
filt_flood = MyFilters().flood
filt_fuck = MyFilters().fuck
