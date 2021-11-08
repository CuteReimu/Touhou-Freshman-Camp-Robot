import abc
import myqq


class IMessageDispatcher(object, metaclass=abc.ABCMeta):
    def __init__(self, name: str, tips: str):
        self.name = name
        self.tips = tips

    @abc.abstractmethod
    def check_auth(self, qq: str) -> bool:
        pass

    @abc.abstractmethod
    def execute(self, qq: str, *args: list[str]):
        pass


class Test(IMessageDispatcher):
    def __init__(self):
        super().__init__('测试', '测试')

    def check_auth(self, qq: str) -> bool:
        return True

    def execute(self, qq: str, *args: list[str]):
        myqq.send_group_message(qq, '返回测试')


class Dispatcher:
    def __init__(self):
        self.messages: dict[str, IMessageDispatcher] = {}
        self.__init_message(Test())

    def __init_message(self, msg: IMessageDispatcher):
        if msg.name in self.messages:
            raise KeyError
        self.messages[msg.name] = msg
