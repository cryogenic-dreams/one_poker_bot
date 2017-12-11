import telegram.bot
from telegram.ext import messagequeue as mq
from strings import Strings
from telegram.utils.request import Request

class MQBot(telegram.bot.Bot):
    """
    A subclass of Bot which delegates send method handling to MQ
    GentleBot is gentle with messages so telegram doesn't ban it
    """
    def __init__(self, is_queued_def=True, mqueue=None, *args, **kwargs):
        super(MQBot, self).__init__(Strings.TOKEN, request=Request(con_pool_size=8), **kwargs)
        # below 2 attributes should be provided for decorator usage
        self._is_messages_queued_default = is_queued_def
        self._msg_queue = mqueue or mq.MessageQueue()

    def __del__(self):
        try:
            self._msg_queue.stop()
        except:
            pass
        super(MQBot, self).__del__()

    @mq.queuedmessage
    def send_message(self, *args, **kwargs):
        """
        Wrapped method would accept new `queued` and `isgroup`
        OPTIONAL arguments
        """
        super(MQBot, self).send_message(*args, **kwargs)
