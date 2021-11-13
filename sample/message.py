import abc

import mirai_bot
from mirai_bot_chain import plain


class IMessageDispatcher(object, metaclass=abc.ABCMeta):
    """这是聊天指令处理器的父类，当你想要新增自己的聊天指令处理器时，继承这个类即可。
    最后，不要忘记在message_dispatcher.py中的init_message函数里面加入你新增的这个聊天指令处理器。"""

    def __init__(self, name: str, tips: str):
        """name是群友输入聊天指令时，第一个空格前的内容。tips是查看帮助时显示的内容。"""
        self.name = name
        self.tips = tips

    @abc.abstractmethod
    def check_auth(self, qq: int) -> bool:
        """如果他有权限执行这个指令，则返回True，否则返回False"""
        pass

    @abc.abstractmethod
    def execute(self, qq_group_number: int, qq: int, *args: str) -> None:
        """args参数是一个str的list，也就是除开指令名（第一个空格前的部分）以外，剩下的所有内容按照空格进行拆分"""
        pass


messages: dict[str, IMessageDispatcher] = {}


class GetTips(IMessageDispatcher):
    def __init__(self):
        super().__init__('查看帮助', '查看帮助')

    def check_auth(self, qq: int) -> bool:
        return True

    def execute(self, qq_group_number: int, qq: int, *args: str) -> None:
        msg = '你可以使用以下功能：'
        for m in messages.values():
            if m.check_auth(qq) and m.tips != '':
                msg += '\n' + m.tips
        mirai_bot.send_group_message(qq_group_number, [plain(msg)])


class Test(IMessageDispatcher):
    def __init__(self):
        super().__init__('测试', '测试')

    def check_auth(self, qq: int) -> bool:
        return True

    def execute(self, qq_group_number: int, qq: int, *args: str) -> None:
        mirai_bot.send_group_message(qq_group_number, [plain('返回测试')])
