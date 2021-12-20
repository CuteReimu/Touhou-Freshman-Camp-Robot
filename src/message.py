import abc

import config
import myqq


class IMessageDispatcher(object, metaclass=abc.ABCMeta):
    """这是聊天指令处理器的父类，当你想要新增自己的聊天指令处理器时，继承这个类即可。
    最后，不要忘记在message_dispatcher.py中的init_message函数里面加入你新增的这个聊天指令处理器。"""

    @property
    @abc.abstractmethod
    def name(self) -> str:
        """群友输入聊天指令时，第一个空格前的内容。"""
        pass

    @property
    @abc.abstractmethod
    def tips(self) -> str:
        """在【帮助列表】中应该如何显示这个命令。空字符串表示不显示"""
        pass

    @abc.abstractmethod
    def check_auth(self, qq: str) -> bool:
        """如果他有权限执行这个指令，则返回True，否则返回False"""
        pass

    @abc.abstractmethod
    def execute(self, qq_group_number: str, qq: str, *args: str) -> None:
        """args参数是一个str的list，也就是除开指令名（第一个空格前的部分）以外，剩下的所有内容按照空格进行拆分"""
        pass


messages: dict[str, IMessageDispatcher] = {}


class GetTips(IMessageDispatcher):
    @property
    def name(self) -> str:
        return '查看帮助'

    @property
    def tips(self) -> str:
        return '查看帮助'

    def check_auth(self, qq: str) -> bool:
        return True

    def execute(self, qq_group_number: str, qq: str, *args: str) -> None:
        msg = '你可以使用以下功能：'
        for m in messages.values():
            if m.check_auth(qq) and m.tips != '':
                msg += '\n' + m.tips
        myqq.send_group_message(qq_group_number, msg)


class GetTips2(IMessageDispatcher):  # 处理艾特请求
    def __init__(self):
        self.__name = '[@%s]' % config.qq['robot_self_qq']

    @property
    def name(self) -> str:
        return self.__name

    @property
    def tips(self) -> str:
        return ''

    def check_auth(self, qq: str) -> bool:
        return True

    def execute(self, qq_group_number: str, qq: str, *args: str) -> None:
        msg = '你可以使用以下功能：'
        for m in messages.values():
            if m.check_auth(qq) and m.tips != '':
                msg += '\n' + m.tips
        myqq.send_group_message(qq_group_number, msg)


class Test(IMessageDispatcher):
    @property
    def name(self) -> str:
        return '测试'

    @property
    def tips(self) -> str:
        return '测试'

    def check_auth(self, qq: str) -> bool:
        return True

    def execute(self, qq_group_number: str, qq: str, *args: str) -> None:
        myqq.send_group_message(qq_group_number, '返回测试')
