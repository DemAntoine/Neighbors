from telegram.ext import BaseFilter


class MyFilters(BaseFilter):
    """Custom text filters
    """
    def call_err(self, message):
        return 'error' in message.text

    def test_feature(self, message):
        return 'test_feature' in message.text


filt_call_err = MyFilters().call_err
filt_test_feature = MyFilters().test_feature
