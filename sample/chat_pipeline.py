import abc

import config
import message
import message_dispatcher
from logger import logger


class IChatPipeline(object, metaclass=abc.ABCMeta):
    """这是消息处理器的父类，当你想要新增自己的消息处理器时，继承这个类即可。
    最后，不要忘记在chat_pipeline_manager.py中的init_chat_pipeline函数里面加入你新增的这个消息处理器。"""

    @abc.abstractmethod
    def on_init(self):
        """在程序开始，加载过程中，会执行这个函数。"""
        pass

    @abc.abstractmethod
    def execute(self, qq_group_number: int, qq: int, msg_chain: list) -> str:
        """每次收到QQ消息时会执行这个函数。
        这个函数的返回值会传给下一个消息处理器，作为msg参数传入。
        如果你不打算影响后续的消息处理器，在执行完自己的代码后，直接return msg即可。
        如果你打算打断后续的消息处理器，那么return ‘’空字符串即可。"""
        pass


pipelines: list[IChatPipeline] = []


class MessagePipeline(IChatPipeline):
    def on_init(self):
        message_dispatcher.init_message()

    @staticmethod
    def __is_at_message(msg_chain: list) -> True:
        if len(msg_chain) < 2:
            return False
        contains_at = True
        for idx in range(1, len(msg_chain)):
            if msg_chain[idx]['type'] == 'At':
                if msg_chain[idx]['target'] == config.qq['robot_self_qq']:
                    contains_at = True
            elif msg_chain[idx]['type'] == 'Plain':
                if msg_chain[idx]['text'].strip() != '':
                    return False
            else:
                return False
        return contains_at

    def execute(self, qq_group_number: int, qq: int, msg_chain: list) -> str:
        if self.__is_at_message(msg_chain):
            msg_chain = [msg_chain[0], {'type': 'Plain', 'text': '查看帮助'}]
        if len(msg_chain) == 2 and msg_chain[1]['type'] == 'Plain':
            msg = msg_chain[1]['text']
            arr = msg.split(' ')
            d = message.messages.get(arr[0])
            if d is not None and d.check_auth(qq):
                logger.info("%s说：%s", qq, msg)
                d.execute(qq_group_number, qq, *arr[1:])
            return msg
