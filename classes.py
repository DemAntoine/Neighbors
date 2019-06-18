from telegram.ext import BaseFilter


class MyFilters(BaseFilter):
    """Custom text filters
    """
    def call_err(self, message):
        return 'error' in message.text

    def custom_text(self, message):
        return 'custom' in message.text


filt_call_err = MyFilters().call_err
filt_custom = MyFilters().custom_text

