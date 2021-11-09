import abc

import config
import myqq


class IMessageDispatcher(object, metaclass=abc.ABCMeta):
    def __init__(self, name: str, tips: str):
        self.name = name
        self.tips = tips

    @abc.abstractmethod
    def check_auth(self, qq: str) -> bool:
        pass

    @abc.abstractmethod
    def execute(self, qq_group_number: str, qq: str, *args: str) -> None:
        pass


messages: dict[str, IMessageDispatcher] = {}


class GetTips(IMessageDispatcher):
    def __init__(self):
        super().__init__('查看帮助', '查看帮助')

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
        super().__init__('[@' + config.qq['robot_self_qq'] + ']', '')

    def check_auth(self, qq: str) -> bool:
        return True

    def execute(self, qq_group_number: str, qq: str, *args: str) -> None:
        msg = '你可以使用以下功能：'
        for m in messages.values():
            if m.check_auth(qq) and m.tips != '':
                msg += '\n' + m.tips
        myqq.send_group_message(qq_group_number, msg)


class Test(IMessageDispatcher):
    def __init__(self):
        super().__init__('测试', '测试')

    def check_auth(self, qq: str) -> bool:
        return True

    def execute(self, qq_group_number: str, qq: str, *args: str) -> None:
        myqq.send_group_message(qq_group_number, '返回测试')
