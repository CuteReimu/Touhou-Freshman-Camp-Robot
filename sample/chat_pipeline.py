import abc

import message
import message_dispatcher
from logger import logger


class IChatPipeline(object, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def on_init(self):
        pass

    @abc.abstractmethod
    def execute(self, qq_group_number: str, qq: str, msg: str) -> str:
        pass


pipelines: list[IChatPipeline] = []


class MessagePipeline(IChatPipeline):
    def on_init(self):
        message_dispatcher.init_message()

    def execute(self, qq_group_number: str, qq: str, msg: str) -> str:
        arr = msg.split('+')  # MyQQ会自动把空格转为加号，所以这里要用+分隔
        d = message.messages.get(arr[0])
        if d is not None and d.check_auth(qq) and '[pic={' not in msg:
            logger.info("%s说：%s", qq, msg)
            d.execute(qq_group_number, qq, *arr[1:])
        return msg
