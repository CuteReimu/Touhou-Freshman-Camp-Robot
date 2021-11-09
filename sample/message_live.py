import message
import message_admin
from bilibili import Bilibili

bili = Bilibili()


class GetLiveState(message.IMessageDispatcher):
    def __init__(self):
        super().__init__('直播状态', '直播状态')

    def check_auth(self, qq: str) -> bool:
        return True

    def execute(self, qq_group_number: str, qq: str, *args: str) -> None:
        if len(args) != 0:
            return
        bili.get_live_status(qq_group_number)


class StartLive(message.IMessageDispatcher):
    def __init__(self):
        super().__init__('开始直播', '开始直播')

    def check_auth(self, qq: str) -> bool:
        return qq in message_admin.admin_cache

    def execute(self, qq_group_number: str, qq: str, *args: str) -> None:
        if len(args) != 0:
            return
        bili.start_live(qq_group_number, qq)


class StopLive(message.IMessageDispatcher):
    def __init__(self):
        super().__init__('关闭直播', '关闭直播')

    def check_auth(self, qq: str) -> bool:
        return qq in message_admin.admin_cache

    def execute(self, qq_group_number: str, qq: str, *args: str) -> None:
        if len(args) != 0:
            return
        bili.stop_live(qq_group_number)


class ChangeLiveTitle(message.IMessageDispatcher):
    def __init__(self):
        super().__init__('修改直播标题', '修改直播标题 新标题')

    def check_auth(self, qq: str) -> bool:
        return qq in message_admin.admin_cache

    def execute(self, qq_group_number: str, qq: str, *args: str) -> None:
        if len(args) < 1 or len(args) > 10:
            return
        title = ''
        for s in args:
            if title != '':
                title += ' '
            title += s
        bili.change_live_title(qq_group_number, title)
