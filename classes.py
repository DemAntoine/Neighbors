from telegram.ext import BaseFilter
import re


class MyFilters(BaseFilter):
    """Custom text filters
    """

    def call_err(self, message):
        return 'error' in message.text

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


filt_call_err = MyFilters().call_err
filt_flood = MyFilters().flood
filt_fuck = MyFilters().fuck


# pattern = r'(флуд\w{,4}\s{,2}|бубнилк\w{,4}\s)'
# pattern = r'\bфлуд\w{,4}\b|\bбубнилк\w{,4}\b'
# string = 'here is a mpythonm флудhggg         string for бубнилк Pythontt things'
# re.findall(pattern=pattern, string=string, flags=re.IGNORECASE)
#
# print(True if re.findall(pattern, string, flags=re.IGNORECASE) else False)
#
# print(re.findall(pattern, string, flags=re.IGNORECASE))


# print(True == [False, []])
