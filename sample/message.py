import abc

import config
import message_admin
import message_live
import message_whitelist
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
        myqq.send_group_message(qq, '返回测试')


def __init_message(msg: IMessageDispatcher):
    if msg.name in messages:
        raise KeyError
    messages[msg.name] = msg


def init_message():
    __init_message(Test())
    __init_message(GetTips())
    __init_message(GetTips2())
    __init_message(message_admin.GetAdmin())
    __init_message(message_admin.DelAdmin())
    __init_message(message_admin.AddAdmin())
    __init_message(message_whitelist.GetWhitelist())
    __init_message(message_whitelist.DelWhitelist())
    __init_message(message_whitelist.AddWhitelist())
    __init_message(message_live.GetLiveState())
    __init_message(message_live.StartLive())
    __init_message(message_live.StopLive())
    __init_message(message_live.ChangeLiveTitle())
